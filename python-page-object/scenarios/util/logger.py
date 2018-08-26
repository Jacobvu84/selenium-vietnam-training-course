from support import mkdir
from support import TARGET

import datetime
import time
import calendar
import logging
import inspect
import sys, os
from support import capture_screenshot
from support import capture_screenshot_browser

from setting import _capture_mode
from setting import _wait_decorator
from setting import _take_screenshot_browser

def get_timestamp():
    return datetime.datetime.now().strftime("%H:%M:%S")


def setup_logger(logger_name, log_file, level=logging.INFO):
    l = logging.getLogger(logger_name)
    
    if not l.handlers:  # Never addHandler for existing one
        formatter = logging.Formatter('%(message)s')
        fileHandler = logging.FileHandler(log_file, mode='w')
        fileHandler.setFormatter(formatter)
        streamHandler = logging.StreamHandler(sys.stdout)
        streamHandler.setFormatter(formatter)

        l.setLevel(level)
        l.addHandler(fileHandler)
        l.addHandler(streamHandler)

class LogTests():
    def __init__(self, className, funcName, locator, value=None, _driver=None):
        self.className = className
        self.funcName = funcName
        self.locator = locator
        self.value = value
        self._driver = _driver
        self.report_logger = logging.getLogger('report')
        self.epoc_time = str(int(round(time.time() * 1000)))

    def __enter__(self):
        time.sleep(_wait_decorator)
        time_info = "[{0}] {1}".format(self.epoc_time, get_timestamp())
        if self.value == None:
            self.report_logger.debug('%s [DEBUG] : STARTING ACTION: %s - %s. Locator %s' % (time_info,
                                                                           self.className,
                                                                           self.funcName.replace("_", " "),
                                                                           self.locator))
        else:
            self.report_logger.debug('%s [DEBUG] : STARTING ACTION: %s - %s. Locator %s , Value [%s]' % (time_info,
                                                                                        self.className,
                                                                                        self.funcName.replace("_", " "),
                                                                                        self.locator, self.value))

        self.init_time = calendar.timegm(time.gmtime())
        image_name = str(get_timestamp()).replace("-", "").replace(" ", "").replace(":", "") \
                     + self.className + "." + self.funcName \
                     + ".png"
        if 'BEFORE_AND_AFTER_EACH_STEP' == _capture_mode:
            if _take_screenshot_browser and self._driver:
                capture_screenshot_browser(image_name, self._driver)
            else:
                capture_screenshot(image_name)
        return self
    
    def __exit__(self, type, value, tb):
        time_info = "[{0}] {1}".format(self.epoc_time, get_timestamp())
        if tb == None:
            image_name = str(get_timestamp()).replace("-", "").replace(" ", "").replace(":", "") \
                     + self.className + "." + self.funcName \
                     + ".png"
            
            if 'BEFORE_AND_AFTER_EACH_STEP' == _capture_mode or 'AFTER_EACH_STEP' == _capture_mode:
                if _take_screenshot_browser and self._driver:
                    if not capture_screenshot_browser(image_name, self._driver):
                        if not capture_screenshot(image_name):  # If there's exception, capture desktop instead
                            image_name = "None"
                else:
                    if not capture_screenshot(image_name):
                        image_name = "None"
            elif 'DISABLED' == _capture_mode:
                image_name = "None"
            else:
                image_name = "None"
                
            self.report_logger.debug(
                '%s [DEBUG] : ACTION DONE: %s (%s seconds) screen_shot: %s' % (time_info,
                                                             self.funcName,
                                                             calendar.timegm(time.gmtime()) - self.init_time,
                                                             image_name))
        else:
            image_name = str(get_timestamp()).replace("-", "").replace(" ", "").replace(":", "") \
                     + self.funcName \
                     + "_FALSE.png"
            
            # Take screenshot anyway
            if _take_screenshot_browser and self._driver:
                if not capture_screenshot_browser(image_name, self._driver):
                        if not capture_screenshot(image_name):  # If there's exception, capture desktop instead
                            image_name = "None"
            else:
                if not capture_screenshot(image_name):
                    image_name = "None"
            
            self.report_logger.debug(
                '%s [DEBUG] : ACTION FAILED: %s (%s seconds) screen_shot: %s' % (time_info,
                                                             self.funcName,
                                                             calendar.timegm(time.gmtime()) - self.init_time,
                                                             image_name))
            
            self.report_logger.debug(str(type))
            self.report_logger.debug(str(value))
            
                
        

