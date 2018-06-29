# coding=utf-8
from pykafka import KafkaClient
import pymysql
import json


class MyKafka():

    def get_topic(self):
        #For your local machine:
        # client = KafkaClient(hosts="spark237:9092,spark172:9092,spark235:9092,spark61:9092")        
        client = KafkaClient(hosts="34.233.31.237:9092,52.21.74.235:9092,52.4.161.61:9092,34.199.82.172:9092")
        return client.topics[b"test"]

    # producer
    def produce_kafka_data(self, kafka_topic, message):
        with kafka_topic.get_sync_producer() as producer:
            producer.produce(message)
        print("product success")


    def consume_kafka(self, kafka_topic):
        balanced_consumer = kafka_topic.get_balanced_consumer(
        consumer_group=b"testgroup",
        auto_commit_enable=True,
        zookeeper_connect='34.233.31.237:2181,34.199.82.172:2181,52.21.74.235:2181,52.4.161.61:2181',
        zookeeper_connection_timeout_ms=6000,
        consumer_timeout_ms=10000, )


        db= pymysql.connect(host="sqlforwiki.carf1itkjlds.us-east-1.rds.amazonaws.com",user="wikiclick",
                    password="wikiclick",db="wikiclick",port=3306)
        
        cur = db.cursor()
        
        for message in balanced_consumer:
            dt = json.loads(message.value)
            sql_insert ="""insert into intime(curr_title, time, n) values """
            for e in dt:
                sql_insert += '("%s", %d, %d),' % (e['curr_title'], e['date'], int(e['n']))
            
            sql_insert = sql_insert[:len(sql_insert)-1]
            try:
                res = cur.execute(sql_insert)
                db.commit()
                print('save success', res)
            except Exception as e:
                db.rollback()
                print(e)


    def consume_data(self, consume):
        for message in consume:
            if message is not None:
                print(message.offset, message.value)
        print("consumer success")

    
#consumer
    def consumer(self, topic):
        consumer = topic.get_simple_consumer()
        for message in consumer:
            try:
                if message is not None:
                    print(message.offset, message.value)
            except:
                print("error")
                

if __name__ == '__main__':
    myKafka = MyKafka()
    topic = myKafka.get_topic()
    myKafka.consume_kafka(topic)
