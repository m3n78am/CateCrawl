# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CatecrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	title = scrapy.Field()


class JdProductItem(scrapy.Item):
	title = scrapy.Field()
	category = scrapy.Field()
