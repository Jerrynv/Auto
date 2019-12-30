# -*- coding:utf-8 -*-

import math
import re
import logMatch

def checkResult(logfile):
    suitename, logContent = getsuiteNameAndLog(logfile)
    if suitename == 'cuPHY_LDPC_Error_Correction' or \
       suitename == 'cuPHY_PUSCH_rx_pipeline':
        """
        check tput stddev < 5%
        check elapsedtime stddev < 5%
        check bit error count = 0
        """
        tputlist = logMatch.getTputList(suitename, logContent)
        elapsedtimelist = logMatch.getElapsedTimeList(suitename, logContent)
        errorBitList = logMatch.getErrorBitList(suitename, logContent)

        print(tputlist)
        avg_tput, stddev_tput = calcStandardDev(tputlist)
        print(avg_tput, stddev_tput)

        print(elapsedtimelist)
        avg_time, stddev_elapsedTime = calcStandardDev(elapsedtimelist)
        print(avg_time, stddev_elapsedTime)

        print(errorBitList)

    elif suitename == 'cuPHY_PUSCH_rx_pipeline':
        """
        check tput stddev < 5%
        check elapsedtime stddev < 5%
        check  Block Error Rate = 0
        """
    pass

def checkResultBycase(logfile, suitename):
    logContent = ''
    with open(logfile, 'r') as f:
        logContent = f.read()
        #print('log={}'.format(logContent))
    tputlist = logMatch.getTputList(suitename, logContent)
    elapsedtimelist = logMatch.getElapsedTimeList(suitename, logContent)
    errorBitList = logMatch.getErrorBitList(suitename, logContent)

    if len(tputlist) == 0 or len(elapsedtimelist) ==0:
        print('-------------------- LOG Analyze Result --------------------')
        print('------------------------------------------------------FAILED')
        return
    #print('tputlist={}'.format(tputlist))
    avg_tput, stddev_tput = calcStandardDev(tputlist)
    #print("avg tput={}, stddev_tput={}".format(avg_tput, stddev_tput))


    #print('elapsedtimelist={}'.format(elapsedtimelist))
    avg_time, stddev_elapsedTime = calcStandardDev(elapsedtimelist)
    #print('avg time={}, stddev time={}'.format(avg_time, stddev_elapsedTime))

    #print('error bit list={}'.format(errorBitList))

    err = filter(lambda x:x>0, errorBitList)
    result = 'pass' if stddev_tput<5 and stddev_elapsedTime<5 and len(err)<=0 else 'FAILED'
    print('\n')
    print('-------------------- LOG Analyze Result --------------------')
    print('tput            = {}, avg tput={:.2f}, stddev tput={:.2f}'.format(tputlist, avg_tput, stddev_tput))
    print('elapsedtime     = {}, avg time={:.2f}, stddev time={:.2f}'.format(elapsedtimelist, avg_time, stddev_elapsedTime)) 
    print('bit error count = {}'.format(errorBitList))
    print('------------------------------------------------------{}'.format(result))
    #print('------------------------------------------------------------')
    #print('\n')

def getsuiteNameAndLog(logfile):
    suitename = ''
    logContent = ''
    with open(logfile, 'r') as f:
        logContent = f.read()
        f.seek(0,0)
        suitename = f.readlines()[2].split(':')[0].strip().split(' ')[1]

    return suitename, logContent


###

def calcStandardDev(datalist): #mean squared error
    total = 0.0
    count = len(datalist)
    for i, data in enumerate(datalist):
        total += data

    avg = total/count

    variance = 0
    for i, data in enumerate(datalist):
        variance += math.pow((data-avg), 2)

    standardDevValue = math.sqrt(variance/count)

    stddev = (standardDevValue/avg) * 100

    return avg, float('%0.2f' % stddev)

if __name__ == '__main__':
    data = [1.1, 1.2, 1.3, 1.4, 1.5]
    #print(calcStandardDev(data))
    #datafile = '/home/dgx/Jerry/cuPHY_Auto/logs/SNR7_80codewords_HalfPrecision-2019-12-26-23:13:29.txt'
    #datafile = '/home/dgx/Jerry/cuPHY_Auto/logs/MIMO1x8-2019-12-26-22:27:59.txt'
    cmd = '-p 4~42'
    match = re.compile(r'\d+~\d+', re.DOTALL)
    pValue = match.findall(cmd)[0].split('~')
    pMin, pMax = int(pValue[0]), int(pValue[1])
    print(type(pMin))
    for i in range(pMin, pMax+1, 1):
        newCmd = re.sub(match, str(i), cmd)
        print(newCmd)
    #checkResult(datafile)
