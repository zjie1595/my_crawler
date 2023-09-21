# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MangaItem(scrapy.Item):
    title = scrapy.Field()
    cover_image_url = scrapy.Field()
    alias = scrapy.Field()
    author = scrapy.Field()
    status = scrapy.Field()
    region = scrapy.Field()
    tags = scrapy.Field()
    description = scrapy.Field()
    chapters = scrapy.Field()
