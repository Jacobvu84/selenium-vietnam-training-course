'''
Created on Jun 4, 2018

@author: Thang Nguyen
Including locators for Users page on admin
Including actions 
'''

import os, sys
from waiting import wait
from time import sleep

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
from selenium.webdriver.common.by import By
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../../")
from selenium.webdriver.common.keys import Keys
from webium.clinic_page import ClinicPage

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from webium.base_page import Test


class DashboardPage(ClinicPage):
    def __init__(self, ClinicPage):
        self.set_attribute(ClinicPage)
    
    # Header
    dashboard_link = (By.PARTIAL_LINK_TEXT, "Dashboard")
    
    my_profile_link = (By.PARTIAL_LINK_TEXT, "My Profile")
    my_clinic_link = (By.PARTIAL_LINK_TEXT, "My Clinic")
    admin_panel_link = (By.PARTIAL_LINK_TEXT, "Admin panel")
    user_name_dropdown = (By.ID, "top_menu_content_user")
    
    @Test(dashboard_link)
    def click_into_dashboard(self):
        self.element(*self.dashboard_link) \
        .wait_until_clickable() \
        .click()

    @Test(user_name_dropdown)
    def click_into_user_name(self):
        self.element(*self.user_name_dropdown) \
        .wait_until_clickable() \
        .click()
    
    @Test(my_profile_link)
    def click_into_my_profile(self):
        self.element(*self.my_profile_link) \
        .wait_until_clickable() \
        .click()
    
    @Test(my_clinic_link)
    def click_into_my_clinic(self):
        self.element(*self.my_clinic_link) \
        .wait_until_clickable() \
        .click()
    
    @Test(admin_panel_link)
    def click_into_admin_panel(self):
        self.element(*self.admin_panel_link) \
        .wait_until_clickable() \
        .click()
        
        
        