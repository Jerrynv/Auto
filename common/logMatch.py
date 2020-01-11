# -*- coding: utf-8 -*-
import re
from common.logsave import logger

### API
def getTputList(suitename, log):
    if suitename == 'cuPHY_LDPC_Error_Correction' \
        or suitename == 'cuPHY_ldpc_decode_perf' \
        or suitename == 'cuPHY_PUSCH_LDPC_supported_code_block_sizes_BG1_BG2' \
        or suitename == 'cuPHY_PUSCH_LDPC_support_multiple_code_rates_including_HARQ_rate':
        return getTputList_LDPC_Error_Correction(suitename, log)
    elif suitename == 'cuPHY_PUSCH_rx_pipeline' \
        or suitename == 'cuPHY_PUSCH_Multi_TB_support_support':
        return getTputList_cuPHY_PUSCH_rx_pipeline(suitename, log)

    logger.warning('not found any tput suitename = {}, log = {}'.format(suitename, log))

def getElapsedTimeList(suitename, log):
    if suitename == 'cuPHY_LDPC_Error_Correction' \
        or suitename == 'cuPHY_ldpc_decode_perf' \
        or suitename == 'cuPHY_PUSCH_LDPC_supported_code_block_sizes_BG1_BG2' \
        or suitename == 'cuPHY_PUSCH_LDPC_support_multiple_code_rates_including_HARQ_rate':
        return getElapsedTimeList_LDPC_Error_Correction(suitename, log)
    elif suitename == 'cuPHY_PUSCH_rx_pipeline' \
        or suitename == 'cuPHY_PUSCH_Multi_TB_support_support':
        return getElapsedTimeList_cuPHY_PUSCH_rx_pipeline(suitename, log)
    logger.warning('not found any time suitename = {}, log = {}'.format(suitename, log))

def getErrorBitList(suitename, log):
    if suitename == 'cuPHY_LDPC_Error_Correction' \
        or suitename == 'cuPHY_ldpc_decode_perf' \
        or suitename == 'cuPHY_PUSCH_LDPC_supported_code_block_sizes_BG1_BG2' \
        or suitename == 'cuPHY_PUSCH_LDPC_support_multiple_code_rates_including_HARQ_rate':
        return getErrorBitList_cuPHY_LDPC_Error_Correction(suitename, log)
    elif suitename == 'cuPHY_PUSCH_rx_pipeline' \
        or suitename == 'cuPHY_PUSCH_Multi_TB_support_support':
        return getErrorBitList_cuPHY_PUSCH_rx_pipeline(suitename, log)

    logger.warning('not found any time suitename = {}, log = {}'.format(suitename, log))

def selectTputPattern(suitename):
    if suitename == 'cuPHY_LDPC_Error_Correction' \
        or suitename == 'cuPHY_ldpc_decode_perf' \
        or suitename == 'cuPHY_PUSCH_LDPC_supported_code_block_sizes_BG1_BG2' \
        or suitename == 'cuPHY_PUSCH_LDPC_support_multiple_code_rates_including_HARQ_rate':
        return tputMatchPattern_LDPC_Error_Correction()
    elif suitename == 'cuPHY_PUSCH_rx_pipeline' \
        or suitename == 'cuPHY_PUSCH_Multi_TB_support_support':
        return tputMatchPattern_cuPHY_PUSCH_rx_pipeline()

    logger.warning('not found suitable suitename = {}'.format(suitename))

def selectElapsedTimePattern(suitename):
    if suitename == 'cuPHY_LDPC_Error_Correction' \
        or suitename == 'cuPHY_ldpc_decode_perf' \
        or suitename == 'cuPHY_PUSCH_LDPC_supported_code_block_sizes_BG1_BG2' \
        or suitename == 'cuPHY_PUSCH_LDPC_support_multiple_code_rates_including_HARQ_rate':
        return elapsedTimeMatchPattern_LDPC_Error_Correction()
    elif suitename == 'cuPHY_PUSCH_rx_pipeline' \
        or suitename == 'cuPHY_PUSCH_Multi_TB_support_support':
        return elapsedTimeMatchPattern_cuPHY_PUSCH_rx_pipeline()

    logger.warning('not found suitable suitename = {}'.format(suitename))

def selectErrratePattern(suitename):
    if suitename == 'cuPHY_LDPC_Error_Correction' \
        or suitename == 'cuPHY_ldpc_decode_perf' \
        or suitename == 'cuPHY_PUSCH_LDPC_supported_code_block_sizes_BG1_BG2' \
        or suitename == 'cuPHY_PUSCH_LDPC_support_multiple_code_rates_including_HARQ_rate':
        return ErrrateMatchPattern_LDPC_Error_Correction()
    elif suitename == 'cuPHY_PUSCH_rx_pipeline' \
        or suitename == 'cuPHY_PUSCH_Multi_TB_support_support':
        return ErrrateMatchPattern_cuPHY_PUSCH_rx_pipeline()

    logger.warning('not found suitable suitename = {}'.format(suitename))


