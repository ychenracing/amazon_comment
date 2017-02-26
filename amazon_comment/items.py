# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonCommentItem(scrapy.Item):
    """评论item"""
    score = scrapy.Field()
    title = scrapy.Field()
    user = scrapy.Field()
    date = scrapy.Field()
    comment = scrapy.Field()
    amazon_product_id = scrapy.Field()
    support_peoples = scrapy.Field()


class AmazonProductItem(scrapy.Item):
    """商品item"""
    amazon_product_id = scrapy.Field()
    img_url = scrapy.Field()
    detail_url = scrapy.Field()
    title = scrapy.Field()
