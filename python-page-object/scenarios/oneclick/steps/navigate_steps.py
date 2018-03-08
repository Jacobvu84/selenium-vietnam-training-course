__author__ = 'jacob@vsee.com'

#from vseeweb.oneclick.page.navigation_page import MENU

import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from page.navigation_page import NavigatePage

class NavigateSteps():

    #global on_navigate_page
    on_navigate_page = NavigatePage()

    def goto_provider_screen(self):
        self.on_navigate_page.provider_link.click()