'''
Created on Jun 14, 2018

@author: Thang Nguyen
Install VSee, launching vsee e.t.c...
'''

import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
from selenium.webdriver.common.by import By
from webium.clinic_page import ClinicPage

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from webium.base_page import Test


class LaunchingPage(ClinicPage):
    def __init__(self, ClinicPage):
        self.set_attribute(ClinicPage)
    
    # Manual detection
    install_vsee_link = (By.PARTIAL_LINK_TEXT, "click here to install VSee")
    install_vsee_btn = (By.XPATH, "//button[contains(text(), 'Install VSee')]")
    proceed_to_consultation_btn = (By.XPATH, "//button[contains(text(), 'Proceed to Consultation')]")
    
    @Test(install_vsee_link)
    def click_into_click_here_to_install_vsee(self):
        self.element(*self.install_vsee_link) \
        .wait_until_clickable() \
        .click()
    
    @Test(install_vsee_btn)
    def click_into_install_vsee(self):
        self.element(*self.install_vsee_btn) \
        .wait_until_clickable() \
        .click()
    
    @Test(proceed_to_consultation_btn)
    def click_into_proceed_to_consultation(self):
        self.element(*self.proceed_to_consultation_btn) \
        .wait_until_clickable() \
        .click()
    
    # VseeInstallation
    installation_quit_btn = (By.ID, "VseeInstallationCloseButton")
    installation_next_btn = (By.ID, "dlNextButton")
    
    @Test(installation_quit_btn)
    def click_into_installation_quit_(self):
        self.element(*self.installation_quit_btn) \
        .wait_until_clickable() \
        .click()
    
    @Test(installation_next_btn)
    def click_into_installation_next(self):
        self.element(*self.installation_next_btn) \
        .wait_until_clickable() \
        .click()
    
    # VseeAvsetup
    setup_start_test_btn = (By.ID, "VseeAVTestButton")
    
    @Test(setup_start_test_btn)
    def click_into_start_test(self):
        self.element(*self.setup_start_test_btn) \
        .wait_until_clickable() \
        .click()
    
    # launching modal
    launching_modal = (By.ID, "LaunchModalTitle")
    
    @Test(launching_modal)
    def wait_invisible_of_launching_modal(self):
        self.element(*self.launching_modal) \
        .wait_until_invisible(120)