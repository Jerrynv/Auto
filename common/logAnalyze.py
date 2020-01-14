# -*- coding:utf-8 -*-
import math
import re
import logging
from common import logMatch
from common.logsave import logger

def checkResult(logfile, suitename):
    logger.debug('log file : {}. suitename={}'.format(logfile, suitename))
    logContent = getLogContent(logfile)
    result, reason = 'PASS', ''

    if suitename == 'cuPHY_LDPC_Error_Correction' or \
       suitename == 'cuPHY_PUSCH_rx_pipeline' or \
       suitename == 'cuPHY_ldpc_decode_perf' or \
       suitename == 'cuPHY_PUSCH_rx_pipeline' or \
       suitename == 'cuPHY_LDPC_Error_Correction' or \
       suitename == 'cuPHY_PUSCH_LDPC_supported_code_block_sizes_BG1_BG2' or \
       suitename == 'cuPHY_PUSCH_LDPC_support_multiple_code_rates_including_HARQ_rate' or \
       suitename == 'cuPHY_PUSCH_Multi_TB_support_support':
        """
        check tput stddev < 5%
        check elapsedtime stddev < 5%
        check bit error count = 0
        """
        #result, reason = checkResultBycase(logContent, suitename)
        result, reason = analyze_bySuite(suitename, logContent)

    elif suitename == 'cuPHY_PDSCH_pipeline_integration':
        """
        CRC Error Count == 0
        LDPC Error Count == 0
        Rate Matching Error Count == 0
        0 mismatched QAM symbols
        DL pipeline: 96.59 us
        """
        result, reason = analyze_cuPHY_PDSCH_pipeline_integration(logContent)
    elif suitename == 'cuPHY_PUCCH_Format_1_complete':
        result, reason = analyze_cuPHY_PUCCH_Format_1_complete(logContent)
    elif suitename == 'PDCCH_Tx_Pipeline':
        result, reason = analyze_PDCCH_Tx_Pipeline(logContent)
    else:
        logger.warning('don\'t the suitename : {} log analyze, need more script support!'.format(suitename))

    return result, reason

def analyze_PDCCH_Tx_Pipeline(logContent):
    mismatchErrorCount = logMatch.getmisMatch_PDCCH_Tx_Pipeline(logContent)
    logger.info('-------------------- LOG Analyze Result --------------------')
    logger.info('mismatchErrorCount={}'.format(mismatchErrorCount))
    errMisMatch = filter(lambda x:x>0, mismatchErrorCount)

    result, reason = 'PASS', ''
    if len(mismatchErrorCount) == 0:
        result, reason = 'FAILED', 'the data is 0'
    if len(errMisMatch) > 0:
        result, reason = 'FAILED', 'mismatch count > 0'

    if result == 'PASS':
        logger.info('--------------------------------------------------------\033[32m{} \033[0m{}\n'.format(result, reason))
    else:
        logger.info('--------------------------------------------------------\033[31m{} \033[0m{}\n'.format(result, reason))

    return result, reason

def analyze_cuPHY_PUCCH_Format_1_complete(logContent):
    mismatchErrorCount = logMatch.getmisMatch_cuPHY_PUCCH_Format_1_complete(logContent)
    elapsedtimelist = logMatch.getelapseTime_cuPHY_PUCCH_Format_1_complete(logContent)

    errMisMatch = filter(lambda x:x>0, mismatchErrorCount)
    avg_time, stdevValue_elapsedTime, stdev_elapsedTime= calcStandardEv(elapsedtimelist)

    result, reason = logMatch.check_cuPHY_PUCCH_Format_1_complete(errMisMatch, stdev_elapsedTime)
    logger.info('-------------------- LOG Analyze Result --------------------')
    logger.info('mismatchErrorCount={}'.format(mismatchErrorCount))
    logger.info('elapsedtimelist={}'.format(elapsedtimelist))
    logger.info('elapsedtime={}, avg time={:.2f}, stdev time={:.2f}'.format(elapsedtimelist, avg_time, stdev_elapsedTime))

    if len(elapsedtimelist) == 0:
        result, reason = 'FAILED', 'the data is 0'

    if result == 'PASS':
        logger.info('--------------------------------------------------------\033[32m{} \033[0m{}\n'.format(result, reason))
    else:
        logger.info('--------------------------------------------------------\033[31m{} \033[0m{}\n'.format(result, reason))

    return result, reason

def analyze_cuPHY_PDSCH_pipeline_integration(logContent):
    crcErrorCount = logMatch.getCRCErrorCount_PDSCH_pipeline(logContent)
    ldpcErrorCount = logMatch.getLDPCErrorCount_PDSCH_pipeline(logContent)
    rateMatchErrorCount = logMatch.getRateMatchErrorCount_PDSCH_pipeline(logContent)
    mismatchErrorCount = logMatch.getMismatchCount_PDSCH_pipeline(logContent)
    elapsedtimelist = logMatch.getelapseTime_PDSCH_pipeline(logContent)

    errCrc = filter(lambda x:x>0, crcErrorCount)
    errLDPC = filter(lambda x:x>0, ldpcErrorCount)
    errRateMatch = filter(lambda x:x>0, rateMatchErrorCount)
    errMisMatch = filter(lambda x:x>0, mismatchErrorCount)
    avg_time, stdevValue_elapsedTime, stdev_elapsedTime= calcStandardEv(elapsedtimelist)

    result, reason = logMatch.check_PDSCH_pipe_AnalyzeResult(errCrc, errLDPC, errRateMatch, errMisMatch, stdev_elapsedTime)
    if len(elapsedtimelist) == 0:
        result, reason = 'FAILED', 'the data is 0'

    logger.info('-------------------- LOG Analyze Result --------------------')
    logger.info('crcErrorCount={}'.format(crcErrorCount))
    logger.info('ldpcErrorCount={}'.format(ldpcErrorCount))
    logger.info('rateMatchErrorCount={}'.format(rateMatchErrorCount))
    logger.info('mismatchErrorCount={}'.format(mismatchErrorCount))
    logger.info('elapsedtime={}, avg time={:.2f}, stdev time={:.2f}'.format(elapsedtimelist, avg_time, stdev_elapsedTime))

    if result == 'PASS':
        logger.info('--------------------------------------------------------\033[32m{} \033[0m{}\n'.format(result, reason))
    else:
        logger.info('--------------------------------------------------------\033[31m{} \033[0m{}\n'.format(result, reason))

    return result, reason

