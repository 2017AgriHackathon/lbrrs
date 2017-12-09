#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from sqlalchemy import create_engine, update
from contextlib import contextmanager
from . import _base, _session
from .model import Config, Market, Part, Origin, Alias, Unit, Product, Recipe_Part, Crop
import sys

engine = None


def setup_session(db_path):
    global engine
    engine = create_engine(db_path)
    _session.configure(bind=engine)


def init():
    print('initializing database...', file=sys.stdout)
#   _base.metadata.drop_all(engine)
    _base.metadata.create_all(engine)

    init_units()
    init_origins()
    init_market()
    init_configs()
    init_parts_aliases()


def reset_parts_aliases():
    print('reset dictionary...')

    with session_scope() as session:
        # Reset fk from product, recipe_part, season
        session.execute(update(Product, values={Product.part_id: None,
                                                Product.alias_id: None}))
        session.execute(update(Recipe_Part, values={Recipe_Part.part_id: None}))
        session.execute(update(Crop, values={Crop.part_id: None}))

        # Delete parts, aliases
        session.query(Alias).delete()
        session.query(Part).delete()

    # Re-initialize parts & aliases
    init_parts_aliases()


def init_configs():

    with session_scope() as session:

        chicken = Config(name='雞肉')

        pork = Config(name='豬肉')

        groceries = Config(name='雜貨')

        veg = Config(name='蔬菜')

        fruit = Config(name='水果')

        normal = Config(name='常溫商品')

        chills = Config(name='冷藏商品')

        seafood = Config(name='海鮮')

        beef = Config(name='牛肉')

        goat = Config(name='羊肉')

        freezings = Config(name='冷凍商品')

        session.add(chicken)
        session.add(pork)
        session.add(groceries)
        session.add(veg)
        session.add(fruit)
        session.add(normal)
        session.add(chills)
        session.add(seafood)
        session.add(beef)
        session.add(goat)
        session.add(freezings)


