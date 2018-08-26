__author__ = 'jacob@vsee.com'

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.console import start_test
from util.support import create_gif

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from steps.login_steps import LoginSteps
from steps.navigate_steps import NavigateSteps
from steps.font_end.help_steps import HelpSteps

testID = sys.argv[1]  # test case ID


# Tester thread
def help_menu():
    _actor = LoginSteps()
    _navigate = NavigateSteps()
    _help = HelpSteps()

    try:
        # Provider checks help content
        _actor.browse_the_web().signin_as_provider()
        _navigate.goto_help_page()
        _help.should_see_title("TECHNICAL SUPPORT") \
            .should_see_body_description(
            "If you are experiencing technical issues, please email us at onduty@vituity.com.|"
            "When contacting us, please provide:") \
            .should_see_information_need_provide('"On Duty" as the app name|'
                                                 'Your employer or payer (ex. Central Hospital, Google, Blue Cross).') \
            .close_help_window()
        _actor.logout()

        # Patient checks help content
        _actor.access_waiting_room().signin_as_patient()
        _navigate.goto_help_page()
        _help.should_see_title("TECHNICAL SUPPORT") \
            .should_see_body_description(
            "If you are experiencing technical issues, please email us at onduty@vituity.com.|"
            "When contacting us, please provide:") \
            .should_see_information_need_provide('"On Duty" as the app name|'
                                                 'Your employer or payer (ex. Central Hospital, Google, Blue Cross).') \
            .close_help_window()
        _actor.logout()

        # Guest checks help content
        _actor.access_waiting_room().login_as(username="vsee.guest@gmail.com", password="VseeGuest2018")
        _navigate.goto_help_page()
        _help.should_see_title("TECHNICAL SUPPORT") \
            .should_see_body_description(
            "If you are experiencing technical issues, please email us at onduty@vituity.com.|"
            "When contacting us, please provide:") \
            .should_see_information_need_provide('"On Duty" as the app name|'
                                                 'Your employer or payer (ex. Central Hospital, Google, Blue Cross).') \
            .close_help_window()

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
    help_menu()


main()
