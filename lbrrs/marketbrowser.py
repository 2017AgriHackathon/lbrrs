#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import abc
import requests
import re
import logging
import urllib.parse as urlparse
from lxml import html
from logging.config import fileConfig
from pathos.pools import _ThreadPool
from pathos.multiprocessing import cpu_count
from .database.model import Product, Price
from . import _logging_config_path
from .directory import Directory


fileConfig(_logging_config_path)
log = logging.getLogger(__name__)


class MarketBrowser(Directory):
    """Get all urls from products page with abstract method get_product_urls,
    and browse each product with get_product_price method for getting Product
    and Price instance and do further with Directory methods"""
    __metaclass__ = abc.ABCMeta

    @abc.abstractstaticmethod
    def get_product_urls(self):
        return

    @abc.abstractmethod
    def get_product_price(self):
        return

    def config_generator(self):
        for config in self.configs:
            log.info(MarketBrowser.INFO_MAP[0] % (self.market.name, config.name))
            urls = []
            try:
                map_strs = self.PRODUCT_MAP[config.name]
                for map_str in map_strs:
                    urls += self.get_product_urls(map_str)
                yield config, urls
            except KeyError:
                log.error(Directory.ERROR_MAP[1] % config.name)

    def direct(self):

        def browse_each(config, url):
            product, price = self.get_product_price(url)
            if not product and not price:
                return

            # return self if not exists
            product = self.check_product(product)

            # set config_id for future re-classify
            product.config_id = config.id

            if not product.id:
                Directory.STACK.append((config, product, price))
            elif product.part_id:
                price.product = product
                self.set_price(price)
            return

        cpu = cpu_count()
        pool = _ThreadPool(cpu)
        for c, urls in self.config_generator():
            for u in urls:
                pool.apply_async(browse_each, args=(c, u))
        pool.close()
        pool.join()

    @staticmethod
    def get_html(url):
        try:
            res = requests.get(url, timeout=30)
            parsed_page = html.fromstring(res.content)
        except requests.exceptions.Timeout:
            log.error(Directory.ERROR_MAP[4] % url)
            return html.Element('html')
        except:
            return html.Element('html')

        return parsed_page


class WellcomeBrowser(MarketBrowser):

    NAME = '頂好'

    PRODUCTS_ROUTE = 'https://sbd-ec.wellcome.com.tw/product/listByCategory/%s?max=100&query=%s&sort=viewCount&offset=%s'
    INDEX_ROUTE = 'https://sbd-ec.wellcome.com.tw'

    # 米
    # 麵
    # 罐頭 (泡菜、玉米、鳳梨、鮪魚)
    # 咖哩、粉、香料
    # 醬

    # 起司、奶油
    # 牛奶、蛋
    # 蒟蒻、香腸等、豆腐、糕類
    # 沙拉

    PRODUCT_MAP = {
        '常溫商品': [(31, 37),
                 (31, 40),
                 (31, 42), (31, 43),
                 (31, 34),
                 (33, 41), (31, 32),
                 (31, 33)],
        '冷藏商品': [(96, 97), (96, 98),
                 (103, 104), (113, 114),
                 (108, 109), (108, 110), (108, 111), (108, 112)],
        '冷凍商品': [(82, 83), (82, 86), (87, 88)],
        '海鮮': [(20, 21), (20, 22), (20, 23), (20, 24)],
        '牛肉': [(12, 15), (12, 18)],
        '雞肉': [(12, 13)], '豬肉': [(12, 14), (12, 17)],
        '雜貨': [(31, 35)], '蔬菜': [(7, 8), (7, 9), (7, 10)],
        '水果': [(2, 4), (2, 6)]
    }

    NAME_RE = re.compile('''
            (?:.+?)(?=[0-9]+)
    ''', re.X)

    def __init__(self):
        super(WellcomeBrowser, self).__init__()

    @staticmethod
    def get_product_urls(map_str):

        offsets = [0, 100]
        results = []

        for offset in offsets:

            url = WellcomeBrowser.PRODUCTS_ROUTE % (map_str[0], map_str[1], offset)
            page = MarketBrowser.get_html(url)
            urls = page.xpath('//div[@class="item-name"]/a/@href')
            results += [WellcomeBrowser.INDEX_ROUTE + url for url in set(urls)]

        return results

    def get_product_price(self, url):

        page = MarketBrowser.get_html(url)

        xpath = Directory.flat_xpath

        name_str = xpath(page, '//div[@class="product-name"]/text()')

        spec_str = xpath(page, '//ul[@class="product-list"]/li[3]/text()')

        origin_str = xpath(page, '//ul[@class="product-list"]/li[2]/text()')

        price_str = xpath(page, '//span[@class="item-price"]/text()')

        try:
            # 紅蘿蔔3入/袋 => 紅蘿蔔
            name = WellcomeBrowser.NAME_RE.findall(name_str)[0]

            # 規格摘要：300g => 300
            weight = self.get_weight(spec_str)

            # 規格摘要: 3入/袋 => 3
            count = 1
            if not weight:
                count = self.get_count(spec_str)

            # product/view/3001 => 3001
            pid = Directory.NUM_RE.findall(url)[-1]

            # 產地：台灣 => Origin(name='臺灣')
            origin = self.get_origin(origin_str)

            # '$69' => 69
            price = int(price_str)

            # try to find unit in spec and title
            unit = self.get_unit(name_str + spec_str)

        except:
            log.error(Directory.ERROR_MAP[3] % (name_str, url))
            return None, None

        product = Product(source=url,
                          name=name,
                          origin=origin,
                          market_id=self.market.id,
                          pid=pid,
                          weight=weight,
                          count=count,
                          unit=unit)

        price = Price(price=price, date=self.date)

        return product, price


