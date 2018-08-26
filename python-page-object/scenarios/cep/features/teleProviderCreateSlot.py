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


def nurse_walk_in():
    # Objects
    _actor = LoginSteps()
    _navigate = NavigateSteps()
    _my_schedule = MyScheduleSteps()

    start_date = date_time.get_weekday(datetime.datetime.today())
    end_date = date_time.get_next_date()
    start_time = "00:00"
    end_time = "00:00"

    try:
        # GIVEN: Provider creates the schedules
        _actor\
            .visit_telepsych()\
            .signin_as_provider(env='tele')
        _navigate\
            .goto_calendar_page()
        _my_schedule\
            .create_slot(start_date, start_time, end_time) \
            .repeat("Mon,Tue,Wed,Thu,Fri,Sat,Sun") \
            .until(end_date)\
            .should_see_message_is_shown("Success! Slots created successfully.") \
            .should_see_slot_is_created("12:00 - 12:00") \

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
    nurse_walk_in()


main()
