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
from steps.font_end.provider.dashboard import DashBoardSteps
from steps.font_end.provider.my_patient import AllVisitSteps
from steps.navigate_steps import NavigateSteps

testID = sys.argv[1]  # test case ID

def clinic_admin_new_visit_without_vsee_type():
    _actor = LoginSteps()
    _new_visit = NewVisitSteps()
    _dashboard = DashBoardSteps()
    _navigate = NavigateSteps()
    _all_visit = AllVisitSteps()

    index = 2
    odtc = ODTC()
    room_name = odtc.get_room_name_by(env='tele')
    date_app = date_time.get_current_datetime()
    # Patient Tele 03
    patient_index = 2
    patients = odtc.get_tele_patient()
    f_name = patients[patient_index].split(",")[1]
    l_name = patients[patient_index].split(",")[2]
    email = patients[patient_index].split(",")[0]

    full_name = f_name + " " + l_name

    try:
        # CA/SA will create visit/appointment
        _actor\
            .visit_telepsych() \
            .signin_as_provider(env='tele', index=index)
        _new_visit\
            .open_new_visit_form() \
            .create_visit_with_new_patient(room=room_name,
                                           first_name=f_name,
                                           last_name=l_name,
                                           email=email,
                                           gender='Male',
                                           dob='1982-11-17',
                                           visit_type='Video (Other)',
                                           visit_option='30-min Consultation',
                                           date_time='Now') \
            .should_see_visit_details(visit_type='Video (Other)',
                                      visit_option='30-min Consultation',
                                      date_time="Now (" + date_app,
                                      patient_name=full_name)\
            .go_to_visit_detail_page('Are you going to review this visit now?', 'no')

        # Nurse starts to enter the WR for patient
        _actor \
            .logout() \
            .visit_telepsych() \
            .signin_as_nurse(env='tele', index=2)
        _dashboard \
            .should_see_the_cancel_button(full_name) \
            .should_not_see_the_start_appointment_button(full_name)\
            .cancel_appointment(full_name,
                                reason="Hospital needed to reschedule",
                                des="Change visit type is VSee")
        _navigate\
            .goto_my_patients()\
            .re_type_password()

        _all_visit \
            .search_history_visit_by(value=email) \
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
    clinic_admin_new_visit_without_vsee_type()


main()
