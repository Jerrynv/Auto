# -*- coding: UTF-8 -*-
import os
import logging
import shutil
from common import commandLine_parse
from common import testcase_Parse
from common import testcase_Run
from common import logsave
from common import preparation
from common.logsave import logger


def checkcuRanSdkFolder(args, pkgFolder):
    pkgpath = os.path.join(os.getcwd(), pkgFolder)
    for root, dirs, files in os.walk(pkgpath, topdown=True):
        for i in dirs:
            if (args.pkg == 'binary' or args.pkg == 'stress') and 'cuda-ran-sdk' in i and root == pkgpath:
                return i
            if args.pkg == 'src' and 'cuPHY' in i and root == pkgpath:
                return i
    return ''

def getcudaransdk(args, pkgFolder):
    cuRanSdkexistFolder = checkcuRanSdkFolder(args, pkgFolder)
    if cuRanSdkexistFolder != '':
        logger.debug("cuRanSdkexistFolder : {}".format(cuRanSdkexistFolder))
    else:
        logger.debug("the cuRan sdk folder don't exist, will create it")
    cuda_ran_sdk = args.curan[0] if args.curan != None else preparation.doPrepare(cuRanSdkexistFolder, args, pkgFolder)

    return cuda_ran_sdk

if __name__ == '__main__':
    args = commandLine_parse.parse_args()
    pkgFolder = 'pkg'
    testcase_Run.createFolder('logs')
    testcase_Run.createFolder(pkgFolder)


    logger.info("args:{}".format(args))
    cuda_ran_sdk = getcudaransdk(args, pkgFolder)

    logger.info('the running cuda_ran_sdk folder : {}'.format(cuda_ran_sdk))
    
    if args.case:
        testcase_Run.run_testcase(args.case[0], cuda_ran_sdk, args)
    elif args.all_case:
        print("run all cases")
        testcase_Run.run_allTestcase("all_case", args.curan[0], args)
    elif args.analyze:
        print("analyze the log")


