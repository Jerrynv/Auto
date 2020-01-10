# -*- coding: utf-8 -*-
import os
from pandas import DataFrame
from common.logsave import logger
"""
data = {'name' : ['A', 'B', 'C'],
        'age':[11,12,13],
        'sex':['man', 'femal', 'man']
}
"""

class CaseAnalyze():
    _suiteName = ''
    _caseName = ''
    _command = ''
    _criteria = ''
    _result = ''
    _rltDetails = ''
    _logfile = ''

    def __init__(self, suiteName, caseName, command, result, rltDetails, logfile, criteria=['tput stdev<5%', 'elapsetime stdev<5%', 'bit error count<=0']):
        self._suiteName = suiteName
        self._caseName = caseName
        self._command = command
        self._criteria = criteria
        self._result = result
        self._rltDetails = rltDetails
        self._logfile = logfile

    def updateSuitename(self, suiteName):
        _suiteName = suiteName

    def updateCasename(self, caseName):
        _caseName = caseName

    def updateCaseCommand(self, command):
        _command = command

    def updateCaseCommand(self, criteria):
        _criteria = criteria

    def updateTestResult(self, result):
        _result = result

    def updateLogfile(self, logfile):
        _logfile = logfile

    def print_report(self):
        pass


class TestReport():
    caseRltList = []

    def __inif__(self):
        self.caseRltList = []

    def cleanData(self):
        self.caseRltList = []

    def addCaseresult(self, caseAnalyze):
        self.caseRltList.append(caseAnalyze)

    def generateReport(self):
        #for i, report in enumerate(caseRltList):
        #    print(report)
        #print("report len={}".format(len(self.caseRltList)))
        reportfile = 'report.xlsx'

        suiteNameList = []
        caseNameList = []
        commandList = []
        criteriaList = []
        resultList = []
        rltDetailsList = []
        logfileList = []
        for i, report in enumerate(self.caseRltList):
            suiteNameList.append(report._suiteName)
            caseNameList.append(report._caseName)
            commandList.append(report._command)
            criteriaList.append(report._criteria)
            resultList.append(report._result)
            rltDetailsList.append(report._rltDetails)
            logfileList.append(report._logfile)

        reportTable = {'suiteName' : suiteNameList,
                       'case' : caseNameList,
                       'command' : commandList,
                       'result' : resultList,
                       'detail' : rltDetailsList,
                       'log file' : logfileList}

        if os.path.exists(reportfile):
            os.remove(reportfile)
        df = DataFrame(reportTable)
        df.to_excel(reportfile)
        logger.info('generate testing report : {}'.format(os.path.join(os.getcwd(), reportfile)))

        self.cleanData()

if __name__ == '__main__':
    df = DataFrame(data)
    df.to_excel('new.xlsx')