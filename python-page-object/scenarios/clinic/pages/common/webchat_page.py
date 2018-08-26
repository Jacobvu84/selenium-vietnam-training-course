'''
Created on Jun 14, 2018

@author: Thang Nguyen
'''

import os, sys
from time import sleep
import unicodedata
from waiting import wait

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
from selenium.webdriver.common.by import By
from webium.clinic_page import ClinicPage
from selenium.webdriver.common.keys import Keys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from webium.base_page import Test


class WebchatPage(ClinicPage):
    def __init__(self, ClinicPage):
        self.set_attribute(ClinicPage)
    
    @Test()
    def type_into_webchat(self, chat_content, username = ""):
        if username == "":
            xpath = "//input[@type='textarea']"
        else:
            xpath = ".//h4[text()='{0}']/../../div//input[@type='textarea']".format(username)
        self.element(By.XPATH, xpath)
        for text in chat_content:
            self.clear().type(text + Keys.ENTER)
            # sleep 3 seconds to prevent problem from other side
            sleep(3)
    
    def verify_webchat(self, text, username = ""):
        # return normal string   
        def ascii_string(s):
            if isinstance(s, str):
                return s
            elif isinstance(s, unicode):
                print "unicode string"
                return unicodedata.normalize('NFKD', s).encode('ascii','ignore')
            else:
                print "not a string"
                return None
            
        if username == "":
            xpath = "//input[@type='textarea']"
        else:
            xpath = ".//h4[text()='{0}']/../../div//input[@type='textarea']".format(username)
        try:
            self.element(By.XPATH, xpath)
            webchat_content = ascii_string(self.get_text_value())
            if text not in webchat_content:
                return False
            return True
        except: # Case chat hasn't opened yet
            return False
    
    @Test()
    def wait_for_webchat_content(self, chat_content, username = "", timeout=60):
        index = 0
        for text in chat_content:
            if index != 0:
                timeout = 5
            wait(lambda: self.verify_webchat(text, username=username), waiting_for='Wait For Text is in webchat',
                 timeout_seconds=timeout)
            index += 1
    
    @Test()
    def verify_visible_of_webchat(self, user_name):
        xpath = ".//div[@id='webchat-container']/div/div/h4[text()='" + user_name + "']"
        self.element(By.XPATH, xpath) \
        .wait_until_visible()
        