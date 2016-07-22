# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs


class AppPipeline(object):
    def process_item(self, item, spider):
        return item


class GoogleplayPipeline(object):
    def __init__(self):
        self.file = codecs.open('apps.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item))
        line = line.replace("\r", "").replace("\n", "").replace("\t", "").replace("'", "")
        line = line + "\n"
        line = line.decode('unicode_escape')
        self.file.write(line)
        return item