__author__ = 'jacob@vsee.com'

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from webdriver import AbsWebdriver
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from properties import Properties
from scenarios.resource import user_dir

class FirefoxProfile(AbsWebdriver):

    def __init__(self):
        self.cfg = Properties("vsee.properties")
        self.firebug = self.cfg.firebug_mode()

        self.x = self.cfg.browser_x()
        self.y = self.cfg.browser_y()
        self.width = self.cfg.browser_width()
        self.height = self.cfg.browser_height()
        self.maximized = self.cfg.browser_maximized()

        self.ffProfile = self.firefoxProfile()
        self.ffCab = DesiredCapabilities.FIREFOX
        self.ffCab["marionette"] = True

        executable_path = str(self.cfg.firefox_driver())
        if executable_path.startswith("."):
            path = executable_path.split(".")
            self.driverpath = user_dir + path[1] + ".exe"
        else:
            self.driverpath = executable_path

    def init_driver(self):
        driver =  webdriver.Firefox(executable_path=self.driverpath, firefox_profile=self.ffProfile, capabilities=self.ffCab)
        if self.x and self.y:
            driver.set_window_position(self.x, self.y)
        if self.width and self.height:
            driver.set_window_size(self.width, self.height)
        if self.maximized:
            driver.maximize_window()
        return driver

    def firefoxProfile(self):
        ffProfile = os.path.dirname(os.path.realpath(__file__)) + "/forFFProfile"
        profile = webdriver.FirefoxProfile(ffProfile)
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk",
                               "application/octet-stream, application/x-msdownload")
        profile.set_preference("browser.download.manager.alertOnEXEOpen", False)
        profile.set_preference("plugins.notifyMissingFlash", False)
        profile.set_preference("app.update.enabled", False)
        profile.set_preference("browser.helperApps.deleteTempFileOnExit", True)
        profile.set_preference("browser.startup.page", 0)
        profile.set_preference("browser.startup.homepage", "about:blank")
        profile.set_preference("browser.startup.homepage_override.mstone", "ignore")
        profile.set_preference("browser.usedOnWindows10", True)
        profile.set_preference("browser.accept_untrusted_certs", True)
        profile.set_preference("browser.assume_untrusted_issuer", True)
        profile.set_preference("dom.max_chrome_script_run_time", 0)
        profile.set_preference("dom.max_script_run_time", 0)

        if self.firebug:
            # https://getfirebug.com
            firebugPath = os.path.dirname(os.path.realpath(__file__)) + "/forFFProfile/extensions/firebug.xpi"
            # http://www.softwareishard.com/blog/consoleexport/
            exportConsolePath = os.path.dirname(
                os.path.realpath(__file__)) + "/forFFProfile/extensions/consoleexport.xpi"
            profile.add_extension(firebugPath)
            profile.add_extension(exportConsolePath)
            profile.set_preference("extensions.firebug.currentVersion", "2.0.6")
            profile.set_preference("extensions.firebug.defaultPanelName", "console")
            profile.set_preference("extensions.firebug.allPagesActivation", "on")
            profile.set_preference("extensions.firebug.console.enableSites", "on")
            profile.set_preference("extensions.firebug.console.defaultPersist", True)
            # profile.set_preference("extensions.firebug.consoleexport.active", True)
            profile.set_preference("devtools.toolbar.enabled", True)
            profile.set_preference("devtools.toolbar.visible", True)
            profile.set_preference("devtools.webconsole.filter.network", True)
            profile.set_preference("devtools.webconsole.filter.networkinfo", True)
            profile.set_preference("devtools.webconsole.persistlog", True)
            profile.set_preference("devtools.webconsole.timestampMessages", True)
            profile.set_preference("devtools.webconsole.filter.jslog", True)
            profile.set_preference("devtools.toolbar.visible", True)
            profile.set_preference("devtools.toolbox.selectedTool", "webconsole")
            # profile.set_preference("extensions.firebug.consoleexport.serverURL", "http://web.internal.vsee.com/~qa/consoleLog.php")
        return profile