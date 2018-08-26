__author__ = 'jacob@vsee.com'

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.console import start_test
from util.support import create_gif
from util import date_time
from resource import ODTC

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from steps.login_steps import LoginSteps
from steps.font_end.provider.new_visit import NewVisitSteps
from steps.navigate_steps import NavigateSteps
from steps.font_end.provider.dashboard import DashBoardSteps
from steps.font_end.provider.my_patient import AllVisitSteps

testID = sys.argv[1]  # test case ID

def nurse_cancel_visit_Created_by_admib():
    _actor = LoginSteps()
    _new_visit = NewVisitSteps()
    _dashboard = DashBoardSteps()
    _navigate = NavigateSteps()
    _all_visit = AllVisitSteps()
    odtc = ODTC()

    index = 3
    patient_index = 0

    room_name = odtc.get_room_name_by(env='tele')
    patients = odtc.get_tele_patient()

    f_name = patients[patient_index].split(",")[1]
    l_name = patients[patient_index].split(",")[2]
    full_name = f_name + " " + l_name

    not_now = date_time.get_next_date()

    try:
        # CA/SA will create visit/appointment
        _actor\
            .visit_telepsych() \
            .signin_as_provider(env='tele', index=index)
        _new_visit\
            .open_new_visit_form() \
            .should_see_visit_type("Video (Other), Phone, Video (VSee)") \
            .should_see_visit_type_focus_on("Video (Other)") \
            .should_see_date_and_time_type("Now, Schedule for a later time") \
            .should_see_date_and_time_focus_on("Now") \
            .create_new_visit(room=room_name,
                              patient_name=full_name,
                              visit_type='Video (VSee)',
                              visit_option='30-min Consultation',
                              date_time='Schedule for a later time', date=not_now, time='09:00 AM') \
            .should_see_visit_details(visit_type='Video (VSee)',
                                      visit_option='30-min Consultation',
                                      date_time=not_now + " 09:00 AM",
                                      patient_name=full_name)\
            .go_to_visit_detail_page('Are you going to review this visit now?', 'no')

        # Nurse starts to enter the WR for patient
        _actor \
            .logout() \
            .visit_telepsych() \
            .signin_as_nurse(env='tele')
        _dashboard \
            .cancel_appointment(patient=full_name,
                                reason="Hospital needed to reschedule",
                                des="All Doctors are busy")
        _navigate\
            .goto_my_patients()\
            .re_type_password()

        _all_visit \
            .search_history_visit_by(value=full_name) \
            .should_see_the_status_visit("Deleted")

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
    nurse_cancel_visit_Created_by_admib()


main()
