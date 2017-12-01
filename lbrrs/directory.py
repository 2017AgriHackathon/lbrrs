#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import datetime
import re
import logging
from sqlalchemy.orm import subqueryload
from logging.config import fileConfig
from . import _logging_config_path
from .database.config import session_scope
from .database.model import Market, Product, Config, Origin, Price, Part, Unit, Author, Recipe

fileConfig(_logging_config_path)
log = logging.getLogger(__name__)


class Directory(object):
    """initialize with class attribute NAME and loads instance
    attribute from sqlalchemy, as a database entry also provides
    basic text parsing settings"""

    NAME = None

    PRODUCT_MAP = None

    NUM_RE = re.compile('''
            (?:\d+)
    ''', re.X)

    GLOBAL_REPLACE_RE = re.compile('''
        [ 　台／]
        |
        [０-９] 
        |
        [ａ-ｚ]
        |
        [一二三四五六七八九]?
        十?
        [一二三四五六七八九]
    ''', re.X)

    TO_REPLACE_MAP = {
        '台': '臺', '／': '/',
        '１': '1', '２': '2', '３': '3', '４': '4', '５': '5',
        '６': '6', '７': '7', '８': '8', '９': '9', '０': '0',
        'ａ': 'a', 'ｂ': 'b', 'ｃ': 'c', 'ｄ': 'd', 'ｅ': 'e',
        'ｆ': 'f', 'ｇ': 'g', 'ｈ': 'h', 'ｉ': 'i', 'ｊ': 'j',
        'ｋ': 'k', 'ｌ': 'l', 'ｍ': 'm', 'ｎ': 'n', 'ｏ': 'o',
        'ｐ': 'p', 'ｑ': 'q', 'ｒ': 'r', 'ｓ': 's', 'ｔ': 't',
        'ｕ': 'u', 'ｖ': 'v', 'ｗ': 'w', 'ｘ': 'x', 'ｙ': 'y',
        'ｚ': 'z',
        '一': '1', '二': '2', '三': '3', '四': '4', '五': '5',
        '六': '6', '七': '7', '八': '8', '九': '9',
    }

    ORIGIN_MAP = {
        '臺北': '臺灣', '臺中': '臺灣', '基隆': '臺灣', '臺南': '臺灣', '高雄': '臺灣', '新北': '臺灣',
        '桃園': '臺灣', '嘉義': '臺灣', '新竹': '臺灣', '苗栗': '臺灣', '南投': '臺灣', '彰化': '臺灣',
        '屏東': '臺灣', '花蓮': '臺灣', '臺東': '臺灣', '金門': '臺灣', '澎湖': '臺灣', '臺灣': '臺灣',
        '西螺': '臺灣', '美濃': '臺灣', '雲林': '臺灣', '宜蘭': '臺灣', '履歷': '臺灣', '有機': '臺灣',
        '埔里': '臺灣',
        '澳洲': '澳洲',
        '中國': '中國',
        '美國': '美國',
        '日本': '日本', '富士': '日本',
        '韓國': '韓國',
        '進口': '其他'
    }

    UNIT_SET = (1000, 1, 15, 5, 240, 340, 600, 37.5, 454, 28.35, 10, 290, 0.5, 40)

    UNIT_RE = re.compile('''
        (?:
            (?=\D?)(?P<kg>[0-9]+?[./][0-9]+|[0-9]+)(?=kg|公斤|公升|l)                #1000
            |
            (?=\D?)(?P<g>[0-9]+?[./][0-9]+|[0-9]+)(?=g|公克|克|毫升|ml|cc)           #1
            |
            (?=\D?)(?P<u2>[0-9]+?[./][0-9]+|[0-9]+)[大](?=匙|tbs)                    #15
            |
            (?=\D?)(?P<u3>[0-9]+?[./][0-9]+|[0-9]+)[小平]?(?=茶匙|湯匙|匙|tsp|微量|撮|搓) #5
            |
            (?=\D?)(?P<u4>[0-9]+?[./][0-9]+|[0-9]+)[小]?(?=杯|碗|cup)                #240
            |
            (?=\D?)(?P<u5>[0-9]+?[./][0-9]+|[0-9]+)[大](?=杯|碗|罐)                  #340
            |
            (?=\D?)(?P<u6>[0-9]+?[./][0-9]+|[0-9]+)(?=斤)                            #600
            |
            (?=\D?)(?P<u7>[0-9]+?[./][0-9]+|[0-9]+)(?=兩)                            #37.5
            |
            (?=\D?)(?P<u8>[0-9]+?[./][0-9]+|[0-9]+)(?=磅)                            #454
            |
            (?=\D?)(?P<u9>[0-9]+?[./][0-9]+|[0-9]+)(?=盎司)                          #28.35
            |
            (?=\D?)(?P<u10>[0-9]+?[./][0-9]+|[0-9]+)[中](?=匙)                       #10
            |
            (?=\D?)(?P<u11>[0-9]+?[./][0-9]+|[0-9]+)[中](?=碗|飯碗)                  #290
            |
            (?=\D?)(?P<u12>[0-9]+?[./][0-9]+|[0-9]+)[小大]?(?=滴)                    #0.5
            |
            (?=\D?)(?P<u13>[0-9]+?[./][0-9]+|[0-9]+)[小大]?(?=球)                    #40       
            |
            (?=\D?)(?P<value>[0-9]+?[./][0-9]+|[0-9]+)[小大]?(?P<other_unit>[張尾把個片粒顆支條包袋盒瓶罐入])               
        )
    ''', re.X)

    CHINESE_NUMERALS_SET = set('一二三四五六七八九十')

    MULTI_RE = re.compile('''
        (?:[*×xX][0-9]+)
        |
        (?:[0-9]+[*×xX])
    ''', re.X)

    STACK = []

    ERROR_MAP = {
        0: '商品重量單位轉換失敗',
        1: '找不到相對應的%s品項媒合值',
        2: '定義商品部位輸入無效的字串',
        3: '處理html文本%s發生溢位或值錯誤\n請查看原始頁面:(%s)',
        4: '訪問商品頁面(%s)請求逾時',
        5: '處理json文本發生溢位或值錯誤\n%s',
    }

    INFO_MAP = {
        0: '訪問%s取得所有%s商品',
        1: '無法自動分類商品「%s」，產地%s，請定義產品類型或放棄(Enter)\n%s:',
        2: '將商品%s人工定義為%s',
        3: '放棄定義商品%s',
        4: '將商品%s自動定義為%s'
    }

    def __init__(self):

        self.date = datetime.date.today().strftime('%Y-%m-%d')

        with session_scope() as session:
            self.configs = session.query(Config).options(
                subqueryload(Config.parts).subqueryload(Part.aliases)
            ).all()
            self.units = session.query(Unit).order_by(Unit.level.desc()).all()

            if self.PRODUCT_MAP and self.NAME:
                self.market = session.query(Market).filter(Market.name == self.NAME).first()

            session.expunge_all()

    @staticmethod
    def normalize(s):

        def replace(m):

            found = m.group()

            if found in Directory.TO_REPLACE_MAP:
                return Directory.TO_REPLACE_MAP[found]

            # for '十一' to '九十九'
            if found[0] in Directory.CHINESE_NUMERALS_SET:
                len_found = len(found)
                if len_found == 2:
                    return '1' + Directory.TO_REPLACE_MAP[found[1]]
                if len_found == 3:
                    return Directory.TO_REPLACE_MAP[found[0]] + Directory.TO_REPLACE_MAP[found[2]]

            return ''

        s = Directory.GLOBAL_REPLACE_RE.sub(replace, s)

        return s.lower()

    @staticmethod
    def get_origin(origin_str, default='其他'):

        origin_str = Directory.normalize(origin_str)

        def find(s):
            for key in Directory.ORIGIN_MAP.keys():
                if key in s:
                    return Directory.ORIGIN_MAP[key]
            return ''

        with session_scope() as session:
            value = find(origin_str)
            if value:
                origin = session.query(Origin).filter(Origin.name == value).first()
            else:
                origin = session.query(Origin).filter(Origin.name == default).first()
            session.expunge(origin)

        return origin

    def get_unit(self, unit_str):

        for unit in self.units:
            if unit.name in unit_str:
                return unit

        return None

    @classmethod
    def clear_stack(cls):

        def set_product_price(pd, pc):

            if pd.part_id:
                pc.product = pd
                Directory.set_price(pc)
            else:
                Directory.set_product(pd)

        manuals = []

        for config, product, price in cls.STACK:
            product = Directory.classify_product_auto(config, product)
            if product.part_id:
                set_product_price(product, price)
            else:
                manuals.append((config, product, price))

        for config, product, price in manuals:
            product = Directory.classify_product_manual(config, product)
            set_product_price(product, price)

        cls.STACK = []

    @staticmethod
    def set_product(product):
        with session_scope() as session:
            session.add(product)

    @classmethod
    def get_count(cls, s):

        s = cls.normalize(s)

        counts = cls.MULTI_RE.findall(s)

        if counts:
            count_str = ''.join([s for s in counts[0] if s.isalnum()])
            count = int(count_str)

            return count

        return 1

    @classmethod
    def get_weight(cls, s):

        def convert_frac(frac_str):
            num, denom = frac_str.split('/')
            return float(num) / float(denom)

        s = cls.normalize(s)

        s = re.sub('半', '0.5', s)
        s = re.sub('數', '3', s)

        try:

            tokens = cls.UNIT_RE.findall(s)

            for token in tokens:
                for index, multiplier in enumerate(cls.UNIT_SET):
                    unit_value = token[index]
                    if unit_value:
                        if '/' in unit_value:
                            unit_value = convert_frac(unit_value)
                        try:
                            unit_value = float(unit_value)
                        except ValueError:
                            log.error(Directory.ERROR_MAP[0])
                            return None
                        # 120g => 120 * 1 * 3
                        return unit_value * multiplier
        except:
            return None

    @staticmethod
    def classify(config, s):
        find = False
        find_alias_id = None

        for part in config.parts:
            if part.name in s:
                find = True
            for alias in part.aliases:
                if alias.name in s and not alias.anti:
                    find_alias_id = alias.id
                    find = True
            for alias in part.aliases:
                if alias.name in s and alias.anti:
                    find = False
            if find:
                return part.id, find_alias_id

        return None, None

    @staticmethod
    def classify_product_auto(config, product):
        part_id, alias_id = Directory.classify(config, product.name)
        if part_id:
            product.part_id = part_id
            log.info(Directory.INFO_MAP[4] % (product.name, part.name))
        if alias_id:
            product.alias = alias_id
        return product

    @staticmethod
    def classify_product_manual(config, product):

        def decode(s):
            encoding = sys.stdin.encoding
            return s.encode(encoding, 'replace').decode(encoding)

        while True:
            options = ''.join('(%s): %s ' % (i, part.name) for i, part in enumerate(config.parts))
            options = decode(options)
            i = input(Directory.INFO_MAP[1] % (product.name, product.origin.name, options))

            if not i:
                log.info(Directory.INFO_MAP[3] % product.name)
                break
            else:
                try:
                    i = int(i)
                except ValueError:
                    log.error(Directory.ERROR_MAP[2])
                    continue
                if i in range(config.parts.__len__()):
                    product.part_id = config.parts[i].id
                    log.info(Directory.INFO_MAP[2] % (product.name, config.parts[i].name))
                    break
        return product

    @staticmethod
    def check_product(product):
        with session_scope() as session:
            db_product = session.query(Product).filter(
                Product.pid == product.pid
            ).filter(
                Product.market_id == product.market_id
            ).first()

            if db_product:
                session.expunge(db_product)
                return db_product
            return product

    @staticmethod
    def set_price(price):
        with session_scope() as session:

            db_price = session.query(Price).filter(
                Price.date == price.date
            ).filter(
                Price.product_id == price.product.id
            ).first()

            if db_price:
                db_price.price = price.price
            else:
                session.add(price)

    @staticmethod
    def flat_xpath(page, s):
        s = ''.join(page.xpath(s)).strip()
        s = Directory.normalize(s)
        return s

    def get_part(self, s):
        for config in self.configs:
            part_id, alias_id = Directory.classify(config, s)
            if part_id:
                return part_id
        return None

    @staticmethod
    def check_author(author):
        with session_scope() as session:
            db_author = session.query(Author).filter(
                Author.name == author.name
            ).first()

            if db_author:
                session.expunge(db_author)
                return db_author

            return author

    @staticmethod
    def check_recipe(recipe):
        with session_scope() as session:
            db_recipe = session.query(Recipe).filter(
                Recipe.name == recipe.name
            ).filter(
                Recipe.url_id == recipe.url_id
            ).first()

            if db_recipe:
                session.expunge(db_recipe)
                return db_recipe

            return recipe

    @staticmethod
    def set_author(author):
        with session_scope() as session:
            session.add(author)

    @staticmethod
    def set_recipe(recipe):
        with session_scope() as session:
            session.add(recipe)

    @staticmethod
    def set_recipe_part(recipe_part):
        with session_scope() as session:
            session.add(recipe_part)

