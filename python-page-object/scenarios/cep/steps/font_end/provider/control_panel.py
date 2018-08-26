__author__ = 'jacob@vsee.com'

import os, sys, platform

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from page.font_end.provider.control_panel import ControlPanelPage

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
from util.assertions import Assert
from util.support import capture_screenshot
from util.logger import Test

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../../")
from testClass import runSikuli


class ControlPanelSteps(Assert):
    on_control_panel = ControlPanelPage()

    @Test(("Group Steps", ""))
    def make_video_call(self):
        self.on_control_panel.wait_a_bit(10)
        self.on_control_panel.click_on_video_call()
        return self

    #######################

    @Test(("Group Steps", ""))
    def visit(self, image_name):
        self.on_control_panel.wait_a_bit(3)
        capture_screenshot(image_name)
        # capture
        return self

    def should_see_vsee_status_in_a_call(self):
        self.verifyEquals(self.on_control_panel.is_in_a_call(), True)
        return self

    def should_see_vsee_status_is_online(self):
        self.verifyEquals(self.on_control_panel.is_online(), True)
        return self

    @Test(("Group Steps", ""))
    def end_call(self, testID, src, dst, endFlag):
        if "Windows-7" in platform.platform():
            runSikuli.runWin("endcall.sikuli", [testID, src, dst, str(endFlag), "False", "False"])
        return self

    @Test(("Group Steps", ""))
    def close_cam(self, testID, src):
        if "Windows-7" in platform.platform():
            runSikuli.runWin("closeCamLocal.sikuli", [testID, src])
        return self

    def open_webchat(self):
        self.on_control_panel.wait_a_bit(10)
        self.on_control_panel.click_on_chat()
        return self
