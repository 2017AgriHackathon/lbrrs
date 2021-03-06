#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
from argparse import ArgumentParser
from .database import config
from .directory import Directory
from . import marketbrowser, marketapi


def build(db_path, setup, reclassify):
    if db_path:
        config.setup_session(db_path)
        if setup:
            config.init()
            return

        if reclassify:
            # Withdraw all product & recipe_part & crops
            products = Directory.get_products()
            recipe_parts = Directory.get_recipe_parts()
            crops = Directory.get_crops()
            # Reset parts & aliases
            config.reset_parts_aliases()
            # Reclassify
            Directory.re_classify(crops)
            Directory.re_classify(products)
            Directory.re_classify(recipe_parts)
            return

        w = marketbrowser.WellcomeBrowser()
        w.direct()

        g = marketbrowser.GeantBrowser()
        g.direct()

        f = marketbrowser.FengKangBrowser()
        f.direct()

        r1 = marketbrowser.RtmartBrowser()
        r1.direct()

        r2 = marketapi.Rtmart()
        r2.direct()

        c1 = marketapi.Carrefour()
        c1.direct()

        c2 = marketapi.CarrfourBrowser()
        c2.direct()

#       b = marketapi.BinJung()
#       b.direct()

#       n = marketapi.NewTaipeiCenter()
#       n.direct()

        Directory.clear_stack()


def parse_args(args):
    parser = ArgumentParser()
    parser.add_argument('--dbpath', help='sql connection here.', required=True)
    parser.add_argument('--setup', help='present to initialize database.', action='store_true')
    parser.add_argument('--reclassify', help='present to reset configs then do re-classify.', action='store_true')
    return parser.parse_args()


def main(args):
    args = parse_args(args)
    build(args.dbpath, args.setup, args.reclassify)


if __name__ == '__main__':
    main(sys.argv[1:])
