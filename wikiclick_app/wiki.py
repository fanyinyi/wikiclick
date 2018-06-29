# -*- coding: utf-8 -*
from tornado import web, ioloop, httpserver
from model.wikimodels import  WikiModel
import base64
import json
import os.path
import datetime


# 首页
class MainPageHandler(web.RequestHandler):  # 逻辑处理模块

    def get(self, *args, **kwags):
        self.render('batch.html')


# 获取PageRank
class pageRank(web.RequestHandler):

    def get(self):
        model = WikiModel()
        result = model.searh_realTime(minute=5, k=int(10))
        print(result)

        jsonresponse = [{"date": '', "rank": float(x['score']), "topic": x['curr_title']} for x in result]
        print(type(jsonresponse))
        print(jsonresponse)
        self.write(json.dumps(jsonresponse))

    def post(self, *args, **kwags):

        task = self.get_argument('task')
        date = self.get_argument('date')
        k = self.get_argument('num')

# k = 10

        if task == 'pageRank':
            model = WikiModel()
            result = model.searh_log(date=date, k=int(k))
            jsonresponse = [{"date":x['date'],"rank":float(x['score']),"topic":x['curr_title']} for x in result]

            self.render('pagerank.html', output=jsonresponse)

        if task == 'realTime':
            model = WikiModel()
            result = model.searh_realTime(minute=date, k=int(k))
            print(result)

            jsonresponse = [{"date":'',"rank":float(x['score']),"topic":x['curr_title']} for x in result]
            self.render('pagerank.html', output=jsonresponse)



# 设置
settings = dict(
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    debug=True,
)

aplication = web.Application([  # 设置前端网页的访问入口，即路由

# (r"/", LoginHandler),
    (r"/index", MainPageHandler),
    (r"/pagerank", pageRank)

], cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__", **settings)


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return json.JSONEncoder.default(self, obj)

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(DecimalEncoder, self).default(o)

if __name__ == '__main__':  # socket服务，提出并响应http请求
    http_server = httpserver.HTTPServer(aplication)
    http_server.listen(8888)  # 访问端口号
    ioloop.IOLoop.current().start()