class GeantBrowser(MarketBrowser):

    NAME = '愛買'

    PRODUCTS_ROUTE = 'http://www.gohappy.com.tw/shopping/Browse.do?op=vc&cid=%s&sid=12'
    INDEX_ROUTE = 'http://www.gohappy.com.tw'

    # 米
    # 麵
    # 罐頭 (泡菜、玉米、鳳梨、鮪魚、高湯)
    # 咖哩
    # 粉、香料
    # 鹹醬
    # 甜醬

    # 起司、奶油
    # 牛奶、蛋
    # 蒟蒻、香腸等、豆腐、糕類
    # 沙拉味增

    PRODUCT_MAP = {
        '常溫商品': [296465,
                 291776,
                 5008, 934, 297075, 296531, 29703, 300529, 296563,
                 293897,
                 296568,
                 296297, 307858, 247, 29689, 1448, 7322, 297059, 29031, 297068,
                 35593, 19402],
        '冷藏商品': [156695, 161465, 296293,
                 161464,
                 301327, 301328, 301326, 40760, 161724, 161720,
                 297029, 161762],
        '海鮮': [210977, 210975, 329840, 329839, 329870, 329868, 329883],
        '冷凍商品': [84657, 12583, 162218],
        '牛肉': [215205],
        '雞肉': [301299], '豬肉': [212375],
        '雜貨': [295095], '蔬菜': [29979, 358367, '161460&cp=1', '161460&cp=2', 215204, 161755],
        '水果': [208879]
    }

    NAME_RE = re.compile('''
        (?:.+?)(?=[0-9]+.*|$)
    ''', re.X)

    ORIGIN_RE = re.compile('''
        (?<=產地：)(.*?)\W
    ''', re.X)

    COUNT_RE = re.compile('''
        (?<=數量：)(.*?)\W
    ''', re.X)

    WEIGHT_RE = re.compile('''
        (?<=規格：)(.*?)\W
    ''', re.X)

    def __init__(self):
        super(GeantBrowser, self).__init__()

    @staticmethod
    def get_product_urls(map_str):
        url = GeantBrowser.PRODUCTS_ROUTE % (map_str)
        page = MarketBrowser.get_html(url)
        urls = page.xpath('//ul[@class="product_list"]//h5/a/@href')
        return [GeantBrowser.INDEX_ROUTE + url for url in set(urls)]

    def get_product_price(self, url):

        page = MarketBrowser.get_html(url)

        xpath = Directory.flat_xpath

        name_str = xpath(page, '//h3[@class="trade_Name"]/text()')

        intro_str = xpath(page, '//dd[@class="introduction"]/text()')

        content_origin_str = xpath(page, '//div[@class="product_content"]//tr[contains(string(), "產地")]/td[2]//text()')

        content_unit_str = xpath(page, '//div[@class="product_content"]//tr[contains(string(), "數量")]/td[2]//text()')

        price_str = xpath(page, '//dd[@class="list_price"]/text()')

        try:

            # 大成去骨雞腿1盒 => 大成去骨雞腿
            name = GeantBrowser.NAME_RE.findall(name_str)[0]

            # try to find origin in introduction
            try:
                origin_str = GeantBrowser.ORIGIN_RE.findall(intro_str)[0]

            # try content table, could be ''
            except IndexError:
                origin_str = content_origin_str

            origin = self.get_origin(origin_str)

            # try to find count in introduction
            try:
                count_str = GeantBrowser.COUNT_RE.findall(intro_str)[0]
                count = Directory.get_count(count_str)

            # try to find count in title, or 1
            except IndexError:
                count = Directory.get_count(name_str)

            # try to find spec in introduction
            try:
                spec_str = GeantBrowser.WEIGHT_RE.findall(intro_str)[0]
                weight = self.get_weight(spec_str)

                # test weight with title weight
                test_weight = self.get_weight(name_str)
                if test_weight and weight != test_weight:
                    weight = test_weight

            # try to find spec in title
            except IndexError:
                weight = self.get_weight(name_str)

            # &pid=4940444 => 4940444
            pid = urlparse.parse_qs(url)['pid'][0]

            price = int(price_str)

            # try to find unit in title, introduction, content table
            try:
                unit_str = GeantBrowser.COUNT_RE.findall(intro_str)[0]
                unit_str += name_str
                unit_str += content_unit_str
            except IndexError:
                unit_str = name_str + content_unit_str

            unit = self.get_unit(unit_str)

        except:
            log.error(Directory.ERROR_MAP[3] % (name_str, url))
            return None, None

        product = Product(source=url,
                          name=name,
                          origin=origin,
                          market_id=self.market.id,
                          pid=pid,
                          weight=weight,
                          count=count,
                          unit=unit)

        price = Price(price=price, date=self.date)

        return product, price


