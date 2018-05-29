# -*- coding: utf-8 -*-
import scrapy
import re
from zhaoping.items import *
from kafka import KafkaProducer

class JobSpider(scrapy.Spider):
    count = 0
    name = 'job'
    start_urls = ['http://sou.zhaopin.com/jobs/searchresult.ashx?'
                  'jl=%E5%8C%97%E4%BA%AC&kw=%E5%BC%80%E5%8F%91&sm=0&p=1']

    def parse(self, response):
        #实现
            #1找到职位名称并进行跟踪
            #2找到页面中的写一页跟踪

        #zwmc:得到所有职位链接对象
        zwmcs = response.css("td.zwmc")
        for zwmc in zwmcs:
            #href 所有链接地址
            href = zwmc.css('a::attr("href")').extract_first()
            #follow() href:要继续解析的链接地址，deatil:函数名称
            yield response.follow(href,self.deatil)
        next_href = response.css("ul > li.pagesDown-pos > a::attr('href')").extract_first()
        if next_href is not None:
            if self.count <1:
                self.count+=1
                yield response.follow(next_href,self.parse)

        # ::text ：获得文本内容
        # ::arrt("href"): 得到链接地址

    def deatil(self,response):
        p = '<[^>]+>'
        zwmc = response.css("div.inner-left.fl > h1::text").extract_first()
        gsmc = response.css("div.inner-left.fl > h2 > a::text").extract_first()
        zwyx = response.css("div.terminalpage-left > ul > li:nth-child(1) > strong::text").extract_first()
        gzdd = response.css("div.terminalpage-left > ul > li:nth-child(2) > strong").extract_first()
        gzdd = re.subn(p,'',gzdd)[0]
        zwyq = response.css("div.terminalpage-main.clearfix  div.tab-inner-cont").extract_first()
        zwyq = re.subn(p, '', zwyq)[0]
        zwyq = re.subn('\s+|n','',zwyq)[0]
        item = ZhaopingItem()
        item["zwmc"]=zwmc
        item["gsmc"]=gsmc
        item["gzdd"]=gzdd
        item["zwyq"]=zwyq
        item["zwyx"]=zwyx
        #print(type(item['zwyx']))
        yield item