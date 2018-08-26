__author__ = 'jacob@vsee.com'

import sys, os
from waiting import wait

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
from webium.base_page import BasePage
from selenium.webdriver.common.by import By

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.logger import Test


class Installer(BasePage):
    linkdownload = (By.XPATH, "//a[@class='install-vsee' and text()='click here to install VSee']")
    next_btn = (By.ID, "dlNextButton")
    start_test = (By.ID, "VseeAVTestButton")

    def browser_type(self):
        return self.get_webdriver_driver()

    @Test(linkdownload)
    def click_on_link_download_vsee_messenger(self):
        self.element(*self.linkdownload).wait_until_visible().click()

    @Test(next_btn)
    def click_on_next(self):
        self.element(*self.next_btn).wait_until_present().click()

    @Test(start_test)
    def click_on_start_test(self):
        self.element(*self.start_test).wait_until_present().click_and_wait(10)

    def is_in_call(self):
        """Wait the provider call"""
        msg_txt = "//*[contains(text(),'Please do not leave this page until your consultation is over.')]"
        count = len(self.find_elements(*(By.XPATH, msg_txt)))
        if count == 0:
            return True
        else:
            return False

    def is_survey_displayed(self):
        """Wait the survey display"""
        survey_form = "//div[@id='VisitSurvey']/following-sibling::a[contains(text(),'End Visit')]"
        count = len(self.find_elements(*(By.XPATH, survey_form)))
        if count == 0:
            return True
        else:
            return False

    @Test()
    def wait_for_provider(self):
        wait(lambda: self.is_in_call(), waiting_for='Wait For Provider call',
             timeout_seconds=600)
        return self

    @Test()
    def wait_for_provider_complete_visit(self):
        """When provider clicks on complete visit, The survey will display on patient side"""
        wait(lambda: self.is_survey_displayed(), waiting_for='Wait For Provider complete visit',
             timeout_seconds=600)
        return self

    consultation = (By.XPATH, "//button[contains(text(), 'Proceed to Consultation')]")

    @Test(consultation)
    def click_on_proceed_to_consultation(self):
        self.element(*self.consultation).wait_a_bit(2).wait_until_clickable().click()
        return self

    just_exit = (By.XPATH, "//a[text()='Or just exit']")

    @Test(just_exit)
    def should_see_the_exit_link(self):
        return self.element(*self.just_exit).wait_until_present().is_present()

    relaunch = (By.PARTIAL_LINK_TEXT, 'click here to relaunch video')

    @Test(relaunch)
    def click_here_to_relaunch_video(self):
        self.element(*self.relaunch).wait_until_present().click_and_wait()
        return self
