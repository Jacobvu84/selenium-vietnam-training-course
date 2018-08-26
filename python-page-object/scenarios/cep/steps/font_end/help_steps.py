__author__ = 'jacob@vsee.com'

import sys, os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from page.font_end.help_page import HelpPage
from util.assertions import Assert


class HelpSteps(Assert):
    on_help_screen = HelpPage()

    def should_see_title(self, title):
        self.verifyEquals(self.on_help_screen.get_title_help_page(), title)
        return self

    def should_see_body_description(self, body):
        _body = body.split("|")
        for des in _body:
            self.verifyContainsString(des, self.on_help_screen.get_body_description())
        return self

    def should_see_information_need_provide(self, infors):
        _infors = infors.split("|")
        for infor in _infors:
            self.verifyContainsString(infor, self.on_help_screen.get_contact_options())
        return self

    def close_help_window(self):
        self.on_help_screen.click_on_close()
