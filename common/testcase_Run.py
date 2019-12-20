# -*- coding: utf-8 -*-
import os
import io
from common import testcase_Parse


def run_testCase(caseName, curan_path):
    caseCmds = testcase_Parse.gettestcaseCmdList("single", caseName)
    print("caseCmds:{}".format(caseCmds))
    logname = caseCmds[0].strip().replace('\n', '').strip().split(':')[-1].strip()

    createFile('logs/%s.txt' % logname)

    for cmd in caseCmds:
        if '#####' in cmd or cmd.strip() == '':
            pass
        else:
            cmd = convertCmdToAbspath(cmd, curan_path)
            if 'sudo' in cmd:
                password = 'dgxqa'
                os.system('echo %s | sudo -S %s > log.txt' % (password, cmd))

            else:
                os.system('%s > log.txt' % cmd)

            with open('logs/%s.txt' % logname, 'a+') as f:
                f.write(cmd)
                f.write('\n')

            copyLog('log.txt', 'logs/%s.txt' % logname)
            os.remove('log.txt')


def convertCmdToAbspath(cmd, curan_path):
    cmd = cmd.strip().replace('\n', '')
    cmd = cmd.replace('cuPHY/build/', '/'.join([curan_path, 'cuPHY/build/']))
    cmd = cmd.replace('./testVectors', '/'.join([curan_path,'/testVectors']))
    print('convertCmdToAbspath={}'.format(cmd))
    return cmd

def createFolder(folder):
    currenWorkPath = os.getcwd()
    folder = folder.strip()
    folder = folder.rstrip("\\")

    path = '/'.join([currenWorkPath, folder])

    isExists=os.path.exists(path)

    if not isExists:
        os.makedirs(path)
        print('create folder logs successfully!')
        return True
    else:
        print('folder logs exists')
        return False

def createFile(filename):
    path = filename[0:filename.rfind("/")]

    if not os.path.isdir(path):
        os.makedirs(path)

    if not os.path.isfile(filename):
        fd = io.open(filename, mode="w", encoding="utf-8")
        fd.close()
    else:
        pass

def copyLog(srcfile, dstfile):
    with open(srcfile, 'r') as srcfh:
        with open(dstfile, 'a+') as dstfh:
            dstfh.write(srcfh.read())
            dstfh.write('\n')