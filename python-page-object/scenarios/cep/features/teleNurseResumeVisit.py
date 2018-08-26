__author__ = 'jacob@vsee.com'

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.console import start_test
from util.support import create_gif
from resource import ODTC

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from steps.login_steps import LoginSteps
from steps.font_end.nurse.nurse_steps import NurseSteps
from steps.install_steps import InstallSteps
from steps.font_end.provider.dashboard import DashBoardSteps
from steps.navigate_steps import NavigateSteps
from steps.font_end.provider.my_patient import MyPatientSteps
from steps.font_end.provider.my_patient import AllVisitSteps

testID = sys.argv[1]  # test case ID
bType = sys.argv[2]  # type of browser
osType = sys.argv[3]  # type of platform
userID = int(sys.argv[4])  # userID
src = sys.argv[5]  # Local VM ID
dst = sys.argv[6]  # Remote VM ID
is_install = int(sys.argv[7])  # Install VSee client if equal to 1


def nurse_resume_visit():
    # Objects
    _actor = LoginSteps()
    _nurse = NurseSteps()
    _install = InstallSteps()
    _navigate = NavigateSteps()
    _my_patient = MyPatientSteps()
    _all_visit = AllVisitSteps()
    _dashboard = DashBoardSteps()

    odtc = ODTC()

    # Nurse Tele 02
    # Provider Tele 02
    # Patient Tele 02
    patient_index = 1
    patients = odtc.get_tele_patient()
    f_name = patients[patient_index].split(",")[1]
    l_name = patients[patient_index].split(",")[2]
    dob = patients[patient_index].split(",")[3]
    full_name = odtc.get_fullname_patient(env='tele', index=patient_index)

    try:
        # WHEN: Nurse resume the visit
        _actor \
            .visit_telepsych() \
            .signin_as_nurse(env='tele', index=1)

        _nurse \
            .enter_patient_information(first_name=f_name,
                                       last_name=l_name,
                                       dob=dob,
                                       gender="Male",
                                       encounter_no="VSEE99912347",
                                       medical_record_no="VSEE658974",
                                       insurance_type="") \
            .account_lookup(patient=f_name + " " + l_name + ", " + dob) \
            .create_new_patient_record(
            legal_status="The patient is involuntary and a psychiatric consultation has been ordered.") \
            .add_contact_information(option='ignore') \
            .reason_for_visit("Suicide Attempt") \
            .click_to_continue() \
            .click_to_continue() \
            .please_select_a_visit_option(visit_option='45-min Consultation') \
            .select_the_psychiatrist_to_see_availability(2) \
            .pick_an_available_time_slot()

        _navigate\
            .goto_my_patients()\
            .re_type_password()

        _my_patient\
            .select_tab("All Visits")
        _all_visit \
            .search_history_visit_by(value=full_name) \
            .should_see_the_status_visit("Confirmed")

        _navigate\
            .goto_dashboard()
        _dashboard \
            .start_appointment_for(f_name)
        # VM is installed the first time
        if is_install:
            _install.install_vsee()
        _install.launch_vsee(is_install)
        _install.accept_privacy_and_term_GDPR()

        _nurse \
            .wait_doctor_visit(testID, src, dst) \
            .wait_doctor_complete_visit(testID, src) \
            .end_visit()

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
    nurse_resume_visit()


main()
