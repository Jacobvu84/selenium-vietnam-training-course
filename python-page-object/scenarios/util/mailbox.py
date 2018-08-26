#!/usr/bin/env python

"""MailBox class for processing IMAP email.

(To use with Gmail:
    1. enable IMAP access in your Google account settings
    2. Allow less secure apps: ON)

usage with GMail:

    import mailbox

    with mailbox.MailBox(gmail_username, gmail_password) as mbox:
        print mbox.get_count()
        print mbox.print_msgs()


for other IMAP servers, adjust settings as necessary.
"""

import imaplib
import time, re
from email import email
import logging
import datetime
from waiting import wait

IMAP_SERVER = 'imap.gmail.com'
IMAP_PORT = '993'
IMAP_USE_SSL = True

EMAIL_FOLDER = 'Inbox'


def get_timestamp():
    return datetime.datetime.now().strftime("%Y-%d-%m  %H:%M:%S")


class MailBox(object):
    def __init__(self, user, password):
        self.log = logging.getLogger('report')
        self.user = user
        self.password = password
        if IMAP_USE_SSL:
            self.imap = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        else:
            self.imap = imaplib.IMAP4(IMAP_SERVER, IMAP_PORT)

    def __enter__(self):
        self.log.debug('%s [DEBUG] : Sign in Gmail with username %s' % (get_timestamp(), self.user))
        self.imap.login(self.user, self.password)
        return self

    def __exit__(self, type, value, traceback):
        self.imap.close()
        self.imap.logout()

    def get_count(self):
        self.imap.select(EMAIL_FOLDER)
        status, data = self.imap.search(None, 'ALL')
        return sum(1 for num in data[0].split())

    def fetch_message(self, num):
        self.imap.select(EMAIL_FOLDER)
        status, data = self.imap.fetch(str(num), '(RFC822)')
        email_msg = email.message_from_string(data[0][1])
        return email_msg

    def delete_message(self, num):
        self.imap.select('Inbox')
        self.imap.store(num, '+FLAGS', r'\Deleted')
        self.imap.expunge()

    def delete_all(self):
        self.log.debug('%s [DEBUG] : Delete all mails in the Inbox' % (get_timestamp()))
        self.imap.select('Inbox')
        status, data = self.imap.search(None, 'ALL')
        for num in data[0].split():
            self.imap.store(num, '+FLAGS', r'\Deleted')
        self.imap.expunge()

    def get_latest_email_sent_to(self, email_address, timeout=300, poll=1):
        start_time = time.time()
        while ((time.time() - start_time) < timeout):
            # It's no use continuing until we've successfully selected
            # the inbox. And if we don't select it on each iteration
            # before searching, we get intermittent failures.
            status, data = self.imap.select(EMAIL_FOLDER)
            if status != 'OK':
                time.sleep(poll)
                continue
            status, data = self.imap.search(None, 'TO', email_address)
            data = [d for d in data if d is not None]
            if status == 'OK' and data:
                for num in reversed(data[0].split()):
                    status, data = self.imap.fetch(num, '(RFC822)')
                    email_msg = email.message_from_string(data[0][1])
                    return email_msg
            time.sleep(poll)
        raise AssertionError("No email sent to '%s' found in inbox "
                             "after polling for %s seconds." % (email_address, timeout))

    def delete_msgs_sent_to(self, email_address):
        self.imap.select(EMAIL_FOLDER)
        status, data = self.imap.search(None, 'TO', email_address)
        if status == 'OK':
            for num in reversed(data[0].split()):
                status, data = self.imap.fetch(num, '(RFC822)')
                self.imap.store(num, '+FLAGS', r'\Deleted')
        self.imap.expunge()

    def print_msgs(self):
        self.imap.select(EMAIL_FOLDER)
        status, data = self.imap.search(None, 'ALL')
        for num in reversed(data[0].split()):
            status, data = self.imap.fetch(num, '(RFC822)')
            self.log.debug('%s [DEBUG] : Message %s\n%s\n' % (get_timestamp(), num, data[0][1]))

    # Function to get activation code from email
    def get_activation_code_mobile(self, subject):
        self.log.debug("[INFO]: Get Activation Code Mobile")
        code = ""
        self.imap.select(EMAIL_FOLDER)
        numUnread = len(self.imap.search(None, '(UNSEEN)')[1][0].split())
        if numUnread > 0:  # connect to inbox and check mail count
            result, data = self.imap.uid('search', None, "ALL")
            latest_email_uid = data[0].split()[-1]
            result, data = self.imap.uid('fetch', latest_email_uid,
                                         '(RFC822)')  # fetch the email body (RFC822) for the given ID
            raw_email = data[0][1]  # here's the body, which is raw text of the whole email
            # including headers and alternate payloads

            email_message = email.message_from_string(raw_email)
            self.log.debug(email_message)
            if subject in email_message['subject']:
                # Because of the way the URL Link is formatted inside the email, we need to process it before using it
                self.log.debug("[INFO]: There is an email")
                lines = str(email_message).splitlines()
                for line in lines:
                    if "within 24 hours" in line:
                        code = lines[lines.index(line) + 1]
                        if len(code) < 6:
                            code = lines[lines.index(line) + 2]
                        code = code.replace(" ", "")
                        code = code.replace("=", "")
                        code = code.replace("0D", "")
                        self.log.debug("[INFO]: Activation code is: " + code)
                        self.imap.select(EMAIL_FOLDER)
                        typ, data = self.imap.search(None, 'ALL')
                        for num in data[0].split():
                            self.imap.store(num, '+FLAGS', r'(\Deleted)')
                        break
            self.imap.expunge()
        return code

    # Using to get first url inside an email and its decoded content
    def get_link_and_content_mail(self, email_subject):
        link = ""
        body = ""
        self.imap.select(EMAIL_FOLDER)
        numUnread = len(self.imap.search(None, '(UNSEEN)')[1][0].split())
        if numUnread > 0:  # connect to inbox and check mail count
            result, data = self.imap.uid('search', None, "ALL")
            latest_email_uid = data[0].split()[-1]
            result, data = self.imap.uid('fetch', latest_email_uid,
                                         '(RFC822)')  # fetch the email body (RFC822) for the given ID
            raw_email = data[0][1]  # here's the body, which is raw text of the whole email
            # including headers and alternate payloads
            email_message = email.message_from_string(raw_email)
            # self.log.debug(str(email_message))
            if email_subject in email_message['subject']:
                # Because of the way the URL Link is formatted inside the email, we need to process it before using it
                self.log.debug("[DEBUG] : You've Got Mail")
                
                # we get email body to check content
                if email_message.is_multipart():
                    for part in email_message.walk():
                        ctype = part.get_content_type()
                        cdispo = str(part.get('Content-Disposition'))

                        # skip any text/plain (txt) attachments
                        if ctype == 'text/plain' and 'attachment' not in cdispo:
                            body = part.get_payload(decode=True)  # decode
                            break
                # not multipart - i.e. plain text, no attachments, keeping fingers crossed
                else:
                    body = email_message.get_payload(decode=True)
                self.log.debug("[DEBUG] :" + body)
                link = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                                  body)
                
                try:
                    link = link[0]  # If there's url
                except:
                    link = ""  # return empty
                
            self.imap.expunge()
        return link, body
    
    def wait_for_email_subject(self, email_subject, get_url=False, timeout=300):
        self.log.debug("[DEBUG] : wait for email with subject: {0}".format(email_subject))
        self.link = ""
        self.content = ""
        def check_new_mail_by_subject():
            try:
                self.link, self.content = self.get_link_and_content_mail(email_subject)
                if get_url:
                    if len(self.link) > 0:
                        self.log.debug("[DEBUG] : url is {0}".format(self.link))
                        return (self.link, self.content)
                    self.log.debug("[DEBUG] : Wait 5s and try to get URL again.")
                    time.sleep(5)
                    return False
                else:
                    if len(self.content) > 0:
                        return (self.link, self.content)
                    self.log.debug("[DEBUG] : Wait 5s and try to check email again.")
                    time.sleep(5)
                    return False
            except Exception as e:
                self.log.debug(str(e))
                self.log.debug("[DEBUG] : Wait 5s and try to check email again.")
                time.sleep(5)
                return False
        
        wait(lambda: check_new_mail_by_subject(), waiting_for='Wait for email by subject',
                 timeout_seconds=timeout)
        
        return (self.link, self.content)