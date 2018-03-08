__author__ = 'jacob@vsee.com'

import os,sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
from selenium.webdriver.common.by import By
from webium import BasePage
from webium import Find, Finds

class NavigatePage(BasePage):

    provider_link = Find(by=By.LINK_TEXT, value='Providers')