def init_parts_aliases():

    with session_scope() as session:

        chicken = session.query(Config).filter(Config.name == '雞肉').first()
        chicken.parts = [
            Part(name='全雞', aliases=[
                Alias(name='土雞'),
                Alias(name='放山雞', insert=0, delete=1, substitute=0),
                Alias(name='烏骨雞'),
                Alias(name='古早雞'),
                Alias(name='雞', insert=0, delete=0, substitute=0),
                Alias(name='塊', anti=True),
                Alias(name='胸', anti=True),
                Alias(name='翅', anti=True),
                Alias(name='腿', anti=True)
            ]),
            Part(name='半雞'),
            Part(name='雞胸肉', aliases=[
                Alias(name='清胸'),
                Alias(name='雞胸'),
                Alias(name='清雞胸'),
                Alias(name='清雞胸肉'),
                Alias(name='胸肉'),
                Alias(name='雞肉'),
                Alias(name='雞丁', insert=1, delete=0, substitute=0),
                Alias(name='骨', anti=True)
            ]),
            Part(name='雞里肌肉', aliases=[
                Alias(name='雞里肌', insert=2, delete=0, substitute=0),
                Alias(name='雞柳')
            ]),
            Part(name='雞腿肉', aliases=[
                Alias(name='骨腿'),
                Alias(name='清腿'),
                Alias(name='棒腿'),
                Alias(name='小腿'),
                Alias(name='腿排'),
                Alias(name='去骨雞腿'),
                Alias(name='雞腿'),
                Alias(name='雞排'),
                Alias(name='翅', anti=True)
            ]),
            Part(name='雞翅', aliases=[
                Alias(name='二節翅'),
                Alias(name='三節翅'),
                Alias(name='翅小腿'),
                Alias(name='翅腿'),
                Alias(name='雞翼')
            ]),
            Part(name='雞切塊', aliases=[
                Alias(name='切塊'),
                Alias(name='剁塊'),
                Alias(name='腿切塊'),
                Alias(name='八塊'),
                Alias(name='九塊')
            ]),
            Part(name='雞腳', aliases=[
                Alias(name='雞爪')
            ]),
            Part(name='雞肫'),
            Part(name='雞心'),
            Part(name='雞尾椎'),
            Part(name='雞屁股'),
            Part(name='雞尾椎'),
            Part(name='雞胗')
        ]

        pork = session.query(Config).filter(Config.name == '豬肉').first()
        pork.parts = [
            Part(name='豬腹脇肉', aliases=[
                Alias(name='五花'),
                Alias(name='五花肉'),
                Alias(name='三層'),
                Alias(name='豬肉'),
                Alias(name='牛', anti=True)
            ]),
            Part(name='豬肩胛肉', aliases=[
                Alias(name='梅花'),
                Alias(name='胛心'),
                Alias(name='胛心排', anti=True),
                Alias(name='牛', anti=True)
            ]),
            Part(name='豬肩頸肉', aliases=[
                Alias(name='霜降'),
                Alias(name='松坂'),
                Alias(name='松阪'),
                Alias(name='雪花'),
                Alias(name='牛', anti=True)
            ]),
            Part(name='豬里肌肉', aliases=[
                Alias(name='豬里肌', insert=2, delete=0, substitute=0),
                Alias(name='豬大里肌'),
                Alias(name='腰內'),
                Alias(name='豬腰子'),
                Alias(name='豬排'),
                Alias(name='豬菲力')
            ]),
            Part(name='豬腿肉', aliases=[
                Alias(name='豬腿'),
                Alias(name='豬前腿'),
                Alias(name='腱子'),
                Alias(name='豬腱'),
                Alias(name='豬蹄膀')
            ]),
            Part(name='豬絞肉', aliases=[
                Alias(name='絞肉'),
                Alias(name='肉末')
            ]),
            Part(name='豬肉片', aliases=[
                Alias(name='肉片')
            ]),
            Part(name='豬肉絲', aliases=[
                Alias(name='肉絲'),
                Alias(name='肉條'),
            ]),
            Part(name='豬排骨', aliases=[
                Alias(name='排骨'),
                Alias(name='龍骨'),
                Alias(name='背骨'),
                Alias(name='肋骨'),
                Alias(name='軟骨'),
                Alias(name='大骨'),
                Alias(name='頸骨'),
                Alias(name='胛心排'),
                Alias(name='豬小排')
            ]),
            Part(name='豬肝'),
            Part(name='豬腳'),
            Part(name='豬心')
        ]

        groceries = session.query(Config).filter(Config.name == '雜貨').first()
        groceries.parts = [
            Part(name='紅豆', aliases=[
                Alias(name='豆仁', anti=True),
                Alias(name='大紅豆', anti=True),
                Alias(name='紅豆薏仁', anti=True)
            ]),
            Part(name='黃豆', aliases=[
                Alias(name='豆仁', anti=True),
                Alias(name='豆仁', anti=True)
            ]),
            Part(name='綠豆', aliases=[
                Alias(name='豆仁', anti=True),
                Alias(name='豆仁', anti=True)
            ]),
            Part(name='黑豆', aliases=[
                Alias(name='豆仁', anti=True),
                Alias(name='黑豆豉', anti=True)
            ]),
            Part(name='花豆', aliases=[
                Alias(name='大紅豆', anti=True)
            ]),
            Part(name='薏仁', aliases=[
                Alias(name='大薏仁'),
                Alias(name='紅豆薏仁', anti=True),
                Alias(name='薏苡')
            ]),
            Part(name='蓮子'),
            Part(name='小米'),
            Part(name='粉圓'),
            Part(name='紅棗'),
            Part(name='芝麻', aliases=[
                Alias(name='芝蔴'),
                Alias(name='胡麻'),
                Alias(name='醬', anti=True)
            ]),
            Part(name='西谷米'),
            Part(name='糯米', aliases=[
                Alias(name='粉', anti=True)
            ]),
            Part(name='藜麥'),
            Part(name='枸杞', aliases=[
                Alias(name='杞子')
            ]),
            Part(name='當歸'),
            Part(name='麥仁'),
            Part(name='八角'),
            Part(name='山楂'),
            Part(name='桂圓'),
            Part(name='花生', aliases=[
                Alias(name='土豆'),
                Alias(name='醬', anti=True)
            ]),
            Part(name='昆布', aliases=[
                Alias(name='和露', anti=True)
            ]),
            Part(name='乾香菇', aliases=[
                Alias(name='香菇'),
                Alias(name='鈕釦菇'),
                Alias(name='冬菇'),
                Alias(name='鈕扣菇')
            ]),
            Part(name='木耳'),
            Part(name='奇亞籽'),
            Part(name='柴魚', aliases=[
                Alias(name='和露', anti=True)
            ]),
            Part(name='海帶芽'),
            Part(name='海苔'),
            Part(name='蝦仁', aliases=[
                Alias(name='櫻花蝦')
            ]),
            Part(name='乾金針', aliases=[
                Alias(name='金針')
            ]),
            Part(name='紫菜'),
            Part(name='魚乾'),
            Part(name='豆豉'),
            Part(name='決明子'),
            Part(name='茶葉'),
            Part(name='印度棗'),
            Part(name='腰果'),
            Part(name='核桃'),
            Part(name='紅藜', aliases=[
                Alias(name='米', anti=True)
            ]),
            Part(name='燕麥片', aliases=[
                Alias(name='燕麥粒')
            ]),
            Part(name='金棗'),
            Part(name='蜜棗'),
            Part(name='栗子')
        ]

        veg = session.query(Config).filter(Config.name == '蔬菜').first()
        veg.parts = [
            Part(name='玉米筍'),
            Part(name='薑'),
            Part(name='洋蔥'),
            Part(name='蘿蔔', aliases=[
                Alias(name='紅蘿蔔', anti=True),
                Alias(name='胡蘿蔔', anti=True),
                Alias(name='菜頭')
            ]),
            Part(name='紅蘿蔔', aliases=[
                Alias(name='胡蘿蔔')
            ]),
            Part(name='馬鈴薯', aliases=[
                Alias(name='薯泥')
            ]),
            Part(name='小白菜'),
            Part(name='青江菜', aliases=[
                Alias(name='清江菜')]
            ),
            Part(name='青江白菜'),
            Part(name='葉白菜'),
            Part(name='奶油白菜'),
            Part(name='翠白菜'),
            Part(name='味美菜'),
            Part(name='小松菜'),
            Part(name='青松菜'),
            Part(name='蚵白菜', aliases=[
                Alias(name='蚵仔白菜')
            ]),
            Part(name='結球白菜', aliases=[
                Alias(name='包心白菜'),
                Alias(name='大白菜')
            ]),
            Part(name='娃娃菜'),
            Part(name='萵苣', aliases=[
                Alias(name='a菜'),
                Alias(name='大陸妹')
            ]),
            Part(name='芥藍', aliases=[
                Alias(name='格藍菜'),
                Alias(name='格蘭菜')
            ]),
            Part(name='地瓜葉', aliases=[
                Alias(name='番薯葉')
            ]),
            Part(name='地瓜', aliases=[
                Alias(name='地瓜葉', anti=True),
                Alias(name='甘藷'),
                Alias(name='番薯')
            ]),
            Part(name='青蔥', aliases=[
                Alias(name='蔥頭', anti=True),
                Alias(name='洋蔥', anti=True),
                Alias(name='醬', anti=True),
                Alias(name='三星蔥'),
                Alias(name='3星蔥'),
                Alias(name='葱', insert=1, delete=0, substitute=0),
                Alias(name='蔥', insert=1, delete=0, substitute=0),
                Alias(name='蒽', insert=1, delete=0, substitute=0)
            ]),
            Part(name='玉米', aliases=[
                Alias(name='玉米筍', anti=True)
            ]),
            Part(name='茭白筍', aliases=[
                Alias(name='筊白筍')
            ]),
            Part(name='芹菜', aliases=[
                Alias(name='西芹'),
                Alias(name='西洋芹')
            ]),
            Part(name='甜椒', aliases=[
                Alias(name='青椒'),
                Alias(name='紅椒'),
                Alias(name='黃椒'),
                Alias(name='菜椒'),
                Alias(name='花椒', anti=True),
                Alias(name='彩椒')
            ]),
            Part(name='空心菜', aliases=[
                Alias(name='蕹菜')
            ]),
            Part(name='茄子'),
            Part(name='杏鮑菇'),
            Part(name='香菇', aliases=[
                Alias(name='乾香菇', anti=True),
                Alias(name='菇類')
            ]),
            Part(name='金針菇'),
            Part(name='雪白菇'),
            Part(name='金絲菇'),
            Part(name='三絲菇'),
            Part(name='雨來菇'),
            Part(name='白玉菇'),
            Part(name='黑美人菇'),
            Part(name='白精靈菇'),
            Part(name='真珠菇'),
            Part(name='秀珍菇'),
            Part(name='袖珍菇'),
            Part(name='鴻喜菇'),
            Part(name='珊瑚菇'),
            Part(name='白靈菇'),
            Part(name='美白菇'),
            Part(name='金喜菇'),
            Part(name='金滑菇'),
            Part(name='舞菇'),
            Part(name='芋頭'),
            Part(name='韭菜', aliases=[
                Alias(name='韭菜花'),
                Alias(name='韭黃')
            ]),
            Part(name='韭菜花'),
            Part(name='高麗菜', aliases=[
                Alias(name='紫', anti=True),
                Alias(name='甘藍'),
                Alias(name='高麗菜心'),
                Alias(name='高山')
            ]),
            Part(name='紫高麗菜', aliases=[
                Alias(name='紫甘藍'),
                Alias(name='紫色甘藍'),
                Alias(name='紫高麗菜'),
                Alias(name='紫色高麗菜')
            ]),
            Part(name='木耳'),
            Part(name='大頭菜'),
            Part(name='絲瓜', aliases=[
                Alias(name='菜瓜'),
                Alias(name='角瓜'),
            ]),
            Part(name='南瓜', aliases=[
                Alias(name='金瓜')
            ]),
            Part(name='菠菜', aliases=[
                Alias(name='菠菱菜'),
                Alias(name='菠薐菜'),
                Alias(name='波菜')
            ]),
            Part(name='茼蒿'),
            Part(name='苦瓜', aliases=[
                Alias(name='青苦瓜'),
                Alias(name='山苦瓜')
            ]),
            Part(name='牛蕃茄', aliases=[
                Alias(name='牛番茄'),
                Alias(name='蕃茄'),
                Alias(name='番茄')
            ]),
            Part(name='山藥'),
            Part(name='花椰菜', aliases=[
                Alias(name='青花菜'),
                Alias(name='花椰')
            ]),
            Part(name='絲瓜'),
            Part(name='豆芽菜', aliases=[
                Alias(name='豆芽')
            ]),
            Part(name='油菜'),
            Part(name='辣椒', aliases=[
                Alias(name='朝天椒'),
                Alias(name='剝皮辣椒'),
                Alias(name='糯米椒'),
                Alias(name='花椒'),
                Alias(name='醬', anti=True),
                Alias(name='粉', anti=True)
            ]),
            Part(name='芥菜', aliases=[
                Alias(name='雪菜')
            ]),
            Part(name='莧菜'),
            Part(name='苜蓿芽'),
            Part(name='秋葵'),
            Part(name='香菜', aliases=[
                Alias(name='莞荽')
            ]),
            Part(name='九層塔'),
            Part(name='牛蒡'),
            Part(name='小黃瓜', aliases=[
                Alias(name='花胡瓜')
            ]),
            Part(name='大黃瓜', aliases=[
                Alias(name='胡瓜'),
                Alias(name='刺瓜'),
                Alias(name='黃瓜'),
                Alias(name='小黃瓜', anti=True)
            ]),
            Part(name='蒜', aliases=[
                Alias(name='大蒜'),
                Alias(name='蒜味', anti=True),
                Alias(name='蒜頭'),
                Alias(name='醬', anti=True)
            ]),
            Part(name='紅蔥頭'),
            Part(name='冬瓜'),
            Part(name='櫛瓜', aliases=[
                Alias(name='節瓜')
            ]),
            Part(name='洋菇'),
            Part(name='蘆筍'),
            Part(name='甜菜', aliases=[
                Alias(name='甜菜心'),
                Alias(name='甜菜根')
            ]),
            Part(name='銀耳'),
            Part(name='水蓮'),
            Part(name='蓮藕'),
            Part(name='蒲瓜', aliases=[
                Alias(name='蒲子'),
                Alias(name='扁浦'),
                Alias(name='扁蒲'),
                Alias(name='瓠瓜'),
                Alias(name='蒲瓜')
            ]),
            Part(name='豌豆', aliases=[
                Alias(name='荷蘭豆'),
                Alias(name='豌豆嬰', anti=True),
                Alias(name='碗豆')
            ]),
            Part(name='四季豆', aliases=[
                Alias(name='敏豆')
            ]),
            Part(name='菜豆', aliases=[
                Alias(name='長豇豆', insert=1, delete=0, substitute=0)
            ]),
            Part(name='甜豆'),
            Part(name='豆苗', aliases=[
                Alias(name='豆嬰')
            ]),
            Part(name='芥蘭'),
            Part(name='皇宮菜'),
            Part(name='龍鬚菜'),
            Part(name='山蘇'),
            Part(name='紅鳳菜'),
            Part(name='皇帝菜'),
            Part(name='廣島菜'),
            Part(name='竹筍'),
            Part(name='蘿美', aliases=[
                Alias(name='蘿蔓'),
                Alias(name='生菜', insert=0, delete=1, substitute=0)
            ]),
            Part(name='毛豆'),
            Part(name='荸薺')
        ]

        fruit = session.query(Config).filter(Config.name == '水果').first()
        fruit.parts = [
            Part(name='芭樂', aliases=[
                Alias(name='番石榴')
            ]),
            Part(name='檸檬'),
            Part(name='番茄', aliases=[
                Alias(name='蕃茄')

            ]),
            Part(name='木瓜'),
            Part(name='葡萄', aliases=[
                Alias(name='葡萄柚', anti=True),
                Alias(name='巨峰')
            ]),
            Part(name='鳳梨'),
            Part(name='火龍果'),
            Part(name='梨'),
            Part(name='香蕉', aliases=[
                Alias(name='芭蕉')
            ]),
            Part(name='百香果'),
            Part(name='柳丁'),
            Part(name='葡萄柚'),
            Part(name='楊桃'),
            Part(name='釋迦'),
            Part(name='甜柿', aliases=[
                Alias(name='柿子')
            ]),
            Part(name='蓮霧'),
            Part(name='橘子', aliases=[
                Alias(name='桔子'),
                Alias(name='柑子')
            ]),
            Part(name='蘋果'),
            Part(name='奇異果'),
            Part(name='甜瓜', aliases=[
                Alias(name='香瓜'),
                Alias(name='洋香瓜'),
                Alias(name='哈蜜瓜'),
                Alias(name='華蜜瓜'),
                Alias(name='哈密瓜'),
                Alias(name='美濃瓜')
            ]),
            Part(name='金桔'),
            Part(name='藍莓', aliases=[
                Alias(name='醬', anti=True)
            ]),
            Part(name='橄欖', aliases=[
                Alias(name='油', anti=True)
            ]),
            Part(name='茂谷柑'),
            Part(name='芒果', aliases=[
                Alias(name='醬', anti=True)
            ]),
            Part(name='櫻桃'),
            Part(name='柳橙'),
            Part(name='楊桃'),
            Part(name='椪柑'),
            Part(name='桶柑'),
            Part(name='海梨柑'),
            Part(name='金柑'),
            Part(name='枇杷'),
            Part(name='椰子'),
            Part(name='青梅'),
            Part(name='甜蜜桃'),
            Part(name='高接梨'),
            Part(name='水蜜桃'),
            Part(name='荔枝', aliases=[
                Alias(name='番', anti=True)
            ]),
            Part(name='番荔枝'),
            Part(name='李子', aliases=[
                Alias(name='李', insert=0, delete=0, substitute=0),

            ]),
            Part(name='酪梨'),
            Part(name='龍眼'),
            Part(name='檸檬'),
            Part(name='溫帶梨'),
            Part(name='文旦柚', aliases=[
                Alias(name='柚子')
            ]),
            Part(name='葡萄柚'),
            Part(name='草莓'),
            Part(name='西瓜')
        ]

        normal = session.query(Config).filter(Config.name == '常溫商品').first()
        normal.parts = [
            Part(name='砂糖'),
            Part(name='冰糖'),
            Part(name='味霖', aliases=[
                Alias(name='味林'),
                Alias(name='味淋'),
                Alias(name='味醂')
            ]),
            Part(name='魚露'),
            Part(name='白米', aliases=[
                Alias(name='米', insert=0, delete=0, substitute=0),
                Alias(name='飯', insert=1, delete=0, substitute=0),
                Alias(name='精米'),
                Alias(name='鮮米'),
                Alias(name='秈米'),
                Alias(name='臺東米'),
                Alias(name='花蓮米'),
                Alias(name='關山米'),
                Alias(name='多力米'),
                Alias(name='池上米'),
                Alias(name='有機米'),
                Alias(name='免洗米'),
                Alias(name='無洗米'),
                Alias(name='好米'),
                Alias(name='優質米'),
                Alias(name='履歷米'),
                Alias(name='隔夜飯')
            ]),
            Part(name='糙米', aliases=[
                Alias(name='糙米飯')
            ]),
            Part(name='黑米'),
            Part(name='玄米'),
            Part(name='壽司米', aliases=[
                Alias(name='壽司飯')
            ]),
            Part(name='紫米'),
            Part(name='香米'),
            Part(name='越光米'),
            Part(name='胚芽米'),
            Part(name='穀米', aliases=[
                Alias(name='五穀飯')
            ]),
            Part(name='玉米罐頭', aliases=[
                Alias(name='綠巨人'),
                Alias(name='玉米粒')
            ]),
            Part(name='鮪魚罐頭', aliases=[
                Alias(name='鮪魚片')
            ]),
            Part(name='麵筋罐頭', aliases=[
                Alias(name='麵筋')
            ]),
            Part(name='肉醬罐頭', aliases=[
                Alias(name='肉醬'),
                Alias(name='烤肉醬')
            ]),
            Part(name='高湯', aliases=[
                Alias(name='湯塊')
            ]),
            Part(name='脆瓜'),
            Part(name='紅燒鰻'),
            Part(name='鯖魚罐頭'),
            Part(name='紅燒魚'),
            Part(name='素雞'),
            Part(name='麵粉', aliases=[
                Alias(name='澱粉', anti=True),
                Alias(name='低筋麵粉', insert=0, delete=2, substitute=0),
                Alias(name='中筋麵粉', insert=0, delete=2, substitute=0),
                Alias(name='高筋麵粉', insert=0, delete=2, substitute=0),
                Alias(name='麵團')
            ]),
            Part(name='五香粉'),
            Part(name='番薯粉'),
            Part(name='太白粉'),
            Part(name='海鮮醬'),
            Part(name='麵包粉'),
            Part(name='愛玉粉'),
            Part(name='洋菜粉'),
            Part(name='咖哩粉'),
            Part(name='玉米粉'),
            Part(name='紅莓醬'),
            Part(name='鬆餅粉'),
            Part(name='薑黃粉'),
            Part(name='茴香粉', aliases=[
                Alias(name='小茴香', insert=1, delete=1, substitute=0)
            ]),
            Part(name='七味粉'),
            Part(name='抹茶粉'),
            Part(name='甘梅粉'),
            Part(name='椰子粉'),
            Part(name='布丁粉'),
            Part(name='小蘇打粉'),
            Part(name='糯米粉'),
            Part(name='肉桂粉'),
            Part(name='鰹魚粉'),
            Part(name='泡打粉'),
            Part(name='吉利丁', aliases=[
                Alias(name='吉利T')
            ]),
            Part(name='果凍粉'),
            Part(name='椰漿粉'),
            Part(name='豆蔻粉'),
            Part(name='辣椒粉', aliases=[
                Alias(name='紅椒粉')
            ]),
            Part(name='胡椒粉', aliases=[
                Alias(name='醬', anti=True),
                Alias(name='胡椒')
            ]),
            Part(name='胡椒粒'),
            Part(name='酵母粉', aliases=[
                Alias(name='酵母')
            ]),
            Part(name='孜然粉', aliases=[
                Alias(name='孜然')
            ]),
            Part(name='荳蔻粉'),
            Part(name='可可粉', aliases=[
                Alias(name='巧克力粉')
            ]),
            Part(name='義大利香料'),
            Part(name='羅勒'),
            Part(name='月桂葉'),
            Part(name='百里香'),
            Part(name='雞粉', aliases=[
                Alias(name='雞精粉')
            ]),
            Part(name='薯粉'),
            Part(name='咖哩', aliases=[
                Alias(name='醬', anti=True),
                Alias(name='粉', anti=True)
            ]),
            Part(name='油麵'),
            Part(name='乾麵'),
            Part(name='刀削麵'),
            Part(name='麵條', aliases=[
                Alias(name='麵', insert=0, delete=0, substitute=0),
                Alias(name='寬麵'),
                Alias(name='細麵')
            ]),
            Part(name='蔬菜麵'),
            Part(name='雞蛋麵'),
            Part(name='麵線'),
            Part(name='冬粉'),
            Part(name='意麵'),
            Part(name='雞絲麵'),
            Part(name='蕎麥麵'),
            Part(name='烏龍麵'),
            Part(name='拉麵'),
            Part(name='義大利麵', aliases=[
                Alias(name='意大利面'),
                Alias(name='醬', anti=True),
                Alias(name='義大利直麵')
            ]),
            Part(name='通心粉'),
            Part(name='筆管麵'),
            Part(name='粄條'),
            Part(name='水粉'),
            Part(name='粉絲', aliases=[
                Alias(name='冬粉'),
                Alias(name='粉條'),
                Alias(name='寬粉')
            ]),
            Part(name='米粉', aliases=[
                Alias(name='炊粉'),
                Alias(name='水粉')
            ]),
            Part(name='番茄醬', aliases=[
                Alias(name='蕃茄醬')
            ]),
            Part(name='甜辣醬'),
            Part(name='酸甜醬'),
            Part(name='xo醬'),
            Part(name='醬油膏', aliases=[
                Alias(name='油膏'),
                Alias(name='膏油')
            ]),
            Part(name='豆瓣醬', aliases=[
                Alias(name='豆瓣')
            ]),
            Part(name='蠔油'),
            Part(name='醬油', aliases=[
                Alias(name='清油'),
                Alias(name='蔭油'),
                Alias(name='水餃醬汁')
            ]),
            Part(name='和露', aliases=[
                Alias(name='鮮美露')
            ]),
            Part(name='辣醬'),
            Part(name='烤肉醬'),
            Part(name='芥末', aliases=[
                Alias(name='山葵醬')
            ]),
            Part(name='咖哩醬'),
            Part(name='胡麻醬'),
            Part(name='壽喜燒醬'),
            Part(name='鵝肝醬'),
            Part(name='凱撒醬'),
            Part(name='麵醬', aliases=[
                Alias(name='義大利', anti=True),
                Alias(name='意大利', anti=True)
            ]),
            Part(name='辣椒醬'),
            Part(name='老虎醬'),
            Part(name='排骨醬'),
            Part(name='蛋黃醬'),
            Part(name='干貝醬'),
            Part(name='蘑菇醬'),
            Part(name='海苔醬'),
            Part(name='烤肉醬'),
            Part(name='蔥醬'),
            Part(name='玉米醬'),
            Part(name='卡士達醬'),
            Part(name='義大利麵醬'),
            Part(name='牛排醬', aliases=[
                Alias(name='黑胡椒醬'),
                Alias(name='黑椒醬')
            ]),
            Part(name='脂肪抹醬'),
            Part(name='紅醬'),
            Part(name='白醬'),
            Part(name='炸醬'),
            Part(name='沙茶醬', aliases=[
                Alias(name='沙茶')
            ]),
            Part(name='甜雞醬'),
            Part(name='巧克力醬', aliases=[
                Alias(name='朱古力粉'),
                Alias(name='可可醬')
            ]),
            Part(name='花生醬'),
            Part(name='千島醬'),
            Part(name='蔓越莓醬', aliases=[
                Alias(name='藍莓果醬')
            ]),
            Part(name='草莓醬', aliases=[
                Alias(name='草莓果醬')
            ]),
            Part(name='藍莓醬', aliases=[
                Alias(name='藍莓果醬')
            ]),
            Part(name='芒果醬', aliases=[
                Alias(name='芒果果醬')
            ]),
            Part(name='迷迭香'),
            Part(name='滷包', aliases=[
                Alias(name='滷味包')
            ]),
            Part(name='香鬆'),
            Part(name='肉鬆'),
            Part(name='肉脯'),
            Part(name='素鬆', aliases=[
                Alias(name='素香鬆')
            ]),
            Part(name='蜂蜜'),
            Part(name='煉乳', aliases=[
                Alias(name='煉奶')
            ]),
            Part(name='泡菜'),
            Part(name='豆腐乳'),
            Part(name='黑糖'),
            Part(name='果糖'),
            Part(name='麻油'),
            Part(name='香油'),
            Part(name='蘋果醋', aliases=[
                Alias(name='蘋果酢')
            ]),
            Part(name='檸檬醋', aliases=[
                Alias(name='檸檬酢')
            ]),
            Part(name='壽司醋', aliases=[
                Alias(name='壽司酢')
            ]),
            Part(name='糯米醋', aliases=[
                Alias(name='糯米酢')
            ]),
            Part(name='醋', aliases=[
                Alias(name='蘋果', anti=True),
                Alias(name='檸檬', anti=True),
                Alias(name='壽司', anti=True),
                Alias(name='酢')
            ]),
            Part(name='鮮味炒手'),
            Part(name='豆鼓'),
            Part(name='糖粉'),
            Part(name='奶粉'),
            Part(name='可可脆片', aliases=[
                Alias(name='可可碎片'),
                Alias(name='巧克力脆片'),
                Alias(name='巧克力碎片')
            ])
        ]

        chills = session.query(Config).filter(Config.name == '冷藏商品').first()
        chills.parts = [
            Part(name='鮮乳', aliases=[
                Alias(name='牛奶', insert=0, delete=0, substitute=0),
                Alias(name='全脂牛奶', insert=2, delete=0, substitute=0),
                Alias(name='低脂牛奶', insert=2, delete=0, substitute=0),
                Alias(name='鮮奶'),
                Alias(name='鮮奶油', anti=True),
                Alias(name='乳脂', anti=True)
            ]),
            Part(name='雞蛋', aliases=[
                Alias(name='鹹蛋', anti=True),
                Alias(name='鐵蛋', anti=True),
                Alias(name='滷蛋', anti=True),
                Alias(name='茶葉蛋', anti=True),
                Alias(name='皮蛋', anti=True),
                Alias(name='鹹', anti=True),
                Alias(name='奶', anti=True),
                Alias(name='豆腐', anti=True),
                Alias(name='蛋皮'),
                Alias(name='蛋液'),
                Alias(name='蛋黃'),
                Alias(name='蛋白'),
                Alias(name='蛋', insert=0, delete=0, substitute=0)
            ]),
            Part(name='豆腐', aliases=[
                Alias(name='凍豆腐'),
                Alias(name='豆腐乳', anti=True),
                Alias(name='鍋', anti=True)
            ]),
            Part(name='豆皮', aliases=[
                Alias(name='豆腐皮'),
                Alias(name='豆包')
            ]),
            Part(name='味噌', aliases=[
                Alias(name='味增')
            ]),
            Part(name='奶油'),
            Part(name='起司', aliases=[
                Alias(name='乾酪'),
                Alias(name='起士'),
                Alias(name='乳酪'),
                Alias(name='棒', anti=True),
                Alias(name='芝士'),
                Alias(name='cheese')
            ]),
            Part(name='培根'),
            Part(name='火腿'),
            Part(name='香腸'),
            Part(name='熱狗'),
            Part(name='年糕'),
            Part(name='米血'),
            Part(name='蘿蔔糕'),
            Part(name='豬血'),
            Part(name='沙拉', aliases=[
                Alias(name='美乃滋', insert=0, delete=0, substitute=1)
            ]),
            Part(name='皮蛋'),
            Part(name='鹹蛋'),
            Part(name='海帶結', aliases=[
                Alias(name='海帶'),
                Alias(name='海帶芽', anti=True)
            ]),
            Part(name='豆輪'),
            Part(name='蒟蒻'),
            Part(name='優格'),
            Part(name='豆漿'),
            Part(name='甜不辣'),
            Part(name='竹輪')
        ]

        seafood = session.query(Config).filter(Config.name == '海鮮').first()
        seafood.parts = [
            Part(name='蝦', aliases=[
                Alias(name='沙拉', anti=True)
            ]),
            Part(name='蟹', aliases=[
                Alias(name='蟹棒', anti=True),
                Alias(name='蟹味棒', anti=True)
            ]),
            Part(name='透抽', aliases=[
                Alias(name='小管'),
                Alias(name='小卷'),
                Alias(name='中卷'),
                Alias(name='鎖管')
            ]),
            Part(name='花枝'),
            Part(name='魷魚'),
            Part(name='章魚'),
            Part(name='軟絲'),
            Part(name='蚵'),
            Part(name='蛤'),
            Part(name='干貝'),
            Part(name='蠔'),
            Part(name='螺'),
            Part(name='比目魚'),
            Part(name='虱目魚'),
            Part(name='石斑'),
            Part(name='鮭'),
            Part(name='鱸'),
            Part(name='土魠'),
            Part(name='鯖'),
            Part(name='柳葉魚'),
            Part(name='鯛魚'),
            Part(name='竹莢魚'),
            Part(name='鯧'),
            Part(name='烏魚', aliases=[
                Alias(name='烏魚子', anti=True)
            ]),
            Part(name='烏魚子'),
            Part(name='白帶魚'),
            Part(name='多利魚'),
            Part(name='紅魚'),
            Part(name='吳郭魚'),
            Part(name='草魚'),
            Part(name='旗魚'),
            Part(name='鰻', aliases=[
                Alias(name='紅燒', anti=True)
            ]),
            Part(name='鱈'),
            Part(name='肉魚'),
            Part(name='白鯧'),
            Part(name='秋刀魚'),
            Part(name='吻仔魚'),
            Part(name='黃魚'),
            Part(name='丁香魚'),
            Part(name='香魚'),
            Part(name='腰子貝'),
            Part(name='沙魚'),
            Part(name='午仔魚'),
            Part(name='"紅鮕'),
            Part(name='牡蠣'),
            Part(name='蟳'),
            Part(name='扇貝'),
            Part(name='帆立貝'),
            Part(name='蟳'),
            Part(name='鮑魚', aliases=[
                Alias(name='沙拉', anti=True),
                Alias(name='鮑片')
            ]),
            Part(name='龍蝦', aliases=[
                Alias(name='沙拉', anti=True)
            ]),
            Part(name='海參', aliases=[
                Alias(name='海蔘')
            ]),
            Part(name='魴魚')
        ]

        beef = session.query(Config).filter(Config.name == '牛肉').first()
        beef.parts = [
            Part(name='牛', aliases=[
                Alias(name='奶', anti=True),
                Alias(name='油', anti=True),
                Alias(name='湯', anti=True)
            ])
        ]

        goat = session.query(Config).filter(Config.name == '羊肉').first()
        goat.parts = [
            Part(name='羊', aliases=[
                Alias(name='奶', anti=True),
                Alias(name='油', anti=True),
                Alias(name='湯', anti=True)
            ])
        ]

        freezings = session.query(Config).filter(Config.name == '冷凍商品').first()
        freezings.parts = [
            Part(name='冰', aliases=[
                Alias(name='冰淇淋'),
                Alias(name='冰塊', anti=True),
                Alias(name='糖', anti=True)
            ]),
            Part(name='水餃', aliases=[
                Alias(name='煎餃'),
                Alias(name='餃子')
            ]),
            Part(name='餛飩', aliases=[
                Alias(name='雲吞')
            ]),
            Part(name='貢丸'),
            Part(name='魚丸'),
            Part(name='燕餃'),
            Part(name='蛋餃'),
            Part(name='花枝餃'),
            Part(name='香菇餃'),
            Part(name='鍋貼'),
            Part(name='蟹棒', aliases=[
                Alias(name='蟹味棒')
            ]),
            Part(name='魚板')
        ]


