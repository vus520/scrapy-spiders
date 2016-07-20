# -*- coding: utf-8 -*-

import scrapy, io, json

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.linkextractors import LinkExtractor
from app.items import GoogleItem

class GoogleplaySpider(CrawlSpider):
    name = "googleplay"
    allowed_domains = ["play.google.com"]
    start_urls = [
        'https://play.google.com/store/apps/',
        'https://play.google.com/store/apps/category/TRAVEL_AND_LOCAL'
        'https://play.google.com/store/apps/category/APP_WALLPAPER'
        'https://play.google.com/store/apps/category/PERSONALIZATION'
        'https://play.google.com/store/apps/category/TOOLS'
        'https://play.google.com/store/apps/category/BUSINESS'
        'https://play.google.com/store/apps/category/SHOPPING'
        'https://play.google.com/store/apps/category/HEALTH_AND_FITNESS'
        'https://play.google.com/store/apps/category/TRANSPORTATION'
        'https://play.google.com/store/apps/category/EDUCATION'
        'https://play.google.com/store/apps/category/COMICS'
        'https://play.google.com/store/apps/category/MEDIA_AND_VIDEO'
        'https://play.google.com/store/apps/category/LIBRARIES_AND_DEMO'
    ]
    rules = [
        Rule(LinkExtractor(allow=("https://play\.google\.com/store/apps/details\?id=[\w\.]+$", )), callback='parse_app', follow=True),
    ] # CrawlSpider 会根据 rules 规则爬取页面并调用函数进行处理

    def parse_app(self, response):
        item = GoogleItem()
        item['url']    = response.url
        item['title']    = response.xpath("//div[@class='id-app-title']").xpath("text()").extract()
        item['num']    = response.xpath("//div[@itemprop='numDownloads']").xpath("text()").extract()
        item['cate']   = response.xpath("//span[@itemprop='genre']").xpath("text()").extract()
        item['rate']   = response.xpath("//div[@itemprop='contentRating']").xpath("text()").extract()
        item['desc']   = response.xpath("//div[@class='description']").xpath("text()").extract()
        item['desc']   = "\n".join(item['desc'])
        item['score']  = response.xpath("//div[@class='score']").xpath("text()").extract()
        item['meta']   = response.xpath("//meta[@name='description']").xpath("@content").extract()
        item['pkg']    = response.xpath("/html").re(u'data-docid="(.*?)"')[0]

        item['info'] = dict()
        title = response.css('.details-section.metadata').css(".title::text").extract()
        content = response.css('.details-section.metadata').css(".content::text").extract()

        for i, t in enumerate(title):
            item['info'][t.strip()] = content[i].strip()

        #发现相关应用，并将url替换成唯一url
        urls = response.xpath('//a').xpath("@href").re('store/apps/details\?id=([\w\.]+)')
        urls = set(urls)
        for pkg in urls:
            yield scrapy.Request("https://play.google.com/store/apps/details?id=%s" % pkg, callback=self.parse_app)

        yield item

# extract_first
# http://doc.scrapy.org/en/latest/topics/selectors.html