# -*- coding: utf-8 -*-

import scrapy

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.linkextractors import LinkExtractor
from app.items import GoogleItem

class GoogleplaySpider(CrawlSpider):
    name = "googleplay"
    allowed_domains = ["play.google.com"]
    start_urls = [
        'https://play.google.com/store/apps/',
        'https://play.google.com/store/apps/details?id=com.viber.voip'
    ]
    rules = [
        Rule(LinkExtractor(allow=("https://play\.google\.com/store/apps/details", )), callback='parse_app', follow=True),
    ] # CrawlSpider 会根据 rules 规则爬取页面并调用函数进行处理


    def parse_app(self, response):
        item = GoogleItem()
        item['url']    = response.url
        item['num']    = response.xpath("//div[@itemprop='numDownloads']").xpath("text()").extract()
        item['cate']   = response.xpath("//span[@itemprop='genre']").xpath("text()").extract()
        item['rate']   = response.xpath("//div[@itemprop='contentRating']").xpath("text()").extract()
        item['desc']   = response.xpath("//div[@class='description']").xpath("text()").extract()
        item['score']  = response.xpath("//div[@class='score']").xpath("text()").extract()
        item['meta']   = response.xpath("//meta[@name='description']").xpath("@content").extract()
        item['info']   = response.xpath("//div").re(u'<div class="title">([^<]+)</div>\s*?<div class="content">([^<]+)</div>')
        yield item

# extract_first
# http://doc.scrapy.org/en/latest/topics/selectors.html