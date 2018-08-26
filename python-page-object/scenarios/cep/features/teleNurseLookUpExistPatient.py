__author__ = 'jacob@vsee.com'

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.console import start_test
from util.support import create_gif
from util.mailbox import MailBox
from resource import ODTC

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from steps.login_steps import LoginSteps
from steps.font_end.nurse.nurse_steps import NurseSteps
from steps.install_steps import InstallSteps
from steps.font_end.provider.dashboard import DashBoardSteps

from model.patient import patient_gmail
from model.patient import password_gmail

testID = sys.argv[1]  # test case ID
bType = sys.argv[2]  # type of browser
osType = sys.argv[3]  # type of platform
userID = int(sys.argv[4])  # userID
src = sys.argv[5]  # Local VM ID
dst = sys.argv[6]  # Remote VM ID
is_install = int(sys.argv[7])  # Install VSee client if equal to 1


def nurse_walk_in():
    # Objects
    _actor = LoginSteps()
    _nurse = NurseSteps()
    _install = InstallSteps()
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

    try:
        with MailBox(patient_gmail, password_gmail) as mbox:
            mbox.delete_all()
        # WHEN: Nurse creates the visit
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
            .account_lookup(patient=f_name + " " + l_name+ ", " + dob) \
            .create_new_patient_record(
                legal_status="The patient is involuntary and a psychiatric consultation has been ordered.") \
            .add_contact_information(option='ignore') \
            .reason_for_visit("Suicide Attempt") \
            .click_to_continue() \
            .patient_vitals(hr='99 BPM',
                            bp='180/120 mmHg',
                            temp='38 C',
                            rr='99 BPM',
                            height='60 Inches',
                            weight='80 lb',
                            upload='yes') \
            .past_medical_history(conditions='Stroke, Asthma') \
            .should_see_the_past_medical_history_is_updated('Depression, Diabetes, Stroke, Thyroid problem') \
            .past_surgeries(procedures='Joint replacement') \
            .should_see_the_past_surgeries_is_updated('Heart valve replaced, Hernia repair, Joint replacement') \
            .medications(names='Sick') \
            .should_see_the_medications_is_updated('Headaches, Depression, Sick') \
            .allergies(drug_name='Vsee Clinic') \
            .should_see_the_allergies_is_updated('5HT1 agonist,12 Hour Nasal, Vsee Clinic') \
            .click_to_continue() \
            .please_select_a_visit_option(visit_option='45-min Consultation') \
            .select_the_psychiatrist_to_see_availability(2) \
            .pick_an_available_time_slot()

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
    nurse_walk_in()


main()
