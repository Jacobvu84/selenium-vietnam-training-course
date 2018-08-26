__author__ = 'jacob@vsee.com'

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from webdriver import AbsWebdriver
from selenium import webdriver
from properties import Properties
from scenarios.resource import user_dir

class ChromeProfile(AbsWebdriver):

    def __init__(self):
        self.cfg = Properties("vsee.properties")
        self.x = self.cfg.browser_x()
        self.y = self.cfg.browser_y()
        self.width = self.cfg.browser_width()
        self.height = self.cfg.browser_height()
        self.maximized = self.cfg.browser_maximized()
        arguments = self.cfg.chrome_arguments()
        self.options = arguments.split(",")
        executable_path = str(self.cfg.chrome_driver())
        if executable_path.startswith("."):
            path = executable_path.split(".")
            self.driverpath = user_dir + path[1] + ".exe"
        else:
            self.driverpath = executable_path

    def init_driver(self):
        option = webdriver.ChromeOptions()
        prefs = {'safebrowsing.enabled': 'false'}  # To accept file download
        option.add_experimental_option("prefs", prefs)

        for line in self.options:
            option.add_argument(line)

        try:
            self.disableVSeeProtocol()
            userDataPath = "C:\\Users\\vsee\\AppData\\Local\\Google\\Chrome\\User Data"
            option.add_argument("user-data-dir={0}".format(userDataPath))  # Use default profile on local
        except:  # will return exception if running on local.
            pass
        driver = webdriver.Chrome(executable_path=self.driverpath, chrome_options=option)
        if self.x and self.y:
            driver.set_window_position(self.x, self.y)
        if self.width and self.height:
            driver.set_window_size(self.width, self.height)
        if self.maximized:
            driver.maximize_window()
        return driver

    def disableVSeeProtocol(self):

        localStatePath = "C:\\Users\\vsee\\AppData\\Local\\Google\\Chrome\\User Data\\Local State"
        storageLocalStatePath = "\\\\storage02.internal.vsee.com\\\\users\\\\qa\\\\Local State"

        print "[INFO]: Bypass external protocol popup on Chrome"
        f = open(storageLocalStatePath, "r")
        data = f.read()
        f.close()
        print "[INFO]: Edit Local State file from {0}".format(localStatePath)
        f = open(localStatePath, "w")
        f.write(data)
        f.close()