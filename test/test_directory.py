
import sys, os
sys.path.append(os.path.abspath('..'))
from lbrrs.directory import Directory
from lbrrs.database import config

config.setup_session('postgresql+psycopg2://postgres:1qaz@WSX@104.199.238.161/lbrrs')


configs = Directory.get_configs()
'''
for config in configs:
    part_id, alias_id = Directory.classify(config, '冷飯')
    print(part_id, alias_id)
'''

d = Directory()

string = d.get_today_price('番茄')

print(string)
