__author__ = 'jacob@vsee.com'

import os, sys
from waiting import wait

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webium.base_page import BasePage

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.logger import Test
from util.assertions import Assert


class WebChatPage(BasePage, Assert):
    chatbox = (By.XPATH, "(//form[@id='webchat-input-form']/input[@placeholder='Type your message here'])[last()]")
    close_chat = (By.XPATH, "//button[@class='close closebox']")

    @Test(chatbox)
    def sending_text(self, message):
        self.element(*self.chatbox).wait_until_visible().clear().type(message).type_and_wait(Keys.ENTER, 3)
        return self

    @Test(close_chat)
    def click_on_close_web_chat(self):
        self.element(*self.close_chat).click_and_wait(5)
        return self

    @Test(("Undefined", "Undefined"))
    def is_invisible_web_chat(self, client):
        webchat_container = (By.XPATH, "//div[@id='webchat-container']//h4[text()='{0}']".format(client))
        try:
            self.element(*webchat_container).wait_until_invisible()
            return True
        except Exception as e:
            return False

    def is_message_present(self, msg):
        """Wait the patient in waiting room"""
        patient_xpath = "//div[@class='webchatbox-working']//li[last()]" \
                        "/div[@class='webchat-message-div webchat-message-sender']" \
                        "/div[@class='webchat-message-content']/div[contains(text(),'{0}')]".format(msg)
        patient_view = (By.XPATH, patient_xpath)
        return self.element(*patient_view).is_present()

    # 15s wait for each iterator
    @Test(("Undefined", "Undefined"))
    def wait_for_message(self, msg):
        wait(lambda: self.is_message_present(msg), waiting_for='Wait For Text is in webchat',
             timeout_seconds=600)
        return self

    @Test(("Undefined", "Undefined"))
    def is_chat_icon_present(self):
        chat_icon = (By.XPATH, "//div[@id='providerList']//a[@title='Message']")
        return self.element(*chat_icon).is_present()

    def wait_for_chat_message_icon(self):
        wait(lambda: self.is_chat_icon_present(), waiting_for='Wait For Chat Icon',
             timeout_seconds=300)
        return self

    @Test()
    def click_one_message_icon(self, email, provider):
        self.wait_for_chat_message_icon()
        chat_btn = (By.XPATH, "//a[@data-vsee-id='{0}' and contains(@data-name,'{1}')]".format(email, provider))
        self.element(*chat_btn).wait_until_clickable().highlight_element().click_and_wait(2)
        return self

