from pyspark.sql import SparkSession
import pymysql
from pyspark import *
from operator import add
from sql import *
import pyspark

import sys

reload(sys)

sys.setdefaultencoding('utf-8')
'''
def spark():
    sc = SparkContext('local','top K')
    in_path = sc.textFile("s3a://wikiclick/dataset/2016_02_en_clickstream.tsv")
    raw = sc.textFile(in_path)
    header = raw.first()
    textFile = raw.filter(lambda x: x != header)
    res = textFile.map(lambda x: csv_to_array(x)).reduceByKey(add).collect()
    return res
'''
def csv_to_array(line):
    sp = line.split('\t')
     #'curr_title', 'n', 'date'
    return (str(sp[4].encode('utf-8')),int(sp[2]))

def csv_to_array1(line):
    sp = line.split('\t')
             #'prev_title','curr_title', 'n', 'date'
    return (str(sp[3].encode('utf-8')),str(sp[4].encode('utf-8')),int(sp[2]))

def init():
    sess = SparkSession \
           .builder \
           .appName("sql") \
           .config("spark.some.config.option", "some-value") \
           .getOrCreate()
    return sess

def compute():
# sess = init()
    host = 'sqlforwiki.carf1itkjlds.us-east-1.rds.amazonaws.com'
    port = 3306
    user = 'wikiclick'
    password = 'wikiclick'
    db = 'wikiclick'
    url = 'jdbc:mysql://%s:%d/%s?user=%s&password=%s' % (host, port, db, user, password)
# df = sess.read.jdbc(url, 'test', properties={"driver": 'com.mysql.jdbc.Driver'})
#               df.map(lambda x: ((x[1]), (1 if x[0].startswith('empty') else 2, 1, x[2]))).reduceByKey(add) \
#                           .map(lambda x: (x[0], caculate(x[1])))
#    df = spark()
    sc = SparkContext().getOrCreate()
    in_path = "s3a://wikiclick/dataset/2015_02_en_clickstream.tsv" 
# in_path = '/home/ubuntu/data/project/test1.tsv'
    raw = sc.textFile(in_path)
    header = raw.first()
    df = raw.filter(lambda x: x != header)
#   df = sc.textFile("s3a://wikiclick/dataset/2016_02_en_clickstream.tsv")
    
    
    df = df.map(lambda x: csv_to_array(x)).reduceByKey(add)
    df = df.map(lambda x: {'curr_title':x[0],'score':x[1],'date':'2015-02'})
#    df = df.map(lambda x: csv_to_array1(x))
#    df = df.map(lambda x: {'prev_title':x[0],'curr_title':x[1],'n':x[2],'date':'2015-01'})
    sqlContext = pyspark.sql.SQLContext(sc)
    sqldata = sqlContext.createDataFrame(df)
#    sqldata.show()
    sqldata.write.jdbc(url, 'test3',  mode="append", properties={"driver": 'com.mysql.jdbc.Driver'})

if __name__ == '__main__':
    compute()
