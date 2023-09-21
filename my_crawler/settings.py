# Scrapy settings for my_crawler project

BOT_NAME = "my_crawler"

SPIDER_MODULES = ["my_crawler.spiders"]
NEWSPIDER_MODULE = "my_crawler.spiders"

ROBOTSTXT_OBEY = False

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

IMAGES_STORE = './爱看韩漫'

FEEDS = {
    '爱看韩漫.json': {
        'format': 'json',
        'encoding': 'utf8',
        'store_empty': False,
        'fields': None,
        'indent': 4,
        'export_empty_fields': False,
    },
}
