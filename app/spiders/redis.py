# -*- coding: utf-8 -*-

import scrapy, io, json

from scrapy_redis.spiders import RedisSpider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.linkextractors import LinkExtractor
from app.items import GoogleItem

class RedisSpider(RedisSpider):
    name = "redis"

    rules = [
        Rule(LinkExtractor(allow=("https://play\.google\.com/store/apps/details\?id=[\w\.]+$", )), callback='parse_app', follow=True),
    ] # CrawlSpider 会根据 rules 规则爬取页面并调用函数进行处理

    def parse_app(self, response):
        item = GoogleItem()
        item['url']    = response.url
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