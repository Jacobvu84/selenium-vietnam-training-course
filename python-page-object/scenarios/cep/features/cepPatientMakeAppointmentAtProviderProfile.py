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
from steps.patient_steps import PatientHomeSteps
from steps.navigate_steps import NavigateSteps
from steps.font_end.provider.my_schedule import MyScheduleSteps

testID = sys.argv[1]  # test case ID


def patient_make_appointment_at_provider_profile():
    # Objects
    _actor = LoginSteps()
    _patient = PatientHomeSteps()
    _navigate = NavigateSteps()
    _my_schedule = MyScheduleSteps()

    start_date = date_time.get_weekday(datetime.datetime.today())
    end_date = date_time.get_next_date()
    start_time = "00:00"
    end_time = "00:00"

    try:

        # Provider creates slot
        _actor.browse_the_web().signin_as_provider(index=1)
        _navigate.goto_calendar_page()

        _my_schedule.create_slot(start_date, start_time, end_time) \
            .repeat("Mon,Tue,Wed,Thu,Fri,Sat,Sun") \
            .until(end_date)
        _actor.logout()

        # Patient select a provider and book an appointment
        _actor.access_waiting_room() \
            .signin_as_patient(0)

        _patient.select_a_doctor_and_book_an_appointment(1)

        _actor.logout()
        _actor.access_waiting_room() \
            .signin_as_patient(0)

        _patient.should_see_start_appointment_in_dashboard("Today")

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
    patient_make_appointment_at_provider_profile()


main()
