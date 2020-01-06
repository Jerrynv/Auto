# -*- coding: utf-8 -*-
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description = "description")
    parser.add_argument('--curan', nargs=1)
    parser.add_argument('--case', nargs=1)
    parser.add_argument('--all_case', action='store_true')
    parser.add_argument('--iter', '-i',nargs='?', default=1, type=int, const=True)
    parser.add_argument('--duration', '-t', nargs='?', default=0, type=int, const=True)
    parser.add_argument('--analyze', '-a', action='store_true')
    parser.add_argument('--pkg', '-p', nargs='?', default='binary', type=str, const=True)
    return parser.parse_args()
