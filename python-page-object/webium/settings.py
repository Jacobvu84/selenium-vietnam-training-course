__maintained__ = 'jacob@vsee.com'

import os
import sys

from webdriver.browsers import Browser
from webdriver.chrome import ChromeProfile
from webdriver.ie import IEProfile
from webdriver.edge import EdgeProfile
from webdriver.safari import SafariProfile
from webdriver.firefox import FirefoxProfile

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from scenarios.util.setting import _webdriver_driver

def init_driver():
    if _webdriver_driver == Browser.ie:
        ie = IEProfile()
        return ie.init_driver()
    elif _webdriver_driver == Browser.safari:
        safari = SafariProfile()
        return safari.init_driver()
    elif _webdriver_driver == Browser.chrome:
        chrome = ChromeProfile()
        return chrome.init_driver()
    elif _webdriver_driver == Browser.edge:
        edge = EdgeProfile()
        return edge.init_driver()
    else:
        firefox = FirefoxProfile()
        return firefox.init_driver()

# driver_class = init_driver()

try:
    from local_webium_settings import *  # noqa
except ImportError:
    pass
