# -*- coding: utf-8 -*-
import os
from common.logsave import logger

testcaseFileName = 'testcase/caselist.txt'
currenWorkPath = os.getcwd()

testcaseFile_path = os.path.join(currenWorkPath, testcaseFileName)

def gettestcaseCmdList(testInput, args):
    bFindCase = False
    start_pos = 0

    testcaseFileName = 'testcase/caselist_binary.txt' if args.pkg=='binary' else 'testcase/caselist_src.txt'

    currenWorkPath = os.getcwd()
    testcaseFile_path = os.path.join(currenWorkPath, testcaseFileName)
    
    with open(testcaseFile_path, 'r') as f:
        if testInput == 'all' or testInput == 'all_case':
            return f.readlines()
        else:
            for line_no, line in enumerate(f):
                if testInput in line and '#####' in line:
                    start_pos = line_no
                    bFindCase = True

                if testInput not in line and '#####' in line and bFindCase == True:
                    f.seek(0, 0)
                    return (f.readlines()[start_pos:line_no-1])
