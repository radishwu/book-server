#-*-coding:utf-8-*-
import scrapy
from scrapy import Request
from scrapy.spiders import Spider
from douban_book_spider.items import DoubanBookSpiderItem
from scrapy_splash import SplashRequest
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class DoubanBookTop250Spider(Spider):
    name = 'douban_book'
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    keys = ['作者:', '出版社:', '原作名:', '译者:', '出版年:', '定价:', 'ISBN:']
    infoDic1 = {
        '作者:': 'author',
        '出版社:': 'press',
        '原作名:': 'original_name',
        '译者:': 'translator',
        '出版年:': 'publication_time',
        '定价:': 'pricing',
        'ISBN:': 'isbn'
    }

    def start_requests(self):
        url = 'https://book.douban.com/subject_search?search_text=9787213093302'
        yield SplashRequest(url, self.parse, endpoint='render.html', args={'wait': 0.5}, headers=self.headers)
        # yield Request(url, headers=self.headers)

    def parse(self, response):
        booksUrl = response.xpath('//div[@class="item-root"]/a[@class="cover-link"]/@href').extract()
        for url in booksUrl:
            yield Request(url,
                          callback=self.parse_detail,
                          headers=self.headers)

    def parse_detail(self, response):
        item = DoubanBookSpiderItem()
        item['name'] = response.xpath(
            '//div[@id="wrapper"]/h1/span/text()').extract()[0]
        item['cover'] = response.xpath(
            '//div[@id="mainpic"]/a[@class="nbg"]/@href').extract()[0]
        item['intro'] = response.xpath(
            'string(//div[@class="intro"])').extract()[0].replace(" ",
                                                                  "").replace(
                                                                      "\n", "")
        item['score'] = response.xpath(
            '//strong[@class="ll rating_num "]/text()').extract()[0].replace(
                " ", "")
        info = response.xpath(
            'string(//div[@id="info"])').extract()[0].replace(" ",
                                                              "").splitlines()
        info = [str for str in info if str != '']
        itemKey = ''
        for str in info:
            key = self.get_key(str)
            if key == '':
                if (itemKey != '' and str.find(':') == -1):
                    item[self.infoDic1[itemKey]] += str
                continue
            itemKey = key
            item[self.infoDic1[itemKey]] = str.replace(itemKey, "")
        yield item

    def get_key(self, str):
        for key in self.keys:
            if str.find(key) >= 0:
                return key
        return ''