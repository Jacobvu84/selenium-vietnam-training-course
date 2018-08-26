__author__ = 'jacob@vsee.com'

import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from page.font_end.provider.my_clinic import MyClinicPage

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
from util.assertions import Assert


class MyClinicSteps(Assert):
    on_my_clinic_page = MyClinicPage()

    def choose_waiting_room(self, room):
        self.on_my_clinic_page.select_waiting_room(room)
        return self

    def description(self, value):
        self.on_my_clinic_page.enter_room_description(value)
        return self

    def add_new_visit_option(self, option, duration):
        self.on_my_clinic_page\
            .click_on_add_new_visit_option() \
            .enter_visit_option(option)\
            .enter_duration(duration)\
            .click_on_update()
        return self

    def should_see_message(self, value):
        self.verifyEquals(value, self.on_my_clinic_page.get_alert_message())
