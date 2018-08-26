__author__ = 'jacob@vsee.com'

import sys, os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from page.guest_page import GuestPage
from util.assertions import Assert

class GuestSteps(Assert):
    on_guest_page = GuestPage()

    def provides_intake_information(self, first_name, last_name, reason):
        self\
            .on_guest_page\
            .enter_first_name(first_name)\
            .enter_last_name(last_name)\
            .enter_reason_for_visit(reason)\
            .click_on_confirm()\
            .click_on_continue()
        return self
