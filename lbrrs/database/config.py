#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from sqlalchemy import create_engine
from contextlib import contextmanager
from . import _base, _session
from .model import Config, Market, Part, Origin, Alias, Unit

engine = None


def setup_session(db_path):
    global engine
    engine = create_engine(db_path)
    _session.configure(bind=engine)


def init():
    print('initializing database...')
    _base.metadata.drop_all(engine)
    _base.metadata.create_all(engine)

    with session_scope() as session:

        chicken = Config(name='雞肉')
        chicken.parts = [
            Part(name='全雞', aliases=[
                Alias(name='土雞'),
                Alias(name='烏骨雞'),
                Alias(name='古早雞'),
                Alias(name='塊', anti=True),
                Alias(name='胸', anti=True),
                Alias(name='翅', anti=True),
                Alias(name='腿', anti=True)
            ]),
            Part(name='半雞', aliases=[
                Alias(name='半')
            ]),
            Part(name='雞胸肉', aliases=[
                Alias(name='清胸'),
                Alias(name='雞胸'),
                Alias(name='清雞胸'),
                Alias(name='清雞胸肉'),
                Alias(name='胸肉')
            ]),
            Part(name='雞里肌肉', aliases=[
                Alias(name='里肌')
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

        pork = Config(name='豬肉')
        pork.parts = [
            Part(name='豬腹脇肉', aliases=[
                Alias(name='五花'),
                Alias(name='五花肉'),
                Alias(name='三層'),
                Alias(name='豬肉')
            ]),
            Part(name='豬肩胛肉', aliases=[
                Alias(name='梅花'),
                Alias(name='胛心'),
                Alias(name='胛心排', anti=True)
            ]),
            Part(name='豬肩頸肉', aliases=[
                Alias(name='霜降'),
                Alias(name='松坂'),
                Alias(name='松阪'),
                Alias(name='雪花')
            ]),
            Part(name='豬里肌肉', aliases=[
                Alias(name='里肌'),
                Alias(name='腰內'),
                Alias(name='豬腰子'),
                Alias(name='豬排'),
                Alias(name='菲力')
            ]),
            Part(name='豬腿肉', aliases=[
                Alias(name='腿肉'),
                Alias(name='腿'),
                Alias(name='腱子'),
                Alias(name='豬蹄膀')
            ]),
            Part(name='豬絞肉', aliases=[
                Alias(name='絞肉')
            ]),
            Part(name='豬肉片', aliases=[
                Alias(name='肉片'),
                Alias(name='薄片')
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
            Part(name='豬腳', aliases=[
                Alias(name='豬蹄')
            ]),
            Part(name='豬心')
        ]

        groceries = Config(name='雜貨')
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
                Alias(name='紅豆薏仁', anti=True)
            ]),
            Part(name='蓮子'),
            Part(name='小米'),
            Part(name='粉圓'),
            Part(name='紅棗'),
            Part(name='芝麻', aliases=[
                Alias(name='芝蔴')
            ]),
            Part(name='西谷米'),
            Part(name='糯米'),
            Part(name='藜麥'),
            Part(name='枸杞'),
            Part(name='當歸'),
            Part(name='麥仁'),
            Part(name='八角'),
            Part(name='山楂'),
            Part(name='桂圓'),
            Part(name='花生', aliases=[
                Alias(name='土豆')
            ]),
            Part(name='昆布'),
            Part(name='乾香菇', aliases=[
                Alias(name='香菇'),
                Alias(name='鈕釦菇'),
                Alias(name='冬菇'),
                Alias(name='鈕扣菇')
            ]),
            Part(name='木耳'),
            Part(name='奇亞籽'),
            Part(name='柴魚'),
            Part(name='海帶芽'),
            Part(name='海苔'),
            Part(name='蝦仁', aliases=[
                Alias(name='櫻花蝦')
            ]),
            Part(name='乾金針', aliases=[
                Alias(name='金針')
            ]),
            Part(name='紫菜'),
            Part(name='小魚乾'),
            Part(name='豆豉'),
            Part(name='決明子')
        ]

        veg = Config(name='蔬菜')
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
                Alias(name='A菜'),
                Alias(name='大陸妹')
            ]),
            Part(name='芥藍', aliases=[
                Alias(name='格藍菜'),
                Alias(name='格蘭菜')
            ]),
            Part(name='地瓜葉'),
            Part(name='地瓜', aliases=[
                Alias(name='地瓜葉', anti=True)
            ]),
            Part(name='蔥', aliases=[
                Alias(name='蔥頭', anti=True),
                Alias(name='三星蔥'),
                Alias(name='洋蔥', anti=True),
                Alias(name='葱')
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
                Alias(name='乾香菇', anti=True)
            ]),
            Part(name='乾香菇'),
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
            Part(name='南瓜'),
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
                Alias(name='糯米椒')
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
                Alias(name='蒜頭')
            ]),
            Part(name='紅蔥頭'),
            Part(name='冬瓜'),
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
                Alias(name='長豇豆')
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
                Alias(name='美生菜')
            ])
        ]

        fruit = Config(name='水果')
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
                Alias(name='葡萄柚', anti=True)
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
            Part(name='椪柑'),
            Part(name='甜柿', aliases=[
                Alias(name='柿')
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
            Part(name='藍莓'),
            Part(name='橄欖'),
            Part(name='茂谷柑'),
            Part(name='芒果'),
            Part(name='荔枝'),
            Part(name='櫻桃'),
            Part(name='柳橙')
        ]

        normal = Config(name='常溫商品')
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
                Alias(name='白飯')
            ]),
            Part(name='糙米', aliases=[
                Alias(name='糙米飯')
            ]),
            Part(name='黑米'),
            Part(name='壽司米', aliases=[
                Alias(name='壽司飯')
            ]),
            Part(name='紫米'),
            Part(name='香米'),
            Part(name='月光米'),
            Part(name='胚芽米'),
            Part(name='穀米'),
            Part(name='玉米罐頭', aliases=[
                Alias(name='綠巨人'),
                Alias(name='玉米粒')
            ]),
            Part(name='鮪魚罐頭', aliases=[
                Alias(name='鮪魚')
            ]),
            Part(name='肉醬罐頭', aliases=[
                Alias(name='肉醬'),
                Alias(name='烤肉醬')
            ]),
            Part(name='高湯', aliases=[
                Alias(name='湯塊')
            ]),
            Part(name='泡菜'),
            Part(name='脆瓜'),
            Part(name='紅燒鰻'),
            Part(name='鯖魚罐頭', aliases=[
                Alias(name='鯖魚')
            ]),
            Part(name='紅燒魚'),
            Part(name='素雞'),
            Part(name='麵粉', aliases=[
                Alias(name='澱粉', anti=True),
                Alias(name='低筋麵粉'),
                Alias(name='中筋麵粉'),
                Alias(name='高筋麵粉'),
                Alias(name='高粉'),
                Alias(name='低粉'),
                Alias(name='麵團')
            ]),
            Part(name='五香粉'),
            Part(name='番薯粉'),
            Part(name='太白粉'),
            Part(name='麵包粉'),
            Part(name='愛玉粉'),
            Part(name='洋菜粉'),
            Part(name='咖哩粉'),
            Part(name='玉米粉'),
            Part(name='鬆餅粉'),
            Part(name='薑黃粉'),
            Part(name='茴香粉'),
            Part(name='七味粉'),
            Part(name='抹茶粉'),
            Part(name='甘梅粉'),
            Part(name='椰子粉'),
            Part(name='肉桂粉'),
            Part(name='鰹魚粉'),
            Part(name='泡打粉'),
            Part(name='吉利丁'),
            Part(name='果凍粉'),
            Part(name='豆蔻粉'),
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
            Part(name='羅勒'),
            Part(name='月桂葉'),
            Part(name='百里香'),
            Part(name='雞粉'),
            Part(name='薯粉'),
            Part(name='咖哩'),
            Part(name='胡椒'),
            Part(name='砂糖'),
            Part(name='麵條', aliases=[
                Alias(name='細麵')
            ]),
            Part(name='麵線'),
            Part(name='冬粉'),
            Part(name='意麵'),
            Part(name='雞絲麵'),
            Part(name='蕎麥麵'),
            Part(name='烏龍麵'),
            Part(name='拉麵'),
            Part(name='義大利麵', aliases=[
                Alias(name='意大利面')
            ]),
            Part(name='通心粉'),
            Part(name='筆管麵'),
            Part(name='炊粉'),
            Part(name='粄條'),
            Part(name='水粉'),
            Part(name='粉絲'),
            Part(name='寬粉'),
            Part(name='番茄醬'),
            Part(name='甜辣醬'),
            Part(name='醬油膏'),
            Part(name='豆瓣醬', aliases=[
                Alias(name='豆瓣')
            ]),
            Part(name='醬油'),
            Part(name='辣醬'),
            Part(name='烤肉醬'),
            Part(name='芥末醬'),
            Part(name='咖哩醬'),
            Part(name='胡麻醬'),
            Part(name='壽喜燒醬'),
            Part(name='鵝肝醬'),
            Part(name='凱撒醬'),
            Part(name='辣椒醬'),
            Part(name='老虎醬'),
            Part(name='蛋黃醬'),
            Part(name='烤肉醬'),
            Part(name='玉米醬'),
            Part(name='卡士達醬'),
            Part(name='義大利麵醬'),
            Part(name='紅醬'),
            Part(name='白醬'),
            Part(name='炸醬'),
            Part(name='沙茶醬', aliases=[
                Alias(name='沙茶')
            ]),
            Part(name='甜雞醬'),
            Part(name='巧克力醬', aliases=[
                Alias(name='朱古力粉')
            ]),
            Part(name='花生醬'),
            Part(name='千島醬'),
            Part(name='蔓越莓醬'),
            Part(name='煉乳', aliases=[
                Alias(name='煉奶')
            ]),
            Part(name='迷迭香'),
            Part(name='滷包'),
            Part(name='香鬆')

        ]

        chills = Config(name='冷藏商品')
        chills.parts = [
            Part(name='鮮乳', aliases=[
                Alias(name='鮮奶'),
                Alias(name='鮮奶油', anti=True),
                Alias(name='乳脂', anti=True)
            ]),
            Part(name='蛋', aliases=[
                Alias(name='鹹蛋', anti=True),
                Alias(name='鐵蛋', anti=True),
                Alias(name='滷蛋', anti=True),
                Alias(name='茶葉蛋', anti=True),
                Alias(name='皮蛋', anti=True),
                Alias(name='鹹', anti=True),
                Alias(name='奶', anti=True),
                Alias(name='豆腐', anti=True),
                Alias(name='蛋皮')
            ]),
            Part(name='豆腐', aliases=[
                Alias(name='凍豆腐'),
                Alias(name='豆腐乳', anti=True),
                Alias(name='鍋', anti=True)
            ]),
            Part(name='豆皮'),
            Part(name='味噌', aliases=[
                Alias(name='味增')
            ]),
            Part(name='奶油'),
            Part(name='起司', aliases=[
                Alias(name='乾酪'),
                Alias(name='起士'),
                Alias(name='乳酪'),
                Alias(name='棒', anti=True),
                Alias(name='條', anti=True),
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
                Alias(name='美乃滋')
            ]),
            Part(name='皮蛋'),
            Part(name='鹹蛋'),
            Part(name='海帶結', aliases=[
                Alias(name='海帶'),
                Alias(name='海帶芽', anti=True)
            ]),
            Part(name='豆輪'),
            Part(name='蒟蒻')
        ]

        seafood = Config(name='海鮮')
        seafood.parts = [
            Part(name='蝦', aliases=[
                Alias(name='沙拉', anti=True)
            ]),
            Part(name='蟹', aliases=[
                Alias(name='蟹棒')
            ]),
            Part(name='小卷'),
            Part(name='透抽'),
            Part(name='花枝'),
            Part(name='小管'),
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
            Part(name='鱈'),
            Part(name='肉魚'),
            Part(name='白鯧'),
            Part(name='秋刀魚'),
            Part(name='吻仔魚'),
            Part(name='黃魚'),
            Part(name='丁香魚'),
            Part(name='牡蠣')
        ]

        beef = Config(name='牛肉')
        beef.parts = [
            Part(name='牛')
        ]

        goat = Config(name='羊肉')
        goat.parts = [
            Part(name='羊')
        ]

        freezings = Config(name='冷凍商品')
        freezings.parts = [
            Part(name='冰', aliases=[
                Alias(name='冰淇淋')
            ]),
            Part(name='水餃', aliases=[
                Alias(name='煎餃')
            ]),
            Part(name='餛飩'),
            Part(name='貢丸'),
            Part(name='魚丸')
        ]

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


