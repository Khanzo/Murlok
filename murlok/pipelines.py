# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from peewee import *
import logging

class MurlokPipeline(object):
    
    def open_spider(self, spider):   
        if spider.murlok.format == 'mysql':
            self.conn = MySQLDatabase(spider.murlok.db,
                                      user = spider.murlok.user,
                                      password = spider.murlok.passw,
                                      host = spider.murlok.host,
                                      port = int(spider.murlok.port))
        if spider.murlok.format == 'postg':
            self.conn = PostgresqlDatabase(spider.murlok.db,
                                      user = spider.murlok.user,
                                      password = spider.murlok.passw,
                                      host = spider.murlok.host,
                                      port = int(spider.murlok.port))
        if spider.murlok.format == 'sqlite':
            self.conn = SqliteDatabase(spider.murlok.db, pragmas={'journal_mode':'wal', 'cache_size': -1024 * 64})
            self.conn.connect()
        pass
    
    def process_item(self, item, spider): 
        if spider.murlok.format == 'sqlite':
            s_t = spider.murlok.generatesql()            
            dd = spider.murlok.getDict(item)
            sql = s_t.substitute(dd)            
            logging.log(logging.WARNING, sql)
            self.conn.execute_sql(sql) 
        else:
            with self.conn.cursor() as cursor:
                s_t = spider.murlok.generatesql()            
                dd = spider.murlok.getDict(item)
                sql = s_t.substitute(dd)
                logging.log(logging.WARNING, sql)
                cursor.execute(sql)
            self.conn.commit()
        return item
    
    def close_spider(self, spider): 
        self.conn.close()
        pass