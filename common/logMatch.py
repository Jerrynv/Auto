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
##### for suite uPHY_PUSCH_rx_pipeline
