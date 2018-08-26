__author__ = 'jacob@vsee.com'

import sys, os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from page.web_chat import WebChatPage
from util.assertions import Assert


class WebChatSteps(Assert):
    on_web_chat = WebChatPage()

    def open_web_chat_from_dashboard(self, vsee_id, provider_name):
        self.on_web_chat.click_one_message_icon(vsee_id, provider_name)
        return self

    def should_see_the_webchat_of(self, client):
        self.verifyEquals(self.on_web_chat.is_invisible_web_chat(client), False)
        return self

    def send_a_message(self, message):
        self.on_web_chat.sending_text(message)
        return self

    def reply_message(self, reply):
        self.on_web_chat.sending_text(reply)
        return self

    def close_web_chat(self):
        self.on_web_chat.click_on_close_web_chat()
        return self

    def should_not_see_web_chat_of(self, sender):
        self.verifyEquals(self.on_web_chat.is_invisible_web_chat(sender), True)
        return self

    def wait_for_message_from_sender(self, message):
        self.on_web_chat.wait_for_message(message)
        return self