##### for suite LDPC_Error_Correction
    """
    Workspace size: 0 bytes
    Average (1 runs) elapsed time in usec = 206.8, throughput = 0.04 Gbps
    K = 8448, numCodeblocks = 1
    bit error count = 0, bit error rate (BER) = (0 / 8448) = 0.00000e+00, block error rate (BLER) = (0 / 1) = 0.00000e+00
    """
def tputMatchPattern_LDPC_Error_Correction():

    pattern = re.compile(r'throughput = \d+\.\d+ Gbps', re.DOTALL)
    return pattern

def elapsedTimeMatchPattern_LDPC_Error_Correction():
    pattern = re.compile(r'elapsed time in usec = \d+\.\d+', re.DOTALL)
    return pattern

def ErrrateMatchPattern_LDPC_Error_Correction():
    pattern = re.compile(r'bit error count = \d+', re.DOTALL)
    return pattern

def getTputList_LDPC_Error_Correction(suitename, log):
    match = selectTputPattern(suitename).findall(log)

    tputlist = []
    if match:
        for i in match:
            tput = i.split(' ')[-2]
            tputlist.append(float(tput))
    return tputlist

def getElapsedTimeList_LDPC_Error_Correction(suitename, log):
    match = selectElapsedTimePattern(suitename).findall(log)

    lapsedTimelist = []
    if match:
        for i in match:
            lapsedTime = i.split(' ')[-1]
            lapsedTimelist.append(float(lapsedTime))
    return lapsedTimelist

def getErrorBitList_cuPHY_LDPC_Error_Correction(suitename, log):
    match = selectErrratePattern(suitename).findall(log)

    errBitList = []
    if match:
        for i in match:
            errorBit = i.split(' ')[-1]
            errBitList.append(float(errorBit))
    return errBitList
##### for suite LDPC_Error_Correction


##### for suite cuPHY_PUSCH_rx_pipeline
    """
    PuschRx Pipeline[0]: Metric - Throughput            : 0.1125 Gbps (encoded input bits 50208) 
    PuschRx Pipeline[0]: Metric - Block Error Rate      : 0.0000 (Error CBs 0, Total CBs 6)
    PuschRx Pipeline[0]: Metric - Average execution time: 446.4343 usec (over 1000 runs, using CUDA event)
    PuschRx Pipeline[0]: Metric - Average execution time (excluding start delay): 446.4292 usec (over 1000 runs, using CUDA event)
    PuschRx Pipeline[0]: Kernel launch start delay: 5.1200 usec, amortized per run 0.0051 usec (over 1000 runs, using CUDA event)
   """
def tputMatchPattern_cuPHY_PUSCH_rx_pipeline():
    pattern = re.compile(r'Metric - Throughput            : \d+\.\d+ Gbps', re.DOTALL)
    return pattern

def elapsedTimeMatchPattern_cuPHY_PUSCH_rx_pipeline():
    pattern = re.compile(r'Metric - Average execution time: \d+\.\d+ usec', re.DOTALL)
    return pattern

def ErrrateMatchPattern_cuPHY_PUSCH_rx_pipeline():
    pattern = re.compile(r'Metric - Block Error Rate      : \d+\.\d+', re.DOTALL)
    return pattern

def getTputList_cuPHY_PUSCH_rx_pipeline(suitename, log):
    match = selectTputPattern(suitename).findall(log)

    tputlist = []
    if match:
        for i in match:
            tput = i.split(' ')[-2]
            tputlist.append(float(tput))
    return tputlist

def getElapsedTimeList_cuPHY_PUSCH_rx_pipeline(suitename, log):
    match = selectElapsedTimePattern(suitename).findall(log)

    lapsedTimelist = []
    if match:
        for i in match:
            lapsedTime = i.split(' ')[-2]
            lapsedTimelist.append(float(lapsedTime))
    return lapsedTimelist

def getErrorBitList_cuPHY_PUSCH_rx_pipeline(suitename, log):
    match = selectErrratePattern(suitename).findall(log)

    errBitList = []
    if match:
        for i in match:
            errorBit = i.split(' ')[-1]
            errBitList.append(float(errorBit))
    return errBitList

def check_AnalyzeResult_bySuite(stdev_tput, stdev_elapsedTime, errorBitcount):
    result, reason = 'PASS', ''
    if stdev_tput >= 5:
        result, reason = 'FAILED', 'stdev tput >= 5'
    elif stdev_elapsedTime >= 5:
        result, reason = 'FAILED', 'stdev elapsed time >= 5'
    elif len(errorBitcount) > 0:
        result, reason = 'FAILED', 'error bit count > 0'
    else:
        result, reason = 'PASS', ''

    return result, reason
