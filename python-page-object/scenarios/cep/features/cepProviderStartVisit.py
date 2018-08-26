__author__ = 'jacob@vsee.com'

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.console import start_test
from util.support import create_gif

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from steps.login_steps import LoginSteps
from steps.font_end.provider.dashboard import DashBoardSteps
from steps.font_end.provider.control_panel import ControlPanelSteps
from steps.font_end.provider.visit_note import VisitNoteSteps
from steps.install_steps import InstallSteps

testID = sys.argv[1]  # test case ID
bType = sys.argv[2]  # type of browser
osType = sys.argv[3]  # type of platform
userID = int(sys.argv[4])  # userID
src = sys.argv[5]  # Local VM ID
dst = sys.argv[6]  # Remote VM ID
is_install = int(sys.argv[7])  # Install VSee client if equal to 1
installFlagMem = int(sys.argv[8])  # Wait for Member installation
editPMHx = int(sys.argv[9])  # if 1 then Provider will edit the PMHx info of patient
checkSurveyFlag = int(sys.argv[10])  # if 1 then Check Provider Post Visit Survey will be on
endFlag = int(sys.argv[11])  # Local ends the call


# Tester thread
def start_visit():
    _actor = LoginSteps()
    _dashboard = DashBoardSteps()
    _control_panel = ControlPanelSteps()
    _install = InstallSteps()
    _visit_note = VisitNoteSteps()

    try:
        _actor.browse_the_web().signin_as_provider()

        # provider start Visit
        _dashboard.select_patient_in_lounge()
        _control_panel.make_video_call()
        if is_install:
            _install.install_vsee()
        _install.launch_vsee(is_install)
        _install.accept_privacy_and_term_GDPR()

        _control_panel.visit("provider_visit.png") \
            .end_call(testID, src, dst, endFlag)

        if editPMHx:
            # Put also the Editing Chief Complaint here to test as well
            _visit_note.should_see_the_reason_for_visit_that_sent_by_patient("Back pain,Chest pain") \
                .provider_edit_chief_complaint("Rash,Fever") \
                .provider_remove_chief_complaint("Back pain") \
                .should_see_the_past_medical_history_that_sent_by_patient("Depression,"
                                                                          "Heart burn (GERD),"
                                                                          "Headaches (Migraines),"
                                                                          "Anorexia and Bulimia") \
                .provider_edit_past_medical_history("Irregular heart beat,Asthma") \
                .should_see_the_allergies_that_sent_by_patient("5HT1 agonist,12 Hour Nasal") \
                .provider_edit_allergies("Apresoline,Moxifloxacin") \
                .should_see_the_medications_that_sent_by_patient("Amoxicillin,Paracetamol") \
                .provider_edit_medications("Hypertension,Metoprolol")

        _visit_note.provider_write_comment_plan_or_discharge_instructions("NOT eat meat, fish, milk, egg") \
            .complete__and_sent_visit_to_patient() \
            .feedback_on_patient().submit().should_see_back_to_lounge()

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
    start_visit()


main()
