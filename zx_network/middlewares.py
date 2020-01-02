# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy.downloadermiddlewares.retry import RetryMiddleware
import logging
from scrapy.utils.response import response_status_message
from scrapy.utils.python import global_object_name
import json
from urllib.parse import unquote
from urllib.parse import urlencode
from urllib import parse
from work_utils.get_code import correct_code

logger = logging.getLogger(__name__)


class MyRetryMiddleware(RetryMiddleware):
    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response

        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) \
                and not request.meta.get('dont_retry', False):
            return self._retry(request, exception, spider)

    def _retry(self, request, reason, spider):
        retries = request.meta.get('retry_times', 0) + 1

        retry_times = self.max_retry_times

        if 'max_retry_times' in request.meta:
            retry_times = request.meta['max_retry_times']

        stats = spider.crawler.stats

        if retries <= retry_times:
            logger.debug("Retrying %(request)s (failed %(retries)d times): %(reason)s",
                         {'request': request, 'retries': retries, 'reason': reason},
                         extra={'spider': spider})
            retryreq = request.copy()
            retryreq.meta['retry_times'] = retries
            retryreq.dont_filter = True
            retryreq.priority = request.priority + self.priority_adjust

            if isinstance(reason, Exception):
                reason = global_object_name(reason.__class__)

            stats.inc_value('retry/count')
            stats.inc_value('retry/reason_count/%s' % reason)
            return retryreq
        else:
            stats.inc_value('retry/max_reached')
            logger.debug("Gave up retrying %(request)s (failed %(retries)d times): %(reason)s",
                         {'request': request, 'retries': retries, 'reason': reason},
                         extra={'spider': spider})


class ProcessException(object):
    def process_exception(self, request, exception, spider):
        # print('获取异常%s' % repr(exception))
        if 'TimeoutError' in repr(exception):
            logger.info('请求超时-请求url-{}-重新请求'.format(request.url))
            return request
        elif 'ConnectionError' in repr(exception):
            return request
        elif 'PDFSyntaxError' in repr(exception):
            return request
        elif 'ConnectionRefusedError' in repr(exception):
            return request
        elif 'JSONDecodeError' in repr(exception):
            return request
        else:
            print(repr(exception))


class FailResponseContentMiddleware(object):  # 检查响应内容 及状态码
    def process_response(self, request, response, spider):
        url = response.url
        url2 = 'http://zxgk.court.gov.cn/xgl/searchXgl.do'
        response_status = response.status
        # print(response_status)
        if url == url2:
            if response_status != 200:
                code, captcha_id = correct_code()
                request_body = unquote(request.body.decode())
                body_dict = dict(parse.parse_qsl(request_body))
                body_dict['pCardNum'] = ''
                body_dict['pCode'] = code
                body_dict['captchaId'] = captcha_id
                request.meta['pCode'] = code
                request.meta['captchaId'] = captcha_id
                quote_body = urlencode(body_dict)
                request = request.replace(body=quote_body, meta=request.meta)
                request.priority = 1000
                # print(request.body)
                # print('修改成功')
                return request
            else:
                response_content = response.text
                # print(response_content)
                try:
                    dict_data = json.loads(response_content)
                    data = dict_data[0]
                    # print('获取数据成功')
                    return response
                except Exception as e:  # 验证码失效 更换验证码 返回请求内容
                    # print("访问页面失败，错误：%s" % repr(e))
                    code, captcha_id = correct_code()
                    request_body = unquote(request.body.decode())
                    body_dict = dict(parse.parse_qsl(request_body))
                    body_dict['pCardNum'] = ''
                    body_dict['pCode'] = code
                    body_dict['captchaId'] = captcha_id
                    request.meta['pCode'] = code
                    request.meta['captchaId'] = captcha_id
                    quote_body = urlencode(body_dict)
                    request = request.replace(body=quote_body, meta=request.meta)
                    request.priority = 1000
                    # print(request.body)
                    # print('修改成功')
                    return request
        return response
