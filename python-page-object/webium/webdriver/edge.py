__author__ = 'jacob@vsee.com'

import os
import sys
import shutil

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from webdriver import AbsWebdriver
from selenium import webdriver
from properties import Properties
from scenarios.resource import user_dir

class EdgeProfile(AbsWebdriver):

    def __init__(self):
        self.cfg = Properties("vsee.properties")

        executable_path = str(self.cfg.edge_driver())
        if executable_path.startswith("."):
            path = executable_path.split(".")
            self.driverpath = user_dir + path[1] + ".exe"
        else:
            self.driverpath = executable_path

    def init_driver(self):
        self._edgeClearTemp()

        driver = webdriver.Edge(executable_path=self.driverpath)
        return driver


    # Remove data on edge browser
    def _edgeClearTemp(self):

        appdata_location = os.environ.get('LOCALAPPDATA')
        _edgeTempDir = r"{0}\Packages\Microsoft.MicrosoftEdge_8wekyb3d8bbwe\AC".format(
            appdata_location)
        _edgeAppData = r"{0}\Packages\Microsoft.MicrosoftEdge_8wekyb3d8bbwe\AppData".format(
            appdata_location)

        try:
            os.system("taskkill  /F /IM MicrosoftEdge.exe")
        except:
            pass
        try:
            os.system("taskkill  /F /IM dllhost.exe")
        except:
            pass
        if os.path.exists(_edgeTempDir):
            for directory in os.listdir(_edgeTempDir):
                if directory.startswith('#!'):
                    shutil.rmtree(
                        os.path.join(_edgeTempDir, directory), ignore_errors=True)

        if os.path.exists(_edgeAppData):
            shutil.rmtree(_edgeAppData, ignore_errors=True)