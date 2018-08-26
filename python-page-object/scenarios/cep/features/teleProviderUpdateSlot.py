__author__ = 'jacob@vsee.com'

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.console import start_test
from util.support import create_gif
from util import date_time
import datetime

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from steps.login_steps import LoginSteps

from steps.navigate_steps import NavigateSteps
from steps.font_end.provider.my_schedule import MyScheduleSteps

testID = sys.argv[1]  # test case ID


def provider_edit_slot():
    # Objects
    _actor = LoginSteps()
    _navigate = NavigateSteps()
    _my_schedule = MyScheduleSteps()

    start_date = date_time.get_weekday(datetime.datetime.today())
    start_time = "00:00"
    end_time = "00:00"

    try:
        # DELETE SLOT
        _actor.visit_telepsych().signin_as_provider(env='tele', index=1)
        _navigate.goto_calendar_page()
        _my_schedule \
            .create_slot(start_date, start_time, end_time) \
            .confirm() \
            .should_see_message_is_shown("Success! Slots created successfully.") \
            .should_see_slot_is_created("12:00 - 12:00")
        _my_schedule \
            .delete_slot("12:00 - 12:00") \
            .should_see_message_is_shown("Success! Slot has been deleted successfully.")
        # EDIT SLOT
        _navigate.goto_calendar_page()
        _my_schedule \
            .create_slot(start_date, "02:00", "05:00") \
            .confirm() \
            .should_see_message_is_shown("Success! Slots created successfully.") \
            .should_see_slot_is_created("2:00 - 5:00")

        _my_schedule \
            .edit_slot("2:00 - 5:00", start_time, end_time) \
            .update() \
            .should_see_message_is_shown("Success! Slot updated successfully.") \
            .should_see_slot_is_created("12:00 - 12:00")

        _my_schedule\
            .should_see_color_slot_is_like("calendarLegend")

        print "[PASSED]: TEST PASSED"
    except Exception as e:
        print type(e)
        print e.args
        print e
        print "[INFO]: TEST FAILED"
    finally:
        _actor.quit()
        create_gif()


def main():
    start_test()
    provider_edit_slot()


main()