class FengKangBrowser(MarketBrowser):

    NAME = '楓康'

    PRODUCTS_ROUTE = 'http://shop.supermarket.com.tw/Shop_ProductList.html?c0=%s&c1=%s&c2=%s&page=%s'
    INDEX_ROUTE = 'http://shop.supermarket.com.tw'

    # 米
    # 麵
    # 罐頭、咖哩
    # 粉、香料
    # 鹹醬
    # 甜醬

    # 起司、奶油
    # 牛奶、蛋
    # 蒟蒻、香腸等、豆腐、糕類
    # 沙拉味增

    PRODUCT_MAP = {
        '常溫商品': [(0, 153, 236, 1),
                 (0, 153, 245, 1), (0, 153, 387, 1),
                 (0, 154, 246, 1), (0, 154, 268, 1), (0, 154, 384, 1), (0, 154, 260, 1),
                 (0, 153, 358, 1), (0, 154, 250, 1), (0, 154, 252, 1),
                 (0, 154, 267, 1), (0, 154, 256, 1), (0, 154, 262, 1), (0, 154, 264, 1), (0, 154, 258, 1), (0, 154, 267, 1), (0, 157, 307, 1),
                 (0, 154, 254, 1)],
        '冷藏商品': [(1, 157, 305, 1), (0, 154, 254, 1),
                 (1, 158, 312, 1),
                 (1, 157, 303, 1), (1, 157, 304, 1), (1, 157, 310, 1),
                 (1, 157, 306, 1), (1, 157, 309, 1)],
        '海鮮': [(1, 364, 347, 1), (1, 364, 368, 1), (2, 165, 514, 1), (2, 165, 316, 1), (2, 165, 348, 1),
               (2, 165, 349, 1), (2, 165, 359, 1)],
        '牛肉': [(1, 160, 328, 1), (2, 167, 354, 1), (2, 167, 355, 1)],
        '羊肉': [(2, 167, 354, 1), (2, 167, 355, 1)],
        '冷凍商品': [(0, 161, 382, 1),
                 (2, 163, 336, 1)],
        '雞肉': [(1, 160, 330, 1), (1, 160, 330, 2)],
        '豬肉': [(1, 160, 331, 1), (1, 160, 330, 2)],
        '蔬菜': [(1, 159, 324, 1), (1, 159, 324, 2), (1, 159, 462, 1), (1, 159, 462, 2), (1, 159, 319, 1), (1, 159, 319, 2)],
        '水果': [(1, 365, 320, 1), (1, 365, 320, 2)],
        '雜貨': [(0, 153, 357, 1)],

    }

    NAME_RE = re.compile('''
        (?:.+?)(?=[0-9]+.*|約.*|$)
    ''', re.X)

    PID_RE = re.compile('''
        p-(.+)(?=.html)
    ''', re.X)

    ORIGIN_RE = re.compile('''
        (?<=產　　地：)(.*)
    ''', re.X)

    UNIT_RE = re.compile('''
        (?<=包　　裝：)(.*)
    ''', re.X)

    def __init__(self):
        super(FengKangBrowser, self).__init__()

    @staticmethod
    def get_product_urls(map_str):
        url = FengKangBrowser.PRODUCTS_ROUTE % (map_str[0], map_str[1], map_str[2], map_str[3])
        page = MarketBrowser.get_html(url)
        urls = page.xpath('//div[@class="lisa3 lisa3-2"]//div[@class="t2"]/a/@href')
        return [FengKangBrowser.INDEX_ROUTE + url for url in set(urls)]

    def get_product_price(self, url):

        page = MarketBrowser.get_html(url)

        xpath = Directory.flat_xpath

        name_str = xpath(page, '//div[@class="vw"]/div[@class="tt21"]/text()')

        price_str = xpath(page, '//div[@class="vw"]/div[@class="tt23"]//h4/text()')

        origin_str = xpath(page, '//div[@id="tab1"]/div[contains(string(), "產　　地：")]/text()')

        unit_str = xpath(page, '//div[@id="tab1"]/div[contains(string(), "包　　裝：")]/text()')

        try:
            # 胡蘿蔔/約500g => 胡蘿蔔
            name = FengKangBrowser.NAME_RE.findall(name_str)[0]

            # try to find weight in title, could be null
            weight = self.get_weight(name_str)

            # 胡蘿蔔-Shop-6738.html => 6738
            pid = FengKangBrowser.PID_RE.findall(url)[0]

            # try to find origin in introduction
            try:
                origin_str = FengKangBrowser.ORIGIN_RE.findall(origin_str)[0]

            # try to find origin in title
            except IndexError:
                origin_str = name_str

            origin = self.get_origin(origin_str)

            count = self.get_count(name_str)

            price = int(price_str)

            # try to find unit in title and introduction
            unit = self.get_unit(name_str + unit_str)

        except:
            log.error(Directory.ERROR_MAP[3] % (name_str, url))
            return None, None

        product = Product(source=url,
                          name=name,
                          origin=origin,
                          market_id=self.market.id,
                          pid=pid,
                          weight=weight,
                          count=count,
                          unit=unit)

        price = Price(price=price, date=self.date)

        return product, price