##### for suite uPHY_PUSCH_rx_pipeline


##### cuPHY_PDSCH_pipeline_integration
"""
Running DL pipeline once w/ reference checks enabled

CRC Error Count: 0; GPU output compared w/ reference dataset <tb_cbs> from </home/dgx/Jerry/test/pkg/cuda-ran-sdk.0.5/testVectors/TV_cuphy_pdsch-default_snrdb40.00_iter1_MIMO8x8_PRB272_DataSyms12_qam256.h5>

LDPC Error Count: 0; GPU output compared w/ reference dataset <tb_codedcbs> from </home/dgx/Jerry/test/pkg/cuda-ran-sdk.0.5/testVectors/TV_cuphy_pdsch-default_snrdb40.00_iter1_MIMO8x8_PRB272_DataSyms12_qam256.h5>

Rate Matching Error Count: 0; GPU output compared w/ reference dataset <tb_scramcbs> from </home/dgx/Jerry/test/pkg/cuda-ran-sdk.0.5/testVectors/TV_cuphy_pdsch-default_snrdb40.00_iter1_MIMO8x8_PRB272_DataSyms12_qam256.h5>

Modulation Mapper: Found 0 mismatched QAM symbols out of 39168
GPU output compared w/ reference dataset <tb_qams> from </home/dgx/Jerry/test/pkg/cuda-ran-sdk.0.5/testVectors/TV_cuphy_pdsch-default_snrdb40.00_iter1_MIMO8x8_PRB272_DataSyms12_qam256.h5>

Timing the DL pipeline
- NB: Allocations not included. Ref. checks will fail!

DL pipeline: 96.59 us (avg. over 100 iterations)
"""
def getCRCErrorCount_PDSCH_pipeline(log):
    crcErrorCount = []
    pattern = re.compile(r'CRC Error Count: \d+', re.DOTALL)

    match = pattern.findall(log)
    if match:
        for i in match:
            crcError = i.split(' ')[-1]
            crcErrorCount.append(float(crcError))
    return crcErrorCount

def getLDPCErrorCount_PDSCH_pipeline(log):
    ldpcErrorCount = []
    pattern = re.compile(r'LDPC Error Count: \d+', re.DOTALL)

    match = pattern.findall(log)
    if match:
        for i in match:
            ldpcError = i.split(' ')[-1]
            ldpcErrorCount.append(float(ldpcError))
    return ldpcErrorCount

def getRateMatchErrorCount_PDSCH_pipeline(log):
    rateMatchErrorCount = []
    pattern = re.compile(r'Rate Matching Error Count: \d+', re.DOTALL)

    match = pattern.findall(log)
    if match:
        for i in match:
            rateMatch = i.split(' ')[-1]
            rateMatchErrorCount.append(float(rateMatch))
    return rateMatchErrorCount

def getMismatchCount_PDSCH_pipeline(log):
    misMatchCount = []
    pattern = re.compile(r'Modulation Mapper: Found \d+', re.DOTALL)

    match = pattern.findall(log)
    if match:
        for i in match:
            misMatch = i.split(' ')[-1]
            misMatchCount.append(float(misMatch))
    return misMatchCount

def getelapseTime_PDSCH_pipeline(log):
    elapsedTimeCount = []
    pattern = re.compile(r'DL pipeline: \d+\.\d+ us', re.DOTALL)

    match = pattern.findall(log)
    if match:
        for i in match:
            elapsedTime = i.split(' ')[-2]
            elapsedTimeCount.append(float(elapsedTime))
    return elapsedTimeCount

def check_PDSCH_pipe_AnalyzeResult(errCrc, errLDPC, errRateMatch, errMisMatch, stdev_elapsedTime):
    result, reason = 'PASS', ''
    #if len(errCrc)==0 and len(errLDPC)==0 and len(errRateMatch)==0 and len(errMisMatch)==0 and stdev_elapsedTime<5:
    if len(errCrc) > 0:
        result, reason = 'FAILED', 'crc error count > 0'
    elif len(errLDPC) > 0:
        result, reason = 'FAILED', 'LDPC error count > 0'
    elif len(errRateMatch) > 0:
        result, reason = 'FAILED', 'rate match error count > 0'
    elif len(errMisMatch) > 0:
        result, reason = 'FAILED', 'mismatch > 0'
    elif stdev_elapsedTime >= 5:
        result, reason = 'FAILED', 'the elapsed time stdev >= 5'
    else:
        result, reason = 'PASS', ''
    return result, reason
##### cuPHY_PDSCH_pipeline_integration


