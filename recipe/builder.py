#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import pandas as pd
from argparse import ArgumentParser
from lbrrs.database import config
from lbrrs.directory import Directory
from lbrrs.database.model import Recipe, Recipe_Part, Author
import re
from . import _icook_path


FAN_RE = re.compile('''
    (?:[0-9]+?[./][0-9]+|[0-9]+)(?=萬)   
''', re.X)
MINUTE_RE = re.compile('''
    (?:[0-9]+?[./][0-9]+|[0-9]+)(?=分鐘)   
''', re.X)
SIZE_RE = re.compile('''
    (?:[0-9]+?[./][0-9]+|[0-9]+)(?=人份)   
''', re.X)


def convert_frac(frac_str):
    num, denom = frac_str.split('/')
    return float(num) / float(denom)


def build(db_path):
    if db_path:
        config.setup_session(db_path)

        df = pd.read_excel(_icook_path, dtype=str)

        config.setup_session('postgresql+psycopg2://postgres:1qaz@WSX@104.199.238.161/lbrrs')
        directory = Directory()

        # build authors
        authors = df.drop(
            ['url_id', 'ing_nm', 'ing_unit', '食譜', 'desrp', 'dur', 'title', 'dish_cnt', 'dish_date', 'view', 'favor_cnt',
             '份量', '跟著做', 'comment_cnt'], axis=1)
        authors.drop_duplicates(inplace=True)

        for i, row in authors.iterrows():
            fans = row['粉絲']
            fans = Directory.normalize(fans)
            match = FAN_RE.findall(fans)
            if match:
                fans = float(match[0]) * 10000
            a = Author(
                name=row['auth_nm'],
                fans=float(fans),
                aid=row['auth_id']
            )
            Directory.set_author(a)

        # build recipe
        recipes = df.drop(['ing_nm', 'ing_unit'], axis=1)
        recipes.drop_duplicates(inplace=True)
        len(recipes)

        for i, row in recipes.iterrows():

            aid = row['auth_id']
            author = Author(aid=aid)
            author = Directory.check_author(author)

            try:
                duration = row['dur']
                duration = Directory.normailze(duration)
                duration = float(MINUTE_RE.findall(duration)[0])
            except:
                duration = None

            try:
                size = row['份量']
                size = Directory.normailze(size)
                size = float(SIZE_RE.findall(size)[0])
            except:
                size = 1

            favors = int(row['favor_cnt'])
            views = int(row['view'])
            comments = int(row['comment_cnt'])
            trys = float(row['跟著做'])

            recipe = Recipe(
                name=row['title'],
                url_id=row['url_id'],
                date=row['dish_date'],
                duration=duration,
                size=size,
                description=row['desrp'],
                favors=favors,
                views=views,
                comments=comments,
                trys=trys,
                author=author
            )

            Directory.set_recipe(recipe)

        # build recipe_part
        for i, row in df.iterrows():

            if len(row['ing_nm']) > 30:
                continue

            weight_str = row['ing_unit']
            weight = Directory.get_weight(weight_str)
            count = None
            unit = None
            if not weight:
                try:
                    token = Directory.UNIT_RE.findall(weight_str)[0]
                    count = token[-2]
                    if '/' in count:
                        count = convert_frac(count)
                    unit_str = token[-1]
                    unit = Directory.get_unit(unit_str)
                except:
                    pass

            recipe = Recipe(name=row['title'], url_id=row['url_id'])
            recipe = Directory.check_recipe(recipe)

            part_id = directory.get_part(row['ing_nm'])

            recipe_part = Recipe_Part(
                name=row['ing_nm'],
                part_id=part_id,
                recipe=recipe,
                weight=weight,
                count=count,
                unit=unit
            )

            Directory.set_recipe_part(recipe_part)


def parse_args(args):
    parser = ArgumentParser()
    parser.add_argument('--dbpath', help='sql connection here.', required=True)
    return parser.parse_args(args)


def main(args):
    args = parse_args(args)
    build(args.dbpath)


if __name__ == '__main__':
    main(sys.argv[1:])