def analyze_bySuite(suitename, logContent):
    tputlist = logMatch.getTputList(suitename, logContent)
    elapsedtimelist = logMatch.getElapsedTimeList(suitename, logContent)
    errorBitList = logMatch.getErrorBitList(suitename, logContent)

    avg_tput, stdevValue_tput, stdev_tput = calcStandardEv(tputlist)
    avg_time, stdevValue_elapsedTime, stdev_elapsedTime = calcStandardEv(elapsedtimelist)
    errorBitcount = filter(lambda x:x>0, errorBitList)

    result, reason = logMatch.check_AnalyzeResult_bySuite(stdev_tput, stdev_elapsedTime, errorBitcount)
    if len(tputlist) == 0 or len(elapsedtimelist) == 0 or len(errorBitList) == 0:
        result, reason = 'FAILED', 'the data is 0'

    logger.info('-------------------- LOG Analyze Result --------------------')
    logger.info('tput={}, avg tput={:.2f}, stdev tput={:.2f}'.format(tputlist, avg_tput, stdev_tput))
    logger.info('elapsedtime={}, avg time={:.2f}, stdev time={:.2f}'.format(elapsedtimelist, avg_time, stdev_elapsedTime))
    logger.info('bit error count={}'.format(errorBitList))
    if result == 'PASS':
        logger.info('--------------------------------------------------------\033[32m{} \033[0m{}\n'.format(result, reason))
    else:
        logger.info('--------------------------------------------------------\033[31m{} \033[0m{}\n'.format(result, reason))

    return result, reason

def checkResultBycase(logContent, suitename):
    tputlist = logMatch.getTputList(suitename, logContent)
    elapsedtimelist = logMatch.getElapsedTimeList(suitename, logContent)
    errorBitList = logMatch.getErrorBitList(suitename, logContent)

    if len(tputlist) == 0 or len(elapsedtimelist) ==0:
        logger.info('-------------------- LOG Analyze Result --------------------')
        logger.info('------------------------------------------------------FAILED')
        return 'FAILED', ''
    avg_tput, stdevValue_tput, stdev_tput = calcStandardEv(tputlist)
    logger.debug('tputlist={}'.format(tputlist))
    logger.debug("avg tput={}, stdev_tput={}".format(avg_tput, stdev_tput))

    avg_time, stdevValue_elapsedTime, stdev_elapsedTime = calcStandardEv(elapsedtimelist)
    logger.debug('elapsedtimelist={}'.format(elapsedtimelist))
    logger.debug('avg time={}, stdev time={}'.format(avg_time, stdev_elapsedTime))

    err = filter(lambda x:x>0, errorBitList)
    result = ''
    reason = '\033[0m'
    if stdev_tput<5 and stdev_elapsedTime<5 and len(err)<=0:
        result, reason = 'PASS', ''
    elif  stdev_tput>5:
        result, reason = 'FAILED', 'tput avg=%s stdev=%s, %s > 5' % (avg_tput, stdevValue_tput, stdev_tput)
    elif stdev_elapsedTime>5:
        result, reason = 'FAILED', 'elapsedtime avg=%s stdev=%s, %s > 5' % (avg_time, stdevValue_elapsedTime, stdev_elapsedTime)
    else:
        result, reason = 'FAILED', 'bit error>0'

    #print('\n')
    logger.info('-------------------- LOG Analyze Result --------------------')
    logger.info('tput={}, avg tput={:.2f}, stdev tput={:.2f}'.format(tputlist, avg_tput, stdev_tput))
    logger.info('elapsedtime={}, avg time={:.2f}, stdev time={:.2f}'.format(elapsedtimelist, avg_time, stdev_elapsedTime)) 
    logger.info('bit error count={}'.format(errorBitList))
    if result == 'PASS':
        logger.info('--------------------------------------------------------\033[32m{} \033[0m{}\n'.format(result, reason))
    else:
        logger.info('--------------------------------------------------------\033[31m{} \033[0m{}\n'.format(result, reason))
    #logger.debug('\033[0m')
    #print('------------------------------------------------------------')
    return result, reason

def getLogContent(logfile):
    logContent = ''
    with open(logfile, 'r') as f:
        logContent = f.read()

    return logContent

###

def calcStandardEv(datalist): #mean squared error
    total = 0.0
    count = len(datalist)
    if count == 0:
        logger.error('the data list len is 0')
        return 0, 0, 0

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
