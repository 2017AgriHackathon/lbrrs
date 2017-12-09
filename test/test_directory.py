import sys, os
sys.path.append(os.path.abspath('..'))
from argparse import ArgumentParser
from lbrrs.directory import Directory
from lbrrs.database import config

config.setup_session('postgresql+psycopg2://postgres:1qaz@WSX@104.199.238.161/lbrrs')


configs = Directory.get_configs()

d = Directory()


def parse_args(args):
    parser = ArgumentParser()
    parser.add_argument('--name', required=True)
    return parser.parse_args()


def main(args):
    args = parse_args(args)
    result = d.get_today_price(args.name)
    print(result)


if __name__ == '__main__':

    main(sys.argv[1:])