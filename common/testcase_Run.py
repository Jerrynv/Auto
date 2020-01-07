# -*- coding: utf-8 -*-
import os
import io
import datetime
import time
import re
from common import testcase_Parse
from common import logAnalyze
from common.logsave import logger

def run_testcase(caseName, curan_path, arguementList):
    logger.info('start run the case ...\n')
    if caseName == 'all_case' or caseName == 'all':
        run_allTestcase(caseName, curan_path, arguementList)
    else:
        run_singleTestcase(caseName, curan_path, arguementList)

def run_singleTestcase(caseName, curan_path, arguementList):
    caseCmds = testcase_Parse.gettestcaseCmdList(caseName, arguementList)

    runCases(caseCmds, curan_path, arguementList)

def runCases(caseCmds, curan_path, arguementList):
    logger.info('casecmd={}'.format(caseCmds))
    casename = caseCmds[0].strip().replace('\n', '').strip().split(':')[-1].strip()
    suitename = caseCmds[0][5:]

    logname = '-'.join([casename, getcurrDate()])

    tempfile = 'logs/log.txt'
    if checkFileStatus(tempfile):
        os.remove(tempfile)

    for cmd in caseCmds:
        if '#' in cmd or cmd.strip() == '':
            continue
        elif suitename.split(':')[0].strip() == 'cuPHY_PUSCH_LDPC_support_multiple_code_rates_including_HARQ_rate':
            runParticularCase_cuPHY_PUSCH_LDPC_support_multiple_code_rates_including_HARQ_rate(cmd, suitename, curan_path, tempfile, logname, arguementList.duration, arguementList.iter)
        else:
            cmd = convertCmdToAbspath(cmd, curan_path, arguementList.pkg)
            runCommandsAndSaveLog(cmd, arguementList.iter, arguementList.duration, tempfile, logname, suitename)

def runCommandsAndSaveLog(cmd, iter_times, duration, temp_file, logname, suitename):
    if (duration == 0):
        logger.info('run case {} times:'.format(iter_times))
        logger.info('{}'.format(cmd))
        loopRunCommand_byiter(cmd, iter_times, temp_file)
    else:
        logger.info('run case in {} minutes:'.format(duration))
        logger.info('{}'.format(cmd))
        loopRunCommand_bytime(cmd, duration, temp_file)

    logAnalyze.checkResultBycase(temp_file, suitename.split(':')[0].strip())

    writelog(temp_file, 'logs/%s.txt' % logname, cmd, suitename)
    os.remove(temp_file)

def loopRunCommand_byiter(cmd, iter_times, temp_file):
    for i in range(iter_times):
        runCommand(cmd, temp_file)

def loopRunCommand_bytime(cmd, duration, temp_file):
    starttime = time.time()
    while ((time.time()-starttime)/60) < duration:
        runCommand(cmd, temp_file)

def runCommand(cmd, logfile):
    if 'sudo' in cmd:
        password = 'dgxqa'
        os.system('echo %s | sudo -S %s >> %s' % (password, cmd, logfile))
    else:
        os.system('%s >> %s' % (cmd, logfile))

def convertCmdToAbspath(cmd, curan_path, pkg='binary'):
    cmd = cmd.strip().replace('\n', '')
    if pkg == 'binary':
        cmd = cmd.replace('build/', '/'.join([curan_path, 'cuPHY/build/']))
        cmd = cmd.replace('./testVectors', '/'.join([curan_path,'testVectors']))
    elif pkg == 'src':
        cmd = cmd.replace('build/', '/'.join([curan_path, 'build/']))
        cmd = cmd.replace('./testVectors', '/'.join([curan_path,'testVectors']))

    return cmd

def runParticularCase_cuPHY_PUSCH_LDPC_support_multiple_code_rates_including_HARQ_rate(cmd, suitename, curan_path, tempfile, logname, duration = 0, iter_times=1):
    match = re.compile(r'\d+~\d+', re.DOTALL)
    pValue = match.findall(cmd)[0].split('~')
    pMin, pMax = int(pValue[0]), int(pValue[1])

    for i in range(pMin, pMax+1, 1):
        newCmd = re.sub(match, str(i), cmd)
        newCmd = convertCmdToAbspath(newCmd, curan_path)
        runCommandsAndSaveLog(newCmd, iter_times, duration, tempfile, logname, suitename)

def runOneCaseAndAnalyze(cmd, curan_path):
    pass      

def createFolder(folder):
    currenWorkPath = os.getcwd()
    folder = folder.strip()
    folder = folder.rstrip("\\")

    path = '/'.join([currenWorkPath, folder])

    isExists=os.path.exists(path)

    if not isExists:
        os.makedirs(path)
        return True
    else:
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

def checkFileStatus(filename):
    return True if os.path.isfile(filename) else False

def copyLog(srcfile, dstfile):
    with open(srcfile, 'r') as srcfh:
        with open(dstfile, 'a+') as dstfh:
            dstfh.write(srcfh.read())
            dstfh.write('\n')

def writelog(srcfile, dstfile, cmds, suitename):
    with open(dstfile, 'a+') as f:
        f.write(cmds + '\n')
        f.write('*****start time {}'.format(getcurrDate()) + '\n')
        f.write('*****run {}'.format(suitename) + '\n')
    copyLog(srcfile, dstfile)
    with open(dstfile, 'a+') as f:
        f.write('*****End time {}'.format(getcurrDate()))
        f.write('\n\n')

def run_allTestcase(caseName, curan_path, arguementList):
    caseCmds = testcase_Parse.gettestcaseCmdList(caseName, arguementList)

    caselist = seperateTestcase(caseCmds)

    for i, case in enumerate(caselist):
        runCases(case, curan_path, arguementList)

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
