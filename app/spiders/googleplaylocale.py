# -*- coding: utf-8 -*-

import scrapy, io, json

from scrapy_redis.spiders import RedisSpider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.linkextractors import LinkExtractor
from app.items import GoogleItem

class googleplaylocale(RedisSpider):
    name = "allhl"

    allowed_domains = ["play.google.com"]
    rules = [
        Rule(LinkExtractor(allow=("store/apps", )), callback='parse', follow=True),
    ]

    def parse(self, response):
        #发现上架的国家列表
        locale = response.xpath('//link').xpath("@href").re('store/apps/details\?id=(.+&hl=.+)$')
        locale = set(locale)
        for lan in locale:
            yield scrapy.Request("https://play.google.com/store/apps/details?id=%s" % lan, callback=self.parse_app)
        
        #发现相关应用，并将url替换成唯一url
        urls = response.xpath('//a').xpath("@href").re('store/apps/details\?id=(.+)')
        urls = set(urls)
        for pkg in urls:
            yield scrapy.Request("https://play.google.com/store/apps/details?id=%s" % pkg, callback=self.parse)

    def parse_app(self, response):
        item = GoogleItem()
        item['title']  = response.xpath("//div[@class='id-app-title']").xpath("text()").extract()
        item['pkg']    = response.xpath("/html").re(u'data-docid="(.*?)"')[0]
        item['local']  = response.url.split("=")[2]
        item['vcode']  = response.css("[itemprop=softwareVersion]::text").extract()[0].strip()
        item['date']   = response.css("[itemprop=datePublished]::text").extract()[0].strip()
        yield item