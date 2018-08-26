'''
Created on Jun 5, 2018

@author: Thang Nguyen
Steps for admin using
'''

import sys, os
from time import sleep
from shutil import copyfile

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from clinic.pages.common.login_page import LoginPage
from clinic.pages.admin.users_page import UsersPage
from clinic.pages.common.webchat_page import WebchatPage
from clinic.pages.common.launching_page import LaunchingPage
from clinic.pages.provider.dashboard_page import DashboardPage
from clinic.pages.provider.calendar_page import CalendarPage
from util.logger import Step
from util.support import wait_for_vsee_downloaded
from util.support import execute_file
from util.support import empty_dir_download
from util.mailbox import MailBox

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
from webium.clinic_page import ClinicPage
from testClass import runSikuli

class CommonSteps(ClinicPage):
    
    def __init__(self, ClinicPage):
        self.set_attribute(ClinicPage)
        
        self.login_page = LoginPage(ClinicPage)
        self.users_page = UsersPage(ClinicPage)
        self.dashboard_page = DashboardPage(ClinicPage)
        self.webchat_page = WebchatPage(ClinicPage)
        self.calendar_page = CalendarPage(ClinicPage)
        self.launching_page = LaunchingPage(ClinicPage)

    def signin_as_admin(self, username, pwd):
        self.login_page.click_on_login_link()
        self.login(username, pwd)
        self.users_page.check_visibile_of_users_link()
        return self
    
    def signin_as_clinic_admin(self, username, pwd):
        self.login_page.click_on_login_link()
        self.login(username, pwd)
        self.calendar_page.wait_visible_of_calendar_link()
        return self
    
    def signin_as_provider(self, username, pwd):
        self.login_page.click_on_login_link()
        self.login(username, pwd)
        self.calendar_page.wait_visible_of_calendar_link()
        return self

    def signin_as_patient(self, username, pwd):
        self.login_page.click_on_login_button()
        self.login(username, pwd)
        return self
    
    def signin_as_remote_medic(self, username, pwd):
        self.login_page.click_on_login_link()
        self.login(username, pwd)

    def login(self, username, pwd):
        self.login_page.enter_username(username)
        self.login_page.enter_password(pwd)
        self.login_page.click_on_submit_button()
        return self
    
    def install_vsee(self, src):
        if self.os_type != "OSX":
            empty_dir_download()
        if self.manual_detection:   # IE doesn't need to click install VSee
            self.launching_page.click_into_install_vsee()
        if self.os_type == "OSX":
            if runSikuli.runMac("ocLaunch.sikuli", [self.testID, src]) != 0:
                raise
        else:
            if self.browser_type != "edge": # installation for edge is inside ocLaunch
                wait_for_vsee_downloaded()
                
                if self.manual_detection:
                    execute_file()
            
            if runSikuli.runWin("ocLaunch.sikuli", [self.testID, src, self.browser_type, self.os_type]) != 0:
                    raise
        
        if self.manual_detection:
            self.launching_page.click_into_installation_next()
            if self.os_type != "OSX":
                self.launching_page.click_into_start_test()
                
    def launch_vsee(self, src, install_flag):
        log_path = "/Users/vsee/Documents/vseeLog.txt"
        temp_dir_mac = "/Users/vsee/Documents/tempDIR/"
        if not install_flag and self.manual_detection:
            self.launching_page.click_into_proceed_to_consultation()
        self.info("Launch VSee client via sikuli")
        if self.os_type == "OSX":
            # Remove previous log in case script failed, we will get vsee log
            if os.path.isfile(log_path):
                os.remove(log_path)
            if runSikuli.runMac("focusVSee.sikuli", [self.testID, src]) != 0:
                # Copy vseeLog to testID folder
                # This should be created by result function
                if os.path.isfile(log_path):
                    fileName = "vseeLog_" + src + ".txt" 
                    copyfile(log_path, temp_dir_mac + self.testID + "/" + fileName)
                raise
        else:
            if self.browser_type == "edge":
                if runSikuli.runWin("edgeSwitchApp.sikuli", [self.testID]) != 0:
                    raise
            if runSikuli.runWin("ocLaunch2.sikuli", [self.testID, src, str(install_flag), 
                                                     self.browser_type, self.single_video, 
                                                     self.start_call]) != 0:
                raise
        self.info("Wait for launching modal disappears")
        self.launching_page.wait_invisible_of_launching_modal() 
    
    # Wait for starting call
    def wait_call(self, src, dst):
        if self.os_type == "OSX":
            sleep(40)
            if runSikuli.runMac("waitCall.sikuli", [self.testID, src, dst, str(300)]) != 0:
                raise
        else:    
            if runSikuli.runWin("waitCall.sikuli", [self.testID, src, dst, str(300), 
                                                    self.single_video, self.three_way_call]) != 0:
                raise
    
    # Ending the call
    def end_call(self, src, dst, end_flag):
        if self.os_type == "OSX":
            if runSikuli.runMac("endcall.sikuli", [self.testID, src, dst, str(end_flag)]) != 0:
                raise
        else:        
            if runSikuli.runWin("endcall.sikuli", [self.testID, src, dst, str(end_flag), 
                                                   self.single_video, self.three_way_call]) != 0:
                raise
    
    # For checking if call has ended 
    def wait_end_call(self, src):
        if self.os_type == "OSX":
            if runSikuli.runMac("waitEndcall.sikuli", [self.testID, src, str(180)]) != 0:
                raise
        else:        
            if runSikuli.runWin("waitEndcall.sikuli", [self.testID, src, str(180), 
                                                       self.single_video, self.three_way_call]) != 0:
                raise
    
    def launch_vsee_again(self, src):
        log_path = "/Users/vsee/Documents/vseeLog.txt"
        self.info("Launch VSee client via sikuli")
        if self.os_type == "OSX":
            # Thang: Remove previous log in case script failed, we will get vsee log
            if os.path.isfile(log_path):
                os.remove(log_path)
            if runSikuli.runMac("focusVSee.sikuli", [self.testID, src]) != 0:
                raise
            print 'proceed the current VSee'    
        else:        
            # Thang: On edge browser, we need to accept switch app
            if self.bType == "Edge":
                if runSikuli.runWin("edgeSwitchApp.sikuli", [self.testID]) != 0:
                    raise
            if runSikuli.runWin("ocLaunch2.sikuli", [self.testID, src, "0", self.browser_type, 
                                                     self.single_video, self.start_call]) != 0:
                raise
            
    def send_webchat_message(self, chat_content, username = ""):
        self.webchat_page.type_into_webchat(chat_content, username)
    
    def wait_for_webchat_message(self, chat_content, username="", timeout=60):
        self.webchat_page.wait_for_webchat_content(chat_content, username, timeout)
    
    def verify_email(self, email, password, subject, content = "", get_url=False):
#         mail_box = MailBox(email, password)
        with MailBox(email, password) as mail_box:
            (url, email_content) = mail_box.wait_for_email_subject(subject, get_url=get_url)
        if content != "":
            self.info("Email received")
            print "\n".join([ll.rstrip() for ll in email_content.splitlines() if ll.strip()])
            print "***************************"
            content = content.format(url)   # Add url into content
            self.info("Email content expected")
            print content.encode("utf-8")
            if not content.encode("utf-8") in "\n".join([ll.rstrip() for ll in email_content.splitlines() if ll.strip()]):
                self.error("Email content does not match.")
        return (url, email_content)