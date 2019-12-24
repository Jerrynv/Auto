# -*- coding: utf-8 -*-
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description = "description")
    parser.add_argument('--curan', nargs=1, required=True)
    parser.add_argument('--case', nargs=1)
    parser.add_argument('--all_case', action='store_true')
    parser.add_argument('--iter', nargs='?', default=1, type=int, const=True)
    parser.add_argument('--duration', nargs='?', default=0, type=int, const=True)
    parser.add_argument('--analyze', '-a', action='store_true')
    return parser.parse_args()
