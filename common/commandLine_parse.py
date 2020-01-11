# -*- coding: utf-8 -*-
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description = "description")
    parser.add_argument('--curan', help='specify local cuda ran sdk path', nargs=1)
    parser.add_argument('--case', '-c', help='show the case to be tested, all will test all case', nargs=1)
    parser.add_argument('--iter', '-i',nargs='?', help='run times', default=1, type=int, const=1)
    parser.add_argument('--duration', '-t', nargs='?', help='run time', default=0, type=int, const=0)
    parser.add_argument('--pkg', '-p', nargs='?', help='package type: binary or src or stress', choices=['binary','src', 'stress'], default='binary', type=str, const='binary')
    parser.add_argument('-f', help='force to update to latest package', action='store_true')
    return parser.parse_args()
