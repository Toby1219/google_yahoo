# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GoogItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    stock_Value = scrapy.Field()
    time = scrapy.Field()
    previous_close = scrapy.Field()
    day_range = scrapy.Field()
    volume = scrapy.Field()
    market_segment = scrapy.Field()
    info = scrapy.Field()


class YahooItem(scrapy.Item):
    name = scrapy.Field()
    market_price = scrapy.Field()
    market_change = scrapy.Field()
    market_change_percent = scrapy.Field()
    time = scrapy.Field()
    sector = scrapy.Field()
    industry = scrapy.Field()
