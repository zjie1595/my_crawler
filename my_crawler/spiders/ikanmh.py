import scrapy

from my_crawler.items import MangaItem


# 爱看韩漫
class IkanmhSpider(scrapy.Spider):
    name = "ikanmh"
    base_url = 'http://wxzmh.top'
    start_urls = [f'{base_url}/booklist?page=1']

    # 解析开始页，寻找总页数
    def parse(self, response):
        # 找出最后一页的页码
        last_page = int(response.xpath('//div[@class="pagination"]/li[last()-1]/a/text()').get())
        for page in range(1, last_page + 1):
            page_url = f'{self.base_url}/booklist?page={page}'
            yield scrapy.Request(page_url, callback=self.page)

    # 解析目录页
    def page(self, response):
        for href in response.xpath('//div[@class="mh-item-detali"]/h2/a/@href').extract():
            detail_page_url = response.urljoin(href)
            yield scrapy.Request(detail_page_url, callback=self.detail)

    # 解析详情页
    def detail(self, response):
        item = MangaItem()
        manga_title = response.xpath('//div[@class="info"]/h1/text()').get().strip()
        item['title'] = manga_title
        item['cover_image_url'] = response.xpath('//div[@class="cover"]/img/@src').get()
        item['alias'] = response.xpath('//p[@class="subtitle"][contains(text(), "别名")]/text()').get().split('：')[1]
        item['author'] = response.xpath('//p[@class="subtitle"][contains(text(), "作者")]/text()').get().split('：')[1]
        item['status'] = response.xpath('//span[contains(text(),"状态")]/span/text()').get().strip()
        item['region'] = response.xpath('//span[contains(text(),"地区")]/a/text()').get().strip()
        item['tags'] = response.xpath('//span[contains(text(),"标签")]/a/text()').getall()
        item['description'] = response.xpath('//p[@class="content"]/text()').get().strip()
        item['chapters'] = []
        for a in response.xpath('//div[@id="chapterlistload"]/ul/li/a'):
            chapter_page_url = response.urljoin(a.xpath('@href').get())
            title = a.xpath('text()').get()
            yield scrapy.Request(chapter_page_url, callback=self.chapter,
                                 meta={'item': item, 'title': title})

    # 解析阅读页
    def chapter(self, response):
        item = response.meta['item']
        chapter_title = response.meta['title']
        if '<' in chapter_title and '>' in chapter_title:
            chapter_title = chapter_title[:chapter_title.rfind('<')]
        chapters = item['chapters']
        chapter = {
            'title': chapter_title,
            'image_url_list': response.xpath('//img[@class="lazy"]/@data-original').getall(),
        }
        chapters.append(chapter)
        yield item
