# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from work_utils.mysql_client import MysqlClient
import logging


class ZxNetworkPipeline(object):
    def __init__(self):
        self.mysql_client = MysqlClient(host='localhost', port=3306, user='root', password='axy#mysql2019',db='shihe_data')
        self.logger = logging.getLogger(__name__)

    def process_item(self, item, spider):
        oname = item["oname"]
        if oname:
            # print('主体：%s' % oname)
            try:
                self.mysql_client.insert('zxxx_xg', item)
                # print("插入:%s" % item["oname"])
                # self.logger.debug("已成功插入MySQL,公司名称:%s" % item["oname"])
            except pymysql.OperationalError as e:
                # print('插入失败,错误：%s' % repr(e))
                # logging.debug('插入失败,错误：%s' % repr(e))
                raise e
            except Exception as e:
                if "Duplicate" in repr(e):
                    # print("公司名称:%s已经存在数据库" % item["oname"])
                    logging.debug("公司名称:%s已经存在数据库" % item["oname"])
                else:
                    # print('插入失败,错误：%s' % repr(e))
                    logging.debug('插入失败,错误：%s' % repr(e))
        return item

    def close_spider(self, spider):  # 爬虫一旦关闭，就会实现这个方法，关闭数据库连接
        pass
