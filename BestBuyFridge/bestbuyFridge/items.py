# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class bestbuyFridgeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
  brand = scrapy.Field()
  product_description = scrapy.Field()
  total_capacity = scrapy.Field()
  freezer_capacity = scrapy.Field()
  price = scrapy.Field()
  ratings = scrapy.Field()
  number_of_reviews = scrapy.Field()

