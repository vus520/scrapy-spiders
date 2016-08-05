#!/bin/sh

rm -f allhl-apps.json
redis-cli flushall
redis-cli lpush allhl:start_urls 'https://play.google.com/store/apps/category/MEDIA_AND_VIDEO'
scrapy crawl allhl
