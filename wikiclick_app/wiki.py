# -*- coding: utf-8 -*
from tornado import web, ioloop, httpserver
from model.wikimodels import  WikiModel
import base64
import json
import os.path
import datetime


# Main Page
class MainPageHandler(web.RequestHandler):

    def get(self, *args, **kwags):
        self.render('batch.html')


# Get PageRank
class pageRank(web.RequestHandler):

    def get(self):
        model = WikiModel()
        result = model.search_traffic(minute=5, k=int(10))
        print(result)

        jsonresponse = [{"date": '', "rank": float(x['score']), "topic": x['curr_title']} for x in result]
        print(type(jsonresponse))
        print(jsonresponse)
        self.write(json.dumps(jsonresponse))

    def post(self, *args, **kwags):

        task = self.get_argument('task')
        date = self.get_argument('date')
        num_to_show = self.get_argument('num_to_show')

        if task == 'Historic_Page_Rank':
            model = WikiModel()
            result = model.search_log(date=date, num_to_show=int(num_to_show))
            jsonresponse = [{"date":x['date'],"rank":float(x['score']),"topic":x['curr_title']} for x in result]

            self.render('pagerank.html', output=jsonresponse)

        if task == 'Traffic_Source':
            model = WikiModel()
            result = model.search_traffic(date=date, num_to_show=int(num_to_show),page_title=page_title)
            jsonresponse = [{"date":x['date'],"rank":float(x['n']),"topic":x['curr_title']} for x in result]

            self.render('pagerank.html', output=jsonresponse)

# Setting
settings = dict(
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    debug=True,
)

aplication = web.Application([  # Setting the path to log in

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

if __name__ == '__main__':  # Socket service，request and respond to http
    http_server = httpserver.HTTPServer(aplication)
    http_server.listen(8888)  # default port
    ioloop.IOLoop.current().start()

