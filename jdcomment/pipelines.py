# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from datetime import datetime
import MySQLdb
import MySQLdb.cursors

from twisted.enterprise import adbapi
'''
MySQL中创建数据库
CREATE DATABASE jdcommentsdb DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
MySQL中创建表
CREATE TABLE jdcomments(
name varchar(60) NOT NULL COMMENT '名字',
userProvince varchar(20) DEFAULT '' COMMENT '省份',
comments varchar(800) COMMENT '评论',
commtime datetime DEFAULT NULL COMMENT '时间',
prosize_col varchar(80) DEFAULT '' COMMENT '产品',
level varchar(80) DEFAULT '' COMMENT '等级',
mobile varchar(80) DEFAULT '' COMMENT '移动端'
)ENGINE=MyISAM DEFAULT CHARSET=utf8;


'''
class JdcommentPipeline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls,settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db = settings['MYSQL_DBNAME'],
            user = settings['MYSQL_USER'],
            passwd= settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode= True
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self._do_upinsert, item, spider)
        return d


    def _do_upinsert(self, conn, item, spider):
        try:
            conn.execute('insert into jdcomments values(%s, %s, %s, %s, %s, %s,%s)',
                        (item['name'],
                         item['userProvince'],
                         item['comments'],
                         item['commtime'].replace('/','-'),
                         item['prosize_col'],
                         item['level'],
                         item['mobile']))
        except MySQLdb.Error,e :
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])













