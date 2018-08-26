__author__ = 'jacob@vsee.com'

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.console import start_test
from util.support import create_gif

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from steps.login_steps import LoginSteps
from steps.navigate_steps import NavigateSteps
from steps.font_end.patient.patient_health import PatientHealthSteps
from steps.font_end.patient.patient_health import PatientMedicalHistorySteps

testID = sys.argv[1]  # test case ID


def edit_medical_history():
    # Objects
    _actor = LoginSteps()
    _navigate = NavigateSteps()
    _patient = PatientHealthSteps()
    _medical_history = PatientMedicalHistorySteps()

    try:
        _actor.access_waiting_room().signin_as_patient()
        _navigate.goto_health()
        _patient.select_medical_history_tab()

        # Past Medical History
        _medical_history.should_see_the_past_medical_history("Depression,"
                                                             "Headaches (Migraines),"
                                                             "Heart burn (GERD),"
                                                             "Anorexia and Bulimia,"
                                                             "Irregular heart beat,"
                                                             "Asthma") \
            .remove_past_medical_history("Anorexia and Bulimia,Headaches (Migraines),Irregular heart beat") \
            .add_past_medical_history("Cancer,Stroke").add_other_condition("Selenium") \
            .should_see_the_past_medical_history("Asthma,Depression,Cancer,Stroke,Selenium,Heart burn (GERD)")

        # Past Surgeries
        _medical_history.update_past_surgeries("Part of my bowels removed,Hernia repair").add_more_procedure("Appium")

        # Family Medical History
        _medical_history.open_family_medical_check_list() \
            .update_mother_medical_history("Alcoholism,Asthma,Heart disease") \
            .update_father_medical_history("Stroke,Thyroid disease") \
            .update_siblings_medical_history("Diabetes,Osteoporosis") \
            .update_maternal_grandparents_medical_history("Mental illness/depression,Migraines") \
            .update_paternal_grandparents_medical_history("Cancer (including skin cancer),Ulcer disease") \
            .close_family_medical_check_list() \
            .should_see_family_medical_history_is_updated("Alcoholism: Mother,"
                                                          "Asthma: Mother,"
                                                          "Cancer (including skin cancer): Paternal grandparents,"
                                                          "Diabetes: Siblings,"
                                                          "Heart disease: Mother,"
                                                          "Mental illness/depression: Maternal grandparents,"
                                                          "Migraines: Maternal grandparents,"
                                                          "Osteoporosis: Siblings,"
                                                          "Stroke: Father,"
                                                          "Thyroid disease: Father,"
                                                          "Ulcer disease: Paternal grandparents")

        # Social History
        _medical_history.update_social_history("In a relationship", "College or equivalent", "IT", "2") \
            .should_see_social_history_is_updated("Marital Status: In a relationship,"
                                                  "Highest Level of Education: College or equivalent,"
                                                  "Occupation: IT,"
                                                  "Number of children: 2")
        # Health Habits
        _medical_history.update_health_habits("Daily", "Weekly", "Angel dust", "Daily") \
            .should_see_health_habits_is_updated("Smoking Frequency: Daily,"
                                                 "Alcohol Frequency: Weekly,"
                                                 "Street Drugs Used: Angel dust,"
                                                 "Exercise Frequency: Daily")

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
    edit_medical_history()


main()
