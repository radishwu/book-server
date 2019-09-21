import json
import requests
from flask import (Blueprint, request)
from lxml import etree

from book.db import get_db
from book.api_util import BusinessException, response_success

bp = Blueprint('book', __name__, url_prefix='/api/book')

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


@bp.route('/book')
def getBook():
    isbn = request.args.get('isbn', '')
    if (len(isbn)) == 0:
        raise BusinessException('isbn不能为空.', -1)
    url = 'https://book.douban.com/subject_search?search_text=' + isbn
    book = query_from_db(isbn)

    if book is None:
        book = spider_douban_book(url)
        insert_to_db(book)

    return response_success(book)


def spider_douban_book(url):
    response = splash_execute(url)
    response = parse_search_page(response)
    data = parse_detail_page(response)
    return data


def splash_execute(url):
    splash_url = 'http://localhost:8050/render.html'

    response = requests.get(splash_url,
                            params={
                                'url': url,
                                'wait': 2
                            },
                            headers=headers)
    return response


def parse_search_page(response):
    html = etree.HTML(response.content)
    booksUrl = html.xpath(
        '//div[@class="item-root"]/a[@class="cover-link"]/@href')[0]
    detailRes = requests.get(booksUrl, headers=headers)
    return detailRes


def parse_detail_page(response):
    html = etree.HTML(response.content)
    data = {}
    data['name'] = html.xpath('//div[@id="wrapper"]/h1/span/text()')[0]
    data['cover'] = html.xpath('//div[@id="mainpic"]/a[@class="nbg"]/@href')[0]
    data['intro'] = html.xpath('string(//div[@class="intro"])').replace(
        " ", "").replace("\n", "")
    data['score'] = html.xpath(
        '//strong[@class="ll rating_num "]/text()')[0].replace(" ", "")
    info = html.xpath('string(//div[@id="info"])').replace(" ",
                                                           "").splitlines()
    info = [str for str in info if str != '']
    itemKey = ''
    for str in info:
        key = get_key(str)
        if key == '':
            if (itemKey != '' and str.find(':') == -1):
                data[infoDic1[itemKey]] += str
            continue
        itemKey = key
        data[infoDic1[itemKey]] = str.replace(itemKey, "")

    return data


def get_key(str):
    for key in keys:
        if str.find(key) >= 0:
            return key
    return ''


def insert_to_db(data):
    db = get_db()
    db.execute(
        'INSERT INTO book(name,cover,original_name,author,press,translator,publication_time,pricing,isbn,intro,score) VALUES (?,?,?,?,?,?,?,?,?,?,?)',
        (data.get('name', ''), data.get('cover', ''),
         data.get('original_name', ''), data.get(
             'author', ''), data.get('press', ''), data.get('translator', ''),
         data.get('publication_time', ''), data.get('pricing', ''),
         data.get('isbn', ''), data.get('intro', ''), data.get('score', '')))
    db.commit()


def query_from_db(isbn):
    db = get_db()
    book = db.execute(
        'select name,cover,original_name,author,press,translator,publication_time,pricing,isbn,intro,score from book where isbn=?',
        (isbn, )).fetchone()
        
    return book
