# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from jieba.analyse import *
import pymysql
from kafka import KafkaProducer

#ZhaopingPipeline:定义保存在本地关系型数据库中
class ZhaopingPipeline(object):
    def open_spider(self,spider):
        self.conn = pymysql.connect(host = 'localhost',user = 'root',password = '123',db = 'python3',charset = 'utf8')


    def close_spider(self,spider):
        self.conn.close()

    def process_item(self, item, spider):
        sql = "insert into job(zwmc,gsmc,zwyx,gzdd,gwyq,words) VALUES (%s,%s,%s,%s,%s,%s)"
        c = self.conn.cursor()
        words = ' '.join(list(item['keywords']))
        c.execute(sql,(item['zwmc'],item['gsmc'],item['zwyx'],item['gzdd'],item['zwyq'],words))
        self.conn.commit()
        print()
        return item


#ZhaopingKafukaPipeline：定义保存在kafaka中
# class ZhaopingKafukaPipeline(object):
#     def open_spider(self,spider):
#         self.producer = KafkaProducer(bootstrap_servers = '192.168.161.131:9092')
#     def close_spider(self,spider):
#         self.producer.close()
#
#     def process_item(self, item, spider):
#         msg = '{zwmc},{gsmc},{zwyx},{gzdd},{zwyq},{keywords}'.format(zwmc = item["zwmc"],gsmc = item['gsmc'],zwyx = ['zwyx'],gzdd = item['gzdd'],zwyq=item['zwyq'],keywords=item['keywords'])
#         self.producer.send('job',msg.encode())
#         return item

#ZhaopingFenCiPipeline：将爬取到的结果分词进行保存结果在本地
class ZhaopingFenCiPipeline(object):
    def process_item(self, item, spider):
        #分词处理
        keywords = extract_tags(item['zwyq'],topK=1000)
        #unkeywords 去掉重复的词
        unkeywords = set(keywords)
        #unkeywords 遍历所有字段，区别大小写
        unkeywords = {key.lower() for key in unkeywords}
        likeskeys = {
            'python',
            'java',
            'html',
            'css',
            'jquery',
            'sql',
            '数据库',
            'hadoop',
            'hive',
            'hbase',
            'flume',
            'kafka',
            'spark',
            'mapreduce',
            'fink',
            'flask',
            'django',
            'nosql',
            'mongodb',
            'zookeeper',
            '大数据'
        }
#         #将unkeywords与likeskeys进行交集
        item['keywords'] = unkeywords & likeskeys
        return item