def init_market():

    with session_scope() as session:

        g = Market(name='愛買')
        w = Market(name='頂好')
        r = Market(name='大潤發')
        f = Market(name='楓康')
        c = Market(name='家樂福')
        b = Market(name='濱江')
        n = Market(name='新北市農產中心')

        session.add(g)
        session.add(w)
        session.add(r)
        session.add(f)
        session.add(c)
        session.add(b)
        session.add(n)


def init_origins():

    with session_scope() as session:

        tw = Origin(name='臺灣')
        au = Origin(name='澳洲')
        us = Origin(name='美國')
        cn = Origin(name='中國')
        jp = Origin(name='日本')
        kr = Origin(name='韓國')
        other = Origin(name='其他')

        session.add(tw)
        session.add(au)
        session.add(us)
        session.add(cn)
        session.add(jp)
        session.add(kr)
        session.add(other)


def init_units():

    with session_scope() as session:

        u101 = Unit(name='根', level=1)
        u102 = Unit(name='粒', level=1)
        u103 = Unit(name='顆', level=1)
        u104 = Unit(name='支', level=1)
        u105 = Unit(name='條', level=1)
        u106 = Unit(name='瓶', level=1)
        u107 = Unit(name='罐', level=1)
        u108 = Unit(name='隻', level=1)
        u109 = Unit(name='塊', level=1)
        u110 = Unit(name='張', level=1)
        u111 = Unit(name='尾', level=1)
        u112 = Unit(name='把', level=1)
        u113 = Unit(name='個', level=1)
        u114 = Unit(name='片', level=1)

        u21 = Unit(name='包', level=2)
        u22 = Unit(name='袋', level=2)
        u23 = Unit(name='盒', level=2)
        u31 = Unit(name='組', level=3)

        session.add(u101)
        session.add(u102)
        session.add(u103)
        session.add(u104)
        session.add(u105)
        session.add(u106)
        session.add(u107)
        session.add(u108)
        session.add(u109)
        session.add(u110)
        session.add(u111)
        session.add(u112)
        session.add(u113)
        session.add(u114)
        session.add(u21)
        session.add(u22)
        session.add(u23)
        session.add(u31)


@contextmanager
def session_scope():
    session = _session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