class RtmartBrowser(MarketBrowser):

    NAME = '大潤發'

    FRESH_ROUTE = 'http://www.rt-mart.com.tw/fresh/index.php?action=product_sort&prod_sort_uid=%s&p_data_num=400'
    NORMAL_ROUTE = 'http://www.rt-mart.com.tw/direct/index.php?action=product_sort&prod_sort_uid=%s&p_data_num=400'

    INDEX_ROUTE = 'http://www.rt-mart.com.tw'

    # 米
    # 麵
    # 罐頭 (泡菜、玉米、鳳梨、鮪魚、高湯)
    # 咖哩
    # 粉、香料
    # 鹹醬
    # 甜醬

    # 起司、奶油
    # 牛奶、蛋
    # 蒟蒻、香腸等、豆腐、糕類
    # 沙拉味增

    PRODUCT_MAP = {
        '常溫商品': [(3762, 0),
                 (3763, 0),
                 (3787, 0),
                 (37824, 0),
                 (37840, 0), (37712, 0),
                 (3765, 0),
                 (3790, 0)],
        '冷藏商品': [(53914, 1),
                 (53901, 1), (53916, 1),
                 (53910, 1), (53909, 1), (53913, 1), (53915, 1),
                 (53911, 1)],
        '冷凍商品': [(53887, 1),
                 (53892, 1)],
        '海鮮': [(52701, 1), (52702, 1), (52703, 1), (52704, 1)],
        '牛肉': [(52698, 1)], '羊肉': [(52699, 1)],
        '雞肉': [(52697, 1)], '豬肉': [(52696, 1)],
        '蔬菜': [(52494, 1)], '水果': [(52495, 1)],
        '雜貨': [(3767, 0)]
    }

    NAME_RE = re.compile('''
        (?:.+?)(?=[0-9]+.*|\(約+.*|$)
    ''', re.X)

    ORIGIN_RE = re.compile('''
        (?<=產地:)(?:.+?)(?=\\r\\n)
    ''', re.X)

    WEIGHT_RE = re.compile('''
        (?<=規格:)(?:.+?)(?=\\r\\n)
    ''', re.X)

    def __init__(self):
        super(RtmartBrowser, self).__init__()

    @staticmethod
    def get_product_urls(map_str):

        normal = map_str[1] == 0

        if normal:
            url = RtmartBrowser.NORMAL_ROUTE % map_str[0]
        else:
            url = RtmartBrowser.FRESH_ROUTE % map_str[0]
        page = MarketBrowser.get_html(url)
        urls = page.xpath('//div[@class="classify_prolistBox"]//h5[@class="for_proname"]/a/@href')
        return [url for url in set(urls)]

    def get_product_price(self, url):

        page = MarketBrowser.get_html(url)

        xpath = Directory.flat_xpath

        name_str = xpath(page, '//div[@class="pro_rightbox"]/h2[@class="product_Titlename"]/span/text()')

        price_str = xpath(page, '//div[@class="product_PRICEBOX"]//span[@class="price_num"]/text()')

        intro_str = xpath(page, '//table[@class="title_word"]//table/tr/td/text()')

        try:

            # 紅蘿蔔約500g => 紅蘿蔔
            name = RtmartBrowser.NAME_RE.findall(name_str)[0]

            # try to find spec in introduction
            try:
                spec_str = RtmartBrowser.WEIGHT_RE.findall(intro_str)[0]
                weight = self.get_weight(spec_str)

                # test spec with weight in title
                test_weight = self.get_weight(name_str)

                if test_weight and test_weight != weight:
                    weight = test_weight

            # try to find spec in title
            except IndexError:
                weight = self.get_weight(name_str)

            # &prod_no=12345 => 12345
            pid = urlparse.parse_qs(url)['prod_no'][0]

            # try to find origin in introduction
            try:
                origin_str = RtmartBrowser.ORIGIN_RE.findall(intro_str)[0]

            # tyr to find origin in title
            except IndexError:
                origin_str = name_str

            origin = self.get_origin(origin_str)

            # try to find count in title
            count = self.get_count(name_str)

            price_str = Directory.NUM_RE.findall(price_str)[0]
            price = int(price_str)

            # try to find unit in title, introduction
            unit = self.get_unit(name_str + intro_str)

        except:
            log.error(Directory.ERROR_MAP[3] % (name_str, url))
            return None, None

        product = Product(source=url,
                          name=name, origin=origin,
                          market_id=self.market.id,
                          pid=pid,
                          weight=weight,
                          count=count,
                          unit=unit)

        price = Price(price=price, date=self.date)

        return product, price







































