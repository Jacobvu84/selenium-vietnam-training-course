__author__ = 'jacob@vsee.com'

import sys, os, platform
from shutil import copyfile

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
from scenarios.util.support import wait_for_vsee_downloaded
from scenarios.util.support import execute_file
from scenarios.util.support import empty_dir_download

from testClass import runSikuli

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from page.install_page import Installer
from util.assertions import Assert
from util.logger import Test


class InstallSteps(Assert):
    _with_installer = Installer()

    def get_browser_type(self):
        return self._with_installer.browser_type()

    def install_vsee(self):
        empty_dir_download()
        self._with_installer.click_on_link_download_vsee_messenger()
        wait_for_vsee_downloaded()

        print "The script is running on " + platform.platform()
        if "Windows-7" in platform.platform():
            execute_file()
            runSikuli.runWin("installationWin7.sikuli")
            self._with_installer.click_on_next()
            self._with_installer.click_on_start_test()
            self.accept_privacy_and_term_GDPR()
            if 'firefox' == self.get_browser_type():
                runSikuli.runWin("setupVM.sikuli")
            elif 'ie' == self.get_browser_type():
                runSikuli.runWin("setupVMonIE.sikuli")
        return self

    @Test()
    def accept_privacy_and_term_GDPR(self):
        runSikuli.runWin("acceptGDPR.sikuli")
        return self

    @Test(("Group Steps", "Proceed to launch VSee - for VSee is already installed case"))
    def launch_vsee(self, is_install):
        if not is_install:
            self._with_installer.click_on_proceed_to_consultation()
        return self

    def close_the_video_conference(self, testID, src):
        runSikuli.runWin("closeCamLocal.sikuli", [testID, src])
        return self

    def relaunch_video(self):
        self._with_installer.click_here_to_relaunch_video()
        return self

    def should_see_the_video_relaunch(self, testID, src):
        runSikuli.runWin("findCam.sikuli", [testID, src])
        return self