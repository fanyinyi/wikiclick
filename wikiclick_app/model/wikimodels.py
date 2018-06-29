#!/usr/bin/python3
import pymysql
import config
import datetime
from model.wikidb import WikiDbConnection
import json
# from face import DateEncoder
from decimal import Decimal
import simplejson as json


class WikiModel(WikiDbConnection):

    # pagerank
    def searh_log(self, **kwargs):
        try:
            # 往数据库里添加用户信息。
            self.connect()
            sql = "select * from test3 where date = %s order by score desc limit 0,%s"

            # 执行sql语句
            self.cursor.execute(sql, (kwargs['date'], int(kwargs['k'])))
            # 获取所有记录列表
            results = self.cursor.fetchall()
# print(results)
            return results
        except Exception as e:
            print(e)


    # realTime
    def searh_realTime(self, **kwargs):
        try:
            # 往数据库里添加用户信息。
            self.connect()


            sql = "select curr_title,sum(n) as score  from intime where from_unixtime(time/1000) between date_add(now(), interval - %s minute) and now() group by curr_title order by score desc limit 0,%s"

            # 执行sql语句
            self.cursor.execute(sql, (int(kwargs['minute']), int(kwargs['k'])))
            # 获取所有记录列表
            results = self.cursor.fetchall()

            return results
        except Exception as e:
            print(e)
