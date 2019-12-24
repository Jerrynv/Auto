# -*- coding: utf-8 -*-
import os
import io
import datetime
import time
from common import testcase_Parse


def run_testCase(caseName, curan_path, arguementList):
    caseCmds = testcase_Parse.gettestcaseCmdList("single", caseName)
 #   print("caseCmds:{}".format(caseCmds))

    runSinglecase(caseCmds, curan_path, arguementList)

def runSinglecase(caseCmds, curan_path, arguementList):
    logname = caseCmds[0].strip().replace('\n', '').strip().split(':')[-1].strip()
    logname = '-'.join([logname, getcurrDate()])

    tempfile = 'log.txt'

    if arguementList.duration == 0:
        for cmd in caseCmds:
            if '#####' in cmd or cmd.strip() == '':
                continue
            else:
                cmd = convertCmdToAbspath(cmd, curan_path)
                for i in range(arguementList.iter):
                    runCommand(cmd, tempfile)
                    writelog(tempfile, 'logs/%s.txt' % logname, cmd)
                    os.remove(tempfile)
    else:
        starttime = time.time()
        while ((time.time()-starttime)/60) < arguementList.duration:
            for cmd in caseCmds:
                if '#####' in cmd or cmd.strip() == '':
                    continue
                else:
                    cmd = convertCmdToAbspath(cmd, curan_path)
                    runCommand(cmd, tempfile)
                    writelog(tempfile, 'logs/%s.txt' % logname, cmd)
                    os.remove(tempfile)

def runCommand(cmd, logfile):
    if 'sudo' in cmd:
        password = 'dgxqa'
        os.system('echo %s | sudo -S %s > %s' % (password, cmd, logfile))
    else:
        os.system('%s > %s' % (cmd, logfile))

def convertCmdToAbspath(cmd, curan_path):
    cmd = cmd.strip().replace('\n', '')
    cmd = cmd.replace('cuPHY/build/', '/'.join([curan_path, 'cuPHY/build/']))
    cmd = cmd.replace('./testVectors', '/'.join([curan_path,'testVectors']))
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

def writelog(srcfile, dstfile, header):
    with open(dstfile, 'a+') as f:
        f.write(header + '\n')
        f.write('*****start time {}'.format(getcurrDate()) + '\n')
    copyLog(srcfile, dstfile)
    with open(dstfile, 'a+') as f:
        f.write('*****End time {}'.format(getcurrDate()))
        f.write('\n\n')

def run_alltestcases(caseName, curan_path, iter=1, time=0):
    caseCmds = testcase_Parse.gettestcaseCmdList("single", caseName)

    caselist = seperateTestcase(caseCmds)
    for i, case in enumerate(caselist):
        runSinglecase(case, curan_path)

def seperateTestcase(allcases):
    caseNamePos = []
    casebuff = []

    for i, case in enumerate(allcases):
        if '#####' in case:
            caseNamePos.append(i)
    caseNamePos.append(len(allcases))

    for i in range(len(caseNamePos)-1):
        casebuff.append(allcases[caseNamePos[i]:caseNamePos[i+1]])

    return casebuff

def getcurrDate():
    return datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')  
