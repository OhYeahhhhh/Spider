# -*- coding: utf-8 -*-
import scrapy
from mySpider.items import MovieItem

class ItcastSpider(scrapy.Spider):
    name = 'itcast'
    #allowed_domains = ['itcast.cn']
    start_urls = ['https://movie.douban.com/top250']
    i=1

    def parse(self, response):
        item=MovieItem()
        movies=response.xpath('//*[@id="content"]/div/div[1]/ol/li')
        for movie in movies:
            item["id"]=self.i
            self.i+=1
            item["name"]=movie.xpath('div/div[2]/div[1]/a/span[1]/text()').extract_first()
            item["score"]=movie.xpath('div/div[2]/div[2]/div/span[2]/text()').extract_first()
            yield item
        nextPage=response.xpath('//*[@id="content"]/div/div[1]/div[2]/span[3]/a/@href').extract_first()
        if nextPage:
            yield scrapy.Request(url = self.start_urls[0]+nextPage,callback = self.parse)