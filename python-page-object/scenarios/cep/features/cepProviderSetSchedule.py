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


# Tester thread
def set_schedule():
    _actor = LoginSteps()
    _navigate = NavigateSteps()
    _my_schedule = MyScheduleSteps()

    start_date = date_time.get_weekday(datetime.datetime.today())
    end_date = date_time.get_next_date()
    start_time = "00:00"
    end_time = "00:00"

    try:
        _actor.browse_the_web().signin_as_provider()
        _navigate.goto_calendar_page()

        _my_schedule.create_slot(start_date, start_time, end_time) \
            .repeat("Mon,Tue,Wed,Thu,Fri,Sat,Sun") \
            .until(end_date).should_see_message_is_shown("Success! Slots created successfully.") \
            .should_see_slot_is_created("12:00 - 12:00") \
            .should_see_provider_name()

        # Create slot without today default
        new_start_date = date_time.get_next_date(4)
        new_end_date = date_time.get_next_date(8)
        new_start_time = "01:15"
        new_end_time = "02:30"
        _my_schedule.create_slot_with_change_start_date(new_start_date, new_start_time, new_end_time) \
            .repeat("Mon,Tue,Wed,Thu,Fri,Sat,Sun") \
            .until(new_end_date) \
            .should_see_message_is_shown("Success! Slots created successfully.") \
            .should_see_slot_is_created("1:15 - 2:30") \
            .should_see_provider_name()

        print "[PASSED]: TEST PASSED"
    except Exception as e:
        print type(e)
        print e.args
        print e
        print "[FAILED]: TEST FAILED"

    finally:
        _actor.quit()
        create_gif()


def main():
    start_test()
    set_schedule()


main()