def Test(locator=None):
    def loc(func):
        def func_wrapper(*args, **kwargs):
            class_name = args[0].__class__.__name__
            value = None
            if len(args) > 1:
                value = args[1]
            className = str(inspect.getfile(args[0].__class__)).split("features")[1] \
                            .replace("pyc", "").replace("py", "") \
                            .replace("/", ".").replace("\\", ".").replace("..", "") + class_name
            with LogTests(className, func.__name__, locator, value):
                return func(*args, **kwargs)
        return func_wrapper
    return loc

class LogSteps():
    def __init__(self, className, funcName, info, failure_msg):
        self.className = className
        self.funcName = funcName
        self.info = info
        self.failure_msg = failure_msg
        self.logger = logging.getLogger('report')
        self.epoc_time = str(int(round(time.time() * 1000)))

    def __enter__(self):
        time.sleep(1)   # Sleep here to not same time info w/ action
        time_info = "[{0}] {1}".format(self.epoc_time, get_timestamp())
        if self.info != None and self.info != "":
            self.logger.debug('{0} [INFO]  : STARTING STEP: {1}'.format(time_info,
                                                        self.info))
        else:
            self.logger.debug('{0} [INFO]  : STARTING STEP: {1}'.format(time_info,
                                                        self.funcName))
            
        self.init_time = calendar.timegm(time.gmtime())
        if 'BEFORE_AND_AFTER_EACH_STEP' == _capture_mode:
            image_name = str(get_timestamp()).replace("-", "").replace(" ", "").replace(":", "") \
                         + self.className + "." + self.funcName \
                         + ".png"
            capture_screenshot(image_name)
        return self
    
    def __exit__(self, type, value, tb):
        time_info = "[{0}] {1}".format(self.epoc_time, get_timestamp())
        if tb == None:
            self.logger.debug(
                '%s [DEBUG] : STEP DONE: %s (%s seconds)' % (time_info,
                                                             self.funcName,
                                                             calendar.timegm(time.gmtime()) - self.init_time))
        else:
            image_name = str(get_timestamp()).replace("-", "").replace(" ", "").replace(":", "") \
                     + self.funcName + "_FALSE.png"
            if not capture_screenshot(image_name):
                image_name = "None"
            if self.failure_msg == None:
                self.logger.debug(
                    '%s [DEBUG] : STEP FAILED: %s (%s seconds) screen_shot: %s' % (time_info,
                                                                 self.funcName,
                                                                 calendar.timegm(time.gmtime()) - self.init_time,
                                                                 image_name))
            else:
                
                self.logger.debug(
                    '%s [DEBUG] : STEP FAILED: %s (%s seconds) screen_shot: %s' % (time_info,
                                                                 self.failure_msg,
                                                                 calendar.timegm(time.gmtime()) - self.init_time,
                                                                 image_name))
                

def Step(info = None, failure_msg=None):
    def loc(func):
        def func_wrapper(*args, **kwargs):
            class_name = args[0].__class__.__name__
            className = str(inspect.getfile(args[0].__class__)).split("features")[1] \
                            .replace("pyc", "").replace("py", "") \
                            .replace("/", ".").replace("\\", ".").replace("..", "") + class_name
            with LogSteps(className, func.__name__, info, failure_msg):
                return func(*args, **kwargs)
        return func_wrapper
    return loc