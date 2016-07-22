# -*- coding: utf-8 -*-

import scrapy, io, json, codecs

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
        item['title']  = response.xpath("//div[@class='id-app-title']").xpath("text()").extract()
        item['title']  = ''.join(item['title']).replace('\n', '').replace('\r', '').replace('\t', '')
        item['num']    = response.xpath("//div[@itemprop='numDownloads']").xpath("text()").extract()
        item['cate']   = response.xpath("//span[@itemprop='genre']").xpath("text()").extract()
        item['cate']   = ''.join(item['cate']).replace(' ', '').replace('\n', '').replace('\r', '').replace('\t', '')
        item['rate']   = response.xpath("//div[@itemprop='contentRating']").xpath("text()").extract()
        item['rate']  = ''.join(item['rate']).replace('\n', '').replace('\r', '').replace('\t', '')
        item['desc']   = response.xpath("//div[@class='description']").xpath("text()").extract()
        item['desc']   = ''.join(item['desc']).replace(' ', '').replace('\n', '').replace('\r', '').replace('\t', '')
        item['score']  = response.xpath("//div[@class='score']").xpath("text()").extract()
        item['meta']   = response.xpath("//meta[@name='description']").xpath("@content").extract()
        item['meta']   = ''.join(item['meta']).replace(' ', '').replace('\n', '').replace('\r', '').replace('\t', '')
        item['pkg']    = response.xpath("/html").re(u'data-docid="(.*?)"')[0]

        item['info'] = dict()
        title = response.css('.details-section.metadata').css(".title::text").extract()
        content = response.css('.details-section.metadata').css(".content::text").extract()

        for i, t in enumerate(title):
            key = ''.join(t.strip()).replace('\t', '').replace('\r', '').replace('\n', '').replace(' ', '')
            value = ''.join(content[i].strip()).replace('\t', '').replace('\r', '').replace('\n', '')
            # item['info'][key] = value
            if key == '安装次数'.decode('utf-8'):
                item['info']['install_num'] = value
            elif key == '内容分级'.decode('utf-8'):
                item['info']['content_level'] = value
            elif key == '大小'.decode('utf-8'):
                item['info']['size'] = value
            elif key == '提供者：'.decode('utf-8'):
                item['info']['provider'] = value
            elif key == 'Android系统版本要求'.decode('utf-8'):
                item['info']['android_level_requirement'] = value
            elif key == '当前版本'.decode('utf-8'):
                item['info']['current_version'] = value
            elif key == '开发者'.decode('utf-8'):
                item['info']['developer'] = value
            elif key == '更新日期'.decode('utf-8'):
                item['info']['update_time'] = value
            elif key == '权限'.decode('utf-8'):
                item['info']['auth'] = value
            elif key == '举报'.decode('utf-8'):
                item['info']['report'] = value

        #发现相关应用，并将url替换成唯一url
        urls = response.xpath('//a').xpath("@href").re('store/apps/details\?id=([\w\.]+)')
        urls = set(urls)
        for pkg in urls:
            yield scrapy.Request("https://play.google.com/store/apps/details?id=%s" % pkg, callback=self.parse_app)

        yield item

# extract_first
# http://doc.scrapy.org/en/latest/topics/selectors.html