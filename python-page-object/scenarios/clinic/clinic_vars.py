'''
Created on May 31, 2018

@author: Thang Nguyen

Initialize variables that needed to test for VC project
'''
#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os, sys
import ConfigParser
import base64
import calendar
import time

running_production = False
beta_production = False
var = ConfigParser.RawConfigParser()
var.read(os.path.dirname(os.path.realpath(__file__)) + '/var.cfg')

config = ConfigParser.RawConfigParser()
config.read(os.path.dirname(os.path.realpath(__file__)) + '/../../clinic.cfg')

# use this password for all emails
user_pass = config.get('account', 'password')

# admin password
admin_pass = config.get('admin.user', 'password')

# epoc time to generate new accounts
epoc_minute = var.getint('time', 'epoc')
# VC
vc_patient_email = var.get('VC', 'patient')
vc_provider_email = var.get('VC', 'provider')

# FS
fs_patient_email_1 = var.get('FS', 'patient')
fs_patient_email_2 = var.get('FS', 'patient1')
fs_provider_email_1 = var.get('FS', 'provider')
fs_provider_email_2 = var.get('FS', 'provider1')

# for webdriver
browser_list = ["ie", "firefox", "chrome", "safari", "edge"] # Available to test
manual_detection = ["firefox", "chrome", "safari", "edge"]
ie_path = "C:\\tempFiles\\IEDriverServer.exe"
chrome_path = "C:\\tempFiles\\chromedriver.exe"
edge_path = "C:\\tempFiles\\MicrosoftWebDriver.exe"

# vseeLog on desktop
vsee_log_path = "C:\\Users\\vsee\\Desktop\\"
vsee_log_name = "vseeLog.txt"

# download location
download_folder = "C:\\Users\\vsee\\downloads\\"

# admin password
if running_production:
    vc_admin_pass_encoded = config.get('account.cmo.product', 'password')
    vc_admin_pass = base64.decodestring(vc_admin_pass_encoded)[::-1]
else:
    vc_admin_pass = config.get('admin.user', 'password')
    
if __name__ == "__main__":
    var.set("time", "epoc", str(calendar.timegm(time.gmtime())/60))
    with open(os.path.dirname(os.path.realpath(__file__)) + '/var.cfg', 'wb') as config:
        var.write(config)
        config.close()
