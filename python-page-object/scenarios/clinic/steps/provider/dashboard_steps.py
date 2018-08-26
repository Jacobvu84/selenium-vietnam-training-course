'''
Created on Jun 5, 2018

@author: Thang Nguyen
Steps for admin using
'''

import sys, os
from time import sleep
import calendar

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
from webium.clinic_page import ClinicPage
from clinic.pages.provider.dashboard_page import DashboardPage
from clinic.pages.admin.users_page import UsersPage


class DashboardSteps(ClinicPage):
    
    def __init__(self, ClinicPage):
        self.set_attribute(ClinicPage)
        
        self.dashboard_page = DashboardPage(ClinicPage)
        self.users_page = UsersPage(ClinicPage)
        
    def open_dashboard(self):
        self.dashboard_page.click_into_dashboard()
        self.dashboard_page.check_visible_of_invite_button()
    
    def open_admin_panel(self):
        self.dashboard_page.click_into_user_name()
        self.dashboard_page.click_into_admin_panel()
        self.users_page.check_visibile_of_users_link()
