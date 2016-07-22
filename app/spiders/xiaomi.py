# -*- coding: utf-8 -*-

import scrapy, io, json

from scrapy_redis.spiders import RedisSpider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from app.items import GoogleItem

class WandoujiaSpider(RedisSpider):
    name = "xiaomi"

    start_urls = [
        'http://app.xiaomi.com/topList'
    ]

    allowed_domains = ["app.xiaomi.com"]
    rules = []

    def parse(self, response):
        urls = response.xpath('//a').xpath("@href").re('category/([\d_]+)$')
        urls = set(urls)
        for cid in urls:
            for page in range(0, 10):
                yield scrapy.Request("http://app.xiaomi.com/categotyAllListApi?page=%s&categoryId=%s&pageSize=2000" % (page, cid), callback=self.parse)

        if response.body[0] == u"{":
            data = json.loads(response.body)
            for row in data['data']:
                yield scrapy.Request("http://app.xiaomi.com/details?id=%s" % row['packageName'], callback=self.parse_app)

    def parse_app(self, response):
        item = GoogleItem()
        item['url']    = response.url
        item['title']  = response.css('.intro-titles h3::text').extract()
        item['num']    = 0
        item['rate']   = response.css('span.app-intro-comment::text').extract()
        item['cate']   = response.css('.bread-crumb li a::text')[1].extract()
        item['tag']    = ''

        item['desc']   = response.css('.pslide::text').extract()
        item['desc']   = "\n".join(item['desc']).strip().replace(" ", "").replace("\n", "").replace("\r", "")

        item['info'] = dict()
        item['info']['大小'] = response.xpath("/html").re(u'<li class="weight-font">软件大小.*?</li><li>([^<]+)<')
        item['info']['更新'] = response.xpath("/html").re(u'<li class="weight-font">更新时间.*?</li><li>([^<]+)<')
        item['info']['厂商'] = response.xpath("/html").re(u'<b>开发者：</b>\s+<span>([^<]+)<')

        yield item