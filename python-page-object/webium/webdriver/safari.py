__author__ = 'jacob@vsee.com'

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from webdriver import AbsWebdriver
from selenium import webdriver
from properties import Properties
from scenarios.resource import user_dir

class SafariProfile(AbsWebdriver):

    def __init__(self):
        self.cfg = Properties("vsee.properties")
        executable_path = str(self.cfg.safari_driver())
        if executable_path.startswith("."):
            path = executable_path.split(".")
            self.driverpath = user_dir + path[1] + ".exe"
        else:
            self.driverpath = executable_path

    def init_driver(self):
        driver = webdriver.Safari(executable_path=self.driverpath)
        return driver