# -*- coding: utf-8 -*-
import os

testcaseFileName = 'cuPHY_Auto/testcase/caselist.txt'
currenWorkPath = os.getcwd()

testcaseFile_path = os.path.join(currenWorkPath, testcaseFileName)

def gettestcaseCmdList(testType, testInput):
    """
    if testType is single, testInput is the case name
    if testType is suite, testInput is the suite name
    """
    bFindCase = False
    start_pos = 0
    print("testInput={}".format(testInput))
    
    with open(testcaseFile_path, 'r') as f:
        if testInput != 'all_case':
            for line_no, line in enumerate(f):
                if testInput in line and '#####' in line:
                    start_pos = line_no
                    bFindCase = True
                if testInput not in line and '#####' in line and bFindCase == True:
                    f.seek(0, 0)
                    return (f.readlines()[start_pos+1:line_no-1])
        else:
            return f.readlines()