 # -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanBookSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 书名
    name = scrapy.Field()
    # 封面
    cover = scrapy.Field()
    # 原作名
    original_name = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 出版社
    press = scrapy.Field()
    # 译者
    translator = scrapy.Field()
    # 出版时间
    publication_time = scrapy.Field()
    # 定价
    pricing = scrapy.Field()
    # ISBN
    isbn = scrapy.Field()
    # 内容简介
    intro = scrapy.Field()
    # 评分
    score = scrapy.Field()
