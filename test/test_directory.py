#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys, os
sys.path.append(os.path.abspath('..'))
from lbrrs.directory import Directory
from lbrrs.database import config

config.setup_session('postgresql+psycopg2://postgres:1qaz@WSX@104.199.238.161/lbrrs')


configs = Directory.get_configs()

d = Directory()

result = d.get_today_recipe('雞腿')

print(result)