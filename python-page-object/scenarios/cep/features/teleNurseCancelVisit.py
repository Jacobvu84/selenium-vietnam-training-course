__author__ = 'jacob@vsee.com'

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.console import start_test
from resource import ODTC
from util.support import create_gif

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from steps.login_steps import LoginSteps
from steps.font_end.nurse.nurse_steps import NurseSteps
from steps.install_steps import InstallSteps
from steps.navigate_steps import NavigateSteps
from steps.font_end.provider.my_patient import MyPatientSteps
from steps.font_end.provider.my_patient import AllVisitSteps
from steps.font_end.provider.dashboard import DashBoardSteps

testID = sys.argv[1]  # test case ID
bType = sys.argv[2]  # type of browser
osType = sys.argv[3]  # type of platform
userID = int(sys.argv[4])  # userID
src = sys.argv[5]  # Local VM ID
dst = sys.argv[6]  # Remote VM ID
is_install = int(sys.argv[7])  # Install VSee client if equal to 1


def nurse_cancel_visit():
    # Objects
    _actor = LoginSteps()
    _nurse = NurseSteps()
    _install = InstallSteps()
    _navigate = NavigateSteps()
    _my_patient = MyPatientSteps()
    _all_visit = AllVisitSteps()
    _dashboard = DashBoardSteps()

    patient_index = 3

    odtc = ODTC()
    patients = odtc.get_tele_patient()
    f_name = patients[patient_index].split(",")[1]
    l_name = patients[patient_index].split(",")[2]
    dob = patients[patient_index].split(",")[3]
    name = f_name + " " + l_name

    try:
        _actor \
            .visit_telepsych() \
            .signin_as_nurse(env='tele', index=1)

        _nurse \
            .enter_patient_information(first_name=f_name,
                                       last_name=l_name,
                                       dob=dob,
                                       gender="Male",
                                       encounter_no="VSEE9999999",
                                       medical_record_no="VSEE888888") \
            .account_lookup(patient='new') \
            .create_new_patient_record(
                            legal_status="The patient is voluntary and has consented to a telepsychiatry evaluation.") \
            .add_contact_information(option='ignore') \
            .reason_for_visit("Agitation, Paranoia") \
            .click_to_continue() \
            .click_to_continue() \
            .please_select_a_visit_option(visit_option='45-min Consultation') \
            .select_the_psychiatrist_to_see_availability(1) \
            .pick_an_available_time_slot()
        _dashboard \
            .start_appointment_for(name)

        # VM is installed the first time
        if is_install:
            _install.install_vsee()
        _install.launch_vsee(is_install)
        _install.accept_privacy_and_term_GDPR()

        _nurse\
            .exit_the_appointment()\

        _navigate\
            .goto_my_patients()\
            .re_type_password()

        _my_patient \
            .select_tab("All Visits") \
            .should_see_the_all_visit_history_table_with_columns("Visit Time,Patient,Waiting Room,Provider,"
                                                                 "Gender,Age,Email,Visit Status,Action")

        _all_visit \
            .search_history_visit_by(value=name) \
            .should_see_the_status_visit("Deleted")

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
    nurse_cancel_visit()


main()
