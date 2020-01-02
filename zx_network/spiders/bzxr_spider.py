# -*- coding: utf-8 -*-
import scrapy
import json
import re
import time
from work_utils.get_code import correct_code
from work_utils.get_db_company import get_keyword
from work_utils.get_md5 import get_md5
from io import BytesIO
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBoxHorizontal
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed, PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfparser import PDFParser, PDFDocument

with open('keys.txt', 'r', encoding='utf-8') as f:
    key_words = f.read()
key_list = key_words.split(' ')


class BzxrSpiderSpider(scrapy.Spider):
    name = 'xg_spider'
    base_info = {
        "sj_type": 64,
        "xxly": "中国执行信息网-限高数据补充",
        "site_id": 31084
    }

    allowed_domains = ['zxgk.court.gov.cn']

    # start_urls = ['http://zxgk.court.gov.cn/']
    # def start_requests(self):
    #     start_num = 6
    #     end_num = 10
    #     for key in key_list[start_num:end_num]:
    #         for h in h_list:
    #             key_word = key + h
    #             code, captcha_id = correct_code()
    #             url = 'http://zxgk.court.gov.cn/xgl/searchXgl.do'
    #             form_data = {
    #                 "pName": key_word,
    #                 "pCardNum": "",
    #                 "selectCourtId": "0",
    #                 "pCode": code,
    #                 "captchaId": captcha_id,
    #                 "searchCourtName": "全国法院（包含地方各级法院）",
    #                 "selectCourtArrange": "1",
    #                 "currentPage": "1",
    #             }
    #             meta = {
    #                 'code': code,
    #                 'captcha_id': captcha_id,
    #                 'pName': key_word,
    #             }
    #             yield scrapy.FormRequest(url=url, formdata=form_data, meta=meta, callback=self.page_parse)
    def start_requests(self):
        for key in key_list:
            key_word = key
            code, captcha_id = correct_code()
            # code = '123'
            url = 'http://zxgk.court.gov.cn/xgl/searchXgl.do'
            form_data = {
                "pName": key_word,
                "pCardNum": "",
                "selectCourtId": "0",
                "pCode": code,
                "captchaId": captcha_id,
                "searchCourtName": "全国法院（包含地方各级法院）",
                "selectCourtArrange": "1",
                "currentPage": "1",
            }
            meta = {
                'code': code,
                'captcha_id': captcha_id,
                'pName': key_word,
            }
            yield scrapy.FormRequest(url=url, formdata=form_data, meta=meta, callback=self.page_parse)

    def page_parse(self, response):
        content = response.text
        # print(content)
        content_dict = json.loads(content)[0]
        total_size = content_dict.get('totalSize')  # 总共有多少数据
        if total_size > 0:
            # for i in range(1, (total_page + 1)):
            content_list = content_dict.get('result')
            for each_content in content_list:
                cf_wsh = each_content.get('AH', '')
                lian_sj = each_content.get('LASJStr', '')
                oname = each_content.get('XM', '')
                oname2 = each_content.get('QY_MC', '')
                path = each_content.get('FILEPATH', '')
                xq_url = "http://zxgk.court.gov.cn/xglfile" + path
                if path:
                    item = {
                        'oname': oname,
                        'oname2': oname2,
                        'cf_wsh': cf_wsh,
                        'lian_sj': lian_sj,
                        'xq_url': xq_url
                    }
                    meta = {'item': item}
                    yield scrapy.Request(url=xq_url, meta=meta, callback=self.parse_detail_page)
            total_page = content_dict.get('totalPage')  # 总共有多少页
            current_page = content_dict.get('currentPage')  # 当前页
            # print(current_page)
            if total_page > current_page:
                p_name = response.meta.get('pName')  # 获取关键词
                current_page += 1  # 页码+1
                code = response.meta.get('code')
                captcha_id = response.meta.get('captcha_id')
                url = 'http://zxgk.court.gov.cn/xgl/searchXgl.do'
                pg = str(current_page)
                form_data = {
                    "pName": p_name,
                    "pCardNum": "",
                    "selectCourtId": "0",
                    "pCode": code,
                    "captchaId": captcha_id,
                    "searchCourtName": "全国法院（包含地方各级法院）",
                    "selectCourtArrange": "1",
                    "currentPage": pg,
                }
                meta = {
                    'code': code,
                    'captcha_id': captcha_id,
                    'pName': p_name,
                    'pg': pg,
                    'total_page': total_page
                }
                yield scrapy.FormRequest(url=url, formdata=form_data, meta=meta, callback=self.page_parse)
            else:
                pass
        else:
            pass
            # print('关键词:%s无数据' % p_name)

    def parse_detail_page(self, response):
        """
        解析详情页
        """
        item = response.meta.get("item")
        # 解析pdf格式
        new_item = self.parse_pdf(response)
        if new_item:
            item = {**item, **new_item}
            item = {**item, **self.base_info}
            if not item.get("cf_jdrq"):
                item['cf_jdrq'] = ''
            ws_nr_txt_list = item.get("ws_nr_txt", "").split(" ")
            oname2 = item.get('oname2', '')
            if oname2:  # 如果有两个主体 拆开
                filter_str1 = item.get("oname", "") + item.get("zxfy", "") + item.get("cf_jdrq", "")
                oname2 = item.pop('oname2')
                item["md5_id"] = get_md5(filter_str1)
                yield item
                item['oname'] = oname2
                filter_str2 = item.get("oname", "") + item.get("zxfy", "") + item.get("cf_jdrq", "")
                item["md5_id"] = get_md5(filter_str2)
                yield item
            else:
                filter_str1 = item.get("oname", "") + item.get("zxfy", "") + item.get("cf_jdrq", "")
                item["md5_id"] = get_md5(filter_str1)
                item.pop('oname2')
                yield item

                # try:
                #     if item.get("oname") != ws_nr_txt_list[3]:
                #         item["zqr"] = ws_nr_txt_list[3]
                # except Exception as e:
                #     self.logger.error(repr(e))

    def parse_pdf(self, response):
        """
        解析pdf响应
        """
        try:
            content_list = self.pdf2txt(response)  # 文本列表，一行一个元素
        except Exception as e:
            with open('error_pdf.txt', "a") as file:  # 下载文件异常处理
                file.write(response.url + "\n")
            return
        content_list = [line.strip() for line in content_list if line.strip()]
        cf_jdrq = content_list[-1]
        cf_jdrq = self.jdrq_word_to_digit(cf_jdrq)
        zxfy = content_list[0].strip()
        content = "".join(content_list).replace("(cid:9)", "")
        sy_pattern = re.compile(r'本院于.*?给付义务')
        yj_pattern = re.compile(r'本院依照.*?采取限制消费措施')
        cf_sy = sy_pattern.search(content)
        if cf_sy:
            cf_sy = cf_sy.group()
        else:
            cf_sy = ""
        cf_yj = yj_pattern.search(content)
        if cf_yj:
            cf_yj = cf_yj.group()
        else:
            cf_yj = ""
        item = dict(cf_sy=cf_sy, cf_yj=cf_yj, cf_jdrq=cf_jdrq, zxfy=zxfy, ws_nr_txt=" ".join(content_list))
        return item

    def jdrq_word_to_digit(self, cf_jdrq):
        """
        汉字的日期转数字日期
        """
        mapper = {"〇": "0", "一": "1", "二": "2", "三": "3", "四": "4", "五": "5", "六": "6", "七": "7", "八": "8",
                  "九": "9", "年": "-", "月": "-", "日": "-"}

        # 替换年月日，及1-9汉字
        new_jdrq = ""
        for word in cf_jdrq:
            if word in mapper.keys():
                new_jdrq += mapper[word]
            else:
                new_jdrq += word
        # 处理十，分几种情况，1.在最左边，在中间，在最后边
        cf_jdrq = ""
        digit_list = [str(digit) for digit in range(1, 10)]
        for idx, word in enumerate(new_jdrq):
            if word == "十":
                # 最左边
                if new_jdrq[idx - 1] == '-' and new_jdrq[idx + 1] in digit_list:
                    cf_jdrq += "1"
                elif new_jdrq[idx - 1] == "-" and new_jdrq[idx + 1] not in digit_list:
                    cf_jdrq += "10"
                elif new_jdrq[idx - 1] in digit_list and new_jdrq[idx + 1] in digit_list:
                    cf_jdrq += ""
                else:
                    cf_jdrq += "0"
            else:
                cf_jdrq += word
        return cf_jdrq[:-1]

    def pdf2txt(self, response):
        """
        解析PDF文本，并保存到TXT文件中
        :param filepath:
        :return:
        """
        # 用文件对象创建一个PDF文档分析器
        parser = PDFParser(BytesIO(response.body))
        # 创建一个PDF文档
        doc = PDFDocument()
        # 连接分析器，与文档对象
        parser.set_document(doc)
        doc.set_parser(parser)
        # 提供初始化密码，如果没有密码，就创建一个空的字符串
        doc.initialize()
        # 检测文档是否提供txt转换，不提供就忽略
        if not doc.is_extractable:
            raise PDFTextExtractionNotAllowed
        else:
            # 创建PDF，资源管理器，来共享资源
            rsrcmgr = PDFResourceManager()
            # 创建一个PDF设备对象
            laparams = LAParams()
            device = PDFPageAggregator(rsrcmgr, laparams=laparams)
            # 创建一个PDF解释其对象
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            # 循环遍历列表，每次处理一个page内容
            # doc.get_pages() 获取page列表
            result_list = []
            for page in doc.get_pages():
                interpreter.process_page(page)
                # 接受该页面的LTPage对象
                layout = device.get_result()
                # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象
                # 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等
                # 想要获取文本就获得对象的text属性，
                for x in layout:
                    if isinstance(x, LTTextBoxHorizontal):
                        line = x.get_text()
                        line = line.replace(" ", "")
                        result_list.append(line)
            return result_list
