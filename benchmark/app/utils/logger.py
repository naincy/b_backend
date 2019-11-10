import logging
from django.conf import settings
from ..utils.globalconstants import *

"""
Custom Logger Class
"""
class Logger:

    def setup_logger(logger_name, log_file, level=logging.INFO):
        log_setup = logging.getLogger(logger_name)
        formatter = logging.Formatter('%(levelname)s: %(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        fileHandler = logging.FileHandler(log_file, mode='a')
        fileHandler.setFormatter(formatter)
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)
        log_setup.setLevel(level)
        log_setup.addHandler(fileHandler)
        log_setup.addHandler(streamHandler)
    
    @staticmethod
    def log(msg, level = DEBUG):
    
        if settings.DEBUG:
                print(msg)

        if level == INFO: 
            log = logging.getLogger(INFO_LOGGER)
            log.info(msg)
            if settings.DEBUG:
                log = logging.getLogger(DEBUG_LOGGER)
                log.debug(msg)
        
        if level == DEBUG: 
            if settings.DEBUG:
                log = logging.getLogger(DEBUG_LOGGER)
                log.debug(msg) 

        if level == ERROR: 
            log = logging.getLogger(ERROR_LOGGER)
            log.exception(msg)
            if settings.DEBUG:
                log = logging.getLogger(DEBUG_LOGGER)
                log.exception(msg)
         

Logger.setup_logger(DEBUG_LOGGER, "logs/debug.log", logging.DEBUG)
Logger.setup_logger(ERROR_LOGGER, "logs/error.log", logging.ERROR)
Logger.setup_logger(INFO_LOGGER, "logs/info.log", logging.INFO)  


