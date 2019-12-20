# -*- coding: utf-8 -*-
import os
from common import testcase_Parse


def run_testCase(caseName):
    caseCmds = testcase_Parse.gettestcaseCmdList("single", caseName)
    
#    os.system([cmd for cmd in caseCmds if '#' not in cmd and cmd.strip() != ''])

    for cmd in caseCmds:
        if '#' not in cmd and cmd.strip() != '':
            print("cmd={}".format(cmd.strip()))
            if 'sudo' in cmd[:3]:
                 password = "dgxqa"
                 os.system('echo %s | sudo -S %s' % (password, cmd.strip()))                 
            else:
                os.system(cmd.strip())
