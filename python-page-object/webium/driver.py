__maintained__ = 'jacob@vsee.com'

from settings import init_driver
from errors import WebiumException
import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from scenarios.util.setting import _implicit_timeout
from scenarios.util.setting import _url

_driver_instance = None


def get_driver():
    global _driver_instance
    if not _driver_instance:    # No session started
        _driver_instance = init_driver()    # Create new then set it to _driver_instance
        _driver_instance.implicitly_wait(_implicit_timeout)
    return _driver_instance


def set_driver(driver):
    global _driver_instance
    _driver_instance = driver

def close_driver():
    global _driver_instance
    if _driver_instance:
        _driver_instance.quit()
        _driver_instance = None


def open_at():
    if _url:
        get_driver().get(_url)
    else:
        get_driver().quit()
        raise WebiumException('[INFO]: Can\'t open page without url. Please check that vsee.properties')


def get_driver_no_init():
    return _driver_instance
