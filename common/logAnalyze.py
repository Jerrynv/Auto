# -*- coding:utf-8 -*-

import math
import re
import logging
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

        #print(tputlist)
        logging.debug('tputlist = {}'.format(tputlist))
        avg_tput, stddev_tput = calcStandardDev(tputlist)
        #print(avg_tput, stddev_tput)
        logging.info('avg_tput={}, stddev={}'.format(avg_tput, stddev_tput))

        #print(elapsedtimelist)
        logging.debug('elapsedtimelist = {}'.format(elapsedtimelist))
        avg_time, stddev_elapsedTime = calcStandardDev(elapsedtimelist)
        #print(avg_time, stddev_elapsedTime)
        logging.info('avg_time={}, stddev={}'.format(avg_time, stddev_elapsedTime))

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
        logging.info('-------------------- LOG Analyze Result --------------------')
        logging.info('------------------------------------------------------FAILED')
        return
    #print('tputlist={}'.format(tputlist))
    avg_tput, stdevValue_tput, stdev_tput = calcStandardEv(tputlist)
    #print("avg tput={}, stdev_tput={}".format(avg_tput, stdev_tput))
    logging.debug('tputlist={}'.format(tputlist))
    logging.info("avg tput={}, stdev_tput={}".format(avg_tput, stdev_tput))

    #print('elapsedtimelist={}'.format(elapsedtimelist))
    avg_time, stdevValue_elapsedTime, stdev_elapsedTime = calcStandardEv(elapsedtimelist)
    #print('avg time={}, stddev time={}'.format(avg_time, stdev_elapsedTime))
    logging.debug('elapsedtimelist={}'.format(elapsedtimelist))
    logging.info('avg time={}, stdev time={}'.format(avg_time, stdev_elapsedTime))

    #print('error bit list={}'.format(errorBitList))

    err = filter(lambda x:x>0, errorBitList)
    result = ''
    reason = ''
    if stdev_tput<5 and stdev_elapsedTime<5 and len(err)<=0:
        result, reason = 'pass', ''
    elif  stdev_tput>5:
        result, reason = 'FAILED', 'tput avg=%s stdev=%s, %s > 5' % (avg_tput, stdevValue_tput, stdev_tput)
    elif stdev_elapsedTime>5:
        result, reason = 'FAILED', 'elapsedtime avg=%s stdev=%s, %s > 5' % (avg_time, stdevValue_elapsedTime, stdev_elapsedTime)
    else:
    	result, reason = 'FAILED', 'bit error'

    #print('\n')
    print('-------------------- LOG Analyze Result --------------------')
    print('tput={}, avg tput={:.2f}, stdev tput={:.2f}'.format(tputlist, avg_tput, stdev_tput))
    print('elapsedtime={}, avg time={:.2f}, stdev time={:.2f}'.format(elapsedtimelist, avg_time, stdev_elapsedTime)) 
    print('bit error count={}'.format(errorBitList))
    print('--------------------------------------------------------{} {}\n'.format(result, reason))
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

def calcStandardEv(datalist): #mean squared error
    total = 0.0
    count = len(datalist)
    for i, data in enumerate(datalist):
        total += data

    avg = total/count

    variance = 0
    for i, data in enumerate(datalist):
        variance += math.pow((data-avg), 2)

    standardEVValue = math.sqrt(variance/(count))

    stdev = (standardEVValue/avg) * 100

    return avg, standardEVValue, float('%0.2f' % stdev)

if __name__ == '__main__':
    data1 = [95, 85, 75, 65, 55, 45]
    data2 = [73, 72, 71, 69, 68, 67]
    print('data1 stdev={}'.format(calcStandardEv(data1)))
    print(calcStandardEv(data2))
    #datafile = '/home/dgx/Jerry/cuPHY_Auto/logs/SNR7_80codewords_HalfPrecision-2019-12-26-23:13:29.txt'
    #datafile = '/home/dgx/Jerry/cuPHY_Auto/logs/MIMO1x8-2019-12-26-22:27:59.txt'
    cmd = '-p 4~42'
    match = re.compile(r'\d+~\d+', re.DOTALL)
    pValue = match.findall(cmd)[0].split('~')
    pMin, pMax = int(pValue[0]), int(pValue[1])
    print(type(pMin))
    for i in range(pMin, pMax+1, 1):
        newCmd = re.sub(match, str(i), cmd)
        #print(newCmd)
    #checkResult(datafile)
