__author__ = 'jacob@vsee.com'

import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from page.backend.room.room_setting import RoomSettingPage

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.assertions import Assert


class RoomSettingSteps(Assert):
    on_room_setting = RoomSettingPage()

    def add_visit_option(self, visit, duration):
        self\
            .on_room_setting\
            .click_on_room_settings_tab() \
            .click_on_add_new_visit_option() \
            .enter_visit_description(visit) \
            .enter_duration(duration)\
            .click_on_update()
        self.should_see_message_success()
        self.on_room_setting.close_form()
        return self

    def description(self, des):
        self\
            .on_room_setting \
            .click_on_room_settings_tab() \
            .enter_room_description(des)\
            .click_on_update()
        self.on_room_setting.close_form()
        return self

    def should_see_message_success(self):
        self.verifyEquals(self.on_room_setting.get_alert_message(), 'Success! Update room details successfully')
        return self
