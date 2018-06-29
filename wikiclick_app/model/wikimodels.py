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

    # Page rank
    def search_log(self, **kwargs):
        try:
            self.connect()
            sql_query = "select * from test3 where date = %s order by score desc limit 0,%s"

            # Executing sql!
            self.cursor.execute(sql_query, (kwargs['date'], int(kwargs['num_to_show'])))

            # Getting records
            results = self.cursor.fetchall()
            return results
        except Exception as e:
            print(e)


    # Traffic Source
    def search_traffic(self, **kwargs):
        try:
            self.connect()

            date_receive = kwargs['date']
            date_post = date_receive.replace("-", "")

            sql_query ="select prev_title, n from rawdata" + date_post + " where curr_title=%s order by n desc limit %s"

            # Executing sql!
            self.cursor.execute(sql_query, (kwargs['page_title'],int(kwargs['num_to_show'])))

            # Getting records
            results = self.cursor.fetchall()

            return results
        except Exception as e:
            print(e)
