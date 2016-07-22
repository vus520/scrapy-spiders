# -*- coding: utf-8 -*-

import scrapy, io, json

from scrapy_redis.spiders import RedisSpider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from app.items import GoogleItem

class WandoujiaSpider(RedisSpider):
#class GoogleplaySpider(CrawlSpider):
    name = "wandou"

    start_urls = [
        'http://www.wandoujia.com/category/408'
    ]

    allowed_domains = ["www.wandoujia.com"]
    rules = [
        Rule(LinkExtractor(allow=("http://www.wandoujia.com/apps/com/apps/([a-z]+\.[\w\.]+)$", )),
            callback='parse',
            follow=True),

        Rule(LinkExtractor(allow=("http://www.wandoujia.com/category/[\d_]+$", )),
            callback='parse',
            follow=True),

        Rule(LinkExtractor(allow=("http://www.wandoujia.com/tag/[\d]+$", )),
            callback='parse',
            follow=True),

        Rule(LinkExtractor(allow=("http://www.wandoujia.com/tag/[\d]+_page[\d]+$", )),
            callback='parse',
            follow=True),
    ]

    def parse_category(self, response):
        urls = response.xpath('//a').xpath("@href").re('category/[\d_]+$')
        urls = set(urls)
        for pkg in urls:
            yield scrapy.Request("http://www.wandoujia.com/%s" % pkg, callback=self.parse_category)

        urls = response.xpath('//a').xpath("@href").re('com/apps/([a-z]+\.[\w\.]+)')
        urls = set(urls)
        for pkg in urls:
            yield scrapy.Request("http://www.wandoujia.com/apps/%s" % pkg, callback=self.parse_app)

    def parse(self, response):
        urls = response.xpath('//a').xpath("@href").re("http://www.wandoujia.com/((category/[\d\w_]+)|(tag/[\d\w_]+))")
        urls = set(urls)
        for pkg in urls:
            yield scrapy.Request("http://www.wandoujia.com/%s" % pkg, callback=self.parse_category)

        urls = response.xpath('//a').xpath("@href").re('com/apps/([a-z]+\.[\w\.]+)')
        urls = set(urls)
        for pkg in urls:
            yield scrapy.Request("http://www.wandoujia.com/apps/%s" % pkg, callback=self.parse_app)

    def parse_app(self, response):
        item = GoogleItem()
        item['url']    = response.url
        item['title']  = response.xpath('//span[@class="title"]').xpath("text()").extract()
        item['num']    = response.xpath("/html").re(u'UserDownloads:(\d+)')
        item['rate']   = response.xpath("/html").re(u'data-like="(\d+)"')

        item['cate']   = response.xpath("//dd[@class='tag-box']").css("a::text").extract()
        item['cate']   = map(unicode.strip, item['cate'])

        item['tag']    = response.css('div.side-tags a::text').extract()
        item['tag']    = map(unicode.strip, item['tag'])

        item['info'] = dict()
        item['info']['大小'] = response.xpath("/html").re(u'<dt>大小</dt>\s+<dd>\s+([\d\.\w]+)')
        item['info']['更新'] = response.css("#baidu_time::text").extract()
        item['info']['厂商'] = response.css("a.dev-sites span::text").extract()
        item['info']['要求'] = response.css("dd.perms::text")[0].extract().strip().replace(" ", "").replace("\n", "")

        yield item