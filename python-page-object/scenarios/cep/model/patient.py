__author__ = 'jacob@vsee.com'

import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.rand import generate
from util.rand import random_int


class Eligibility(object):
    # Eligibility should be set account code is the same with clinic code
    # SSN is only 4 digitals
    def __init__(self, firstname, lastname, DOB, SSN, email,
                 status=('1', 'Eligible'), account_code='cep-tuc1', gender=''):
        self.firstname = firstname
        self.lastname = lastname
        self.DOB = DOB
        self.SSN = SSN
        self.status = status
        self.account_code = account_code
        self.email = email
        self.gender = gender

# On-Duty
suka = Eligibility('User CEP 01', generate(30), '1982-11-17', random_int(4),
                   "evisitqa07+patient{0}@gmail.com".format(generate(30)))
doremon = Eligibility('User CEP 02', generate(40), '1982-10-25', random_int(4),
                      "evisitqa07+patient{0}@gmail.com".format(generate(40)))
nobita = Eligibility('User CEP 03', generate(50), '2012-12-24', random_int(4),
                     "evisitqa07+patient{0}@gmail.com".format(generate(50)))

eligibilities = [suka, doremon, nobita]

# SNF
anton = Eligibility('User SNF 01', generate(32), '1982-11-17', random_int(4), email = "", account_code = 'snf')
anna = Eligibility('User SNF 02', generate(42), '2012-10-25', random_int(4), email="", account_code='snf')

snf_eligibilities = [anton, anna]

# TelepSych
barbara = Eligibility('Patient Tele 01', generate(34), '1982-11-17', random_int(4),
                email="evisitqa07+patient{0}@gmail.com".format(generate(34)), account_code='telepsych', gender='Male')
roman = Eligibility('Patient Tele 02', generate(36), '1982-11-17', random_int(4),
                email="evisitqa07+patient{0}@gmail.com".format(generate(36)), account_code='telepsych', gender='Male')
yaya = Eligibility('Patient Tele 03', generate(38), '1982-11-17', random_int(4),
                email="evisitqa07+patient{0}@gmail.com".format(generate(38)), account_code='telepsych', gender='Male')
hanna = Eligibility('Patient Tele 04', generate(44), '2014-10-25', random_int(4),
                email="evisitqa07+patient{0}@gmail.com".format(generate(44)), account_code='telepsych', gender='Female')

tele_eligibilities = [barbara, roman, yaya, hanna]

patient_pwd = "Vsee@)!*2018"
patient_gmail = "evisitqa07@gmail.com"
password_gmail = "userPass"
