# -*- coding: UTF-8 -*-
import os
from common import commandLine_parse
from common import testcase_Parse
from common import testcase_Run


if __name__ == '__main__':
    args = commandLine_parse.parse_args()
    print("args:{}".format(args))

    if args.case:
        print("run the case")
        testcase_Run.run_testCase(args.case[0], args.curan[0], args)
    elif args.all_case:
        print("run all cases")
        testcase_Run.run_alltestcases("all_case", args.curan[0], args)
    elif args.analyze:
        print("analyze the log")

