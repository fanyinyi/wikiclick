# coding=utf-8

from consume import MyKafka
import json
import numpy
import csv
import time
import boto3
import configparser

config = configparser.ConfigParser()
config.read('config.txt')
client = boto3.client('s3', aws_access_key_id=config['aws_s3']['access_key_id'], aws_secret_access_key=config['aws_s3']['secret_access_key'])
response = client.list_buckets()
bucket_name = 'wikiclick'

object_key = 'dataset/2015_01_en_clickstream.tsv'

csv_obj = client.get_object(Bucket=bucket_name, Key=object_key)
body = csv_obj['Body']

class Read():
    def test(self):
        now = int(time.time() * 1000)
#        fd = open('2015_01_en_clickstream.tsv')
        fd = body._raw_stream

        i = 0
        lst =[]
        for data in csv.reader(fd, delimiter='\t'):
            message_info = {
                            'n': data[2],
                            'curr_title': data[4],
                            'date': now + i * 4000
                            }
            lst.append (message_info)
            i += 1
            if i % 1000 == 0:
                mk = MyKafka()
                topic = mk.get_topic()
                message = json.dumps(lst).encode(encoding='utf-8')
                mk.produce_kafka_data(topic,message)
                lst = []

    def test1(self):
        mk = MyKafka()
        topic = mk.get_topic()
        mk.consume_kafka(topic)

if __name__ =='__main__':
    read = Read()
    read.test()
