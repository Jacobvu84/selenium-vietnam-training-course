__author__ = 'jacob@vsee.com'

import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from page.font_end.provider.my_schedule import MySchedulePage

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
from util.assertions import Assert
from resource import ODTC


class MyScheduleSteps(Assert):
    on_my_schedule_page = MySchedulePage()

    def create_slot(self, start_date, start_time, end_time):
        self.on_my_schedule_page\
            .select_day(start_date) \
            .click_on_create_slots() \
            .set_start_time(start_time) \
            .set_end_time(end_time)
        return self

    def edit_slot(self, old_time, start_time, end_time):
        self.on_my_schedule_page\
            .select_time_to_edit(old_time) \
            .set_start_time(start_time) \
            .set_end_time(end_time)
        return self

    def delete_slot(self, slot):
        self.on_my_schedule_page \
            .select_time_to_delete(slot)\
            .click_on_delete()
        return self

    def create_slot_with_change_start_date(self, new_start_date, start_time, end_time):
        self.on_my_schedule_page\
            .select_day_on_next_week() \
            .click_on_create_slots() \
            .set_date(new_start_date) \
            .set_start_time(start_time) \
            .set_end_time(end_time)
        return self

    def repeat(self, day_of_week):
        self.on_my_schedule_page.click_on_repeat()
        values = day_of_week.split(",")
        for value in values:
            self.on_my_schedule_page.repeat_on_day(value)
        return self

    def until(self, end_date):
        self.on_my_schedule_page.enter_end_date(end_date).click_on_confirm()
        return self

    def confirm(self):
        self.on_my_schedule_page.click_on_confirm()
        return self

    def update(self):
        self.on_my_schedule_page.click_on_update()
        return self

    def should_see_message_is_shown(self, msg):
        self.verifyEquals(self.on_my_schedule_page.get_alert_message(), msg)
        return self

    def should_see_slot_is_created(self, range_time_slot):
        """Make sure there is no slot with different range time"""
        self.verifyContainsString(range_time_slot, self.on_my_schedule_page.get_range_time_of_slot())
        return self

    def should_see_provider_name(self):
        odtc = ODTC()
        """
        providers[x].split(",")[y]
            x: order of doctor in the list
            y: 0 - email
               1 - first name
               2 - last name (fixed)
        """
        providers = odtc.get_cep_provider()
        f_name = providers[0].split(",")[1]
        l_name = providers[0].split(",")[2]
        full_name = f_name + " " + l_name
        self.verifyContainsString(full_name, self.on_my_schedule_page.get_provider_name())
        return self

    def should_see_color_slot_is_like(self, web_image):
        image_res = self.on_my_schedule_page.get_image_resource()
        image_des = self.on_my_schedule_page.capture_calenda_legend(web_image)
        self.compare_image_by_rgba(image_res, image_des)
        return self
