# -*- coding: utf-8 -*-
import logging
from logging import handlers

logger = logging.getLogger("logger")

fmt='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'
format_str = logging.Formatter(fmt)
logger.setLevel(logging.DEBUG)


sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
sh.setFormatter(format_str)

th = handlers.TimedRotatingFileHandler(filename='run.log', when='D', backupCount=3, encoding='utf-8')
th.setLevel(logging.DEBUG)
th.setFormatter(format_str)

logger.addHandler(sh)
logger.addHandler(th)

"""
class Logger():
    level_relations = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'crit':logging.CRITICAL
    }

    def __init__(self,filename, level='info', when='D',backCount=3, fmt='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)
        self.logger.setLevel(self.level_relations.get(level))

        sh = logging.StreamHandler()
        sh.setFormatter(format_str) 

        th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backCount, encoding='utf-8')
        th.setFormatter(format_str)

        self.logger.addHandler(sh)
        self.logger.addHandler(th)
"""

if __name__ == '__main__':
    #log = Logger('all.log',level='debug')
    #log.logger.debug('debug')
    #log.logger.info('info')
    #log.logger.warning('')
    #log.logger.error('')
    #log.logger.critical('')
    #Logger('error.log', level='error').logger.error('error')
    logger("Hello")
