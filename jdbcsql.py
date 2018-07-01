from pyspark.sql import SparkSession
from pyspark import *
from operator import add
from sql import *
import pyspark

import sys

reload(sys)

sys.setdefaultencoding('utf-8')

def csv_to_array(line):
    sp = line.split('\t')
     #'curr_title', 'n', 'date'
    return (str(sp[4].encode('utf-8')),int(sp[2]))

def csv_to_array1(line):
    sp = line.split('\t')
             #'prev_title','curr_title', 'n', 'date'
    return (str(sp[3].encode('utf-8')),str(sp[4].encode('utf-8')),int(sp[2]))

# Initial Spark session
def init():
    sess = SparkSession \
           .builder \
           .appName("sql") \
           .config("spark.some.config.option", "some-value") \
           .getOrCreate()
    return sess

# Spark Calculation
def compute():
    host = 'xxxxx.carf1itkjlds.us-east-1.rds.amazonaws.com'
    port = 3306
    user = 'wikiclick'
    password = 'xxxx'
    db = 'wikiclick'
    url = 'jdbc:mysql://%s:%d/%s?user=%s&password=%s' % (host, port, db, user, password)

    sc = SparkContext().getOrCreate()
    in_path = "s3a://wikiclick/dataset/*.tsv"

    raw = sc.textFile(in_path)

    # Skip the header
    header = raw.first()
    df = raw.filter(lambda x: x != header)
    df = df.map(lambda x: csv_to_array(x)).reduceByKey(add)
    df = df.map(lambda x: {'curr_title':x[0],'score':x[1],'date':'2015-02'})
    sqlContext = pyspark.sql.SQLContext(sc)
    sqldata = sqlContext.createDataFrame(df)
    sqldata.write.jdbc(url, 'test3',  mode="append", properties={"driver": 'com.mysql.jdbc.Driver'})

if __name__ == '__main__':
    compute()
