__author__ = 'jacob@vsee.com'

import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.rand import random_int
from util.rand import random_state
from util.rand import random_npi
from util.rand import generate


class Subtype(object):
    def __init__(self, subtype="Provider"):
        self.subtype = subtype


class Demographics(object):
    def __init__(self, email, firstname="", lastname="", username="", password="", confirm_pwd="", title='Dr.', suffix='Ph.D',
                 phone='650.390.6970', street='514 S. Magnolia St.', city='Orlando', state='Florida', zip="32806",
                 specialties="Default", statesLicensed="All Locations", statesServiced="All Locations"):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.password = password
        self.confirm_pwd = confirm_pwd
        self.email = email
        self.title = title
        self.suffix = suffix
        self.phone = phone
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip
        self.specialties = specialties
        self.statesLicensed = statesLicensed
        self.statesServiced = statesServiced


class License(object):
    def __init__(self, npi=random_npi(), dea="FJ" + str(random_int(7)), specialties="Default",
                 statesLicensed=random_state(), statesServiced="All Locations"):
        self.dea = dea
        self.npi = npi
        self.specialties = specialties
        self.statesLicensed = statesLicensed
        self.statesServiced = statesServiced


class Profile(object):
    def __init__(self, medicalSchool='Harvard Medical School', internship='New York University School of Medicine',
                 residency='Ophthalmology', language="English", shortBio='evisitqa06+test{last_name}@gmail.com',
                 picture='VSeeLogo.png'):
        self.medicalSchool = medicalSchool
        self.internship = internship
        self.residency = residency
        self.language = language
        self.shortBio = shortBio
        self.picture = picture


class Assignment(object):
    def __init__(self, values=None, byClinics=None, byRooms=True):
        self.byClinics = byClinics
        self.byRooms = byRooms
        self.values = values


class Provider(object):
    def __init__(self, subtype, license, profile, assignment, demographics, role=""):
        self.subtype = subtype
        self.demographics = demographics
        self.license = license
        self.profile = profile
        self.assignment = assignment
        self.role = role


main_email = "evisitqa06@gmail.com"
email_pwd = "userPass"

provider_name = 'evisitqa06+test'
domain = '@gmail.com'

new_pass = 'Vsee@)!*2018'
reset_pass = 'Vsee2018@)!*'

profile = Profile()
assignment = Assignment()


# On-Duty
subtype = Subtype()
license = License()
johns = Provider(subtype, license, profile, assignment,
                 demographics=Demographics("{0}{1}{2}".format(provider_name, generate(10), domain),
                                           "Provider CEP 01", generate(10)))
david = Provider(subtype, license, profile, assignment,
                 demographics=Demographics("{0}{1}{2}".format(provider_name, generate(13), domain),
                                           "Provider CEP 02", generate(13)))
mary = Provider(subtype, license, profile, assignment,
                demographics=Demographics("{0}{1}{2}".format(provider_name, generate(16), domain),
                                          "Provider CEP 03", generate(16)))
providers = [johns, david, mary]

# SNF
## Nurse
subtype = Subtype("SNF Nurse")
license = License("", "")

lucy = Provider(subtype, license, profile, assignment,
                demographics=Demographics("{0}{1}{2}".format(provider_name, generate(22), domain),
                                          "Nurse SNF 01", generate(22), generate(22), new_pass, new_pass))
suong = Provider(subtype, license, profile, assignment,
                 demographics=Demographics("{0}{1}{2}".format(provider_name, generate(25), domain),
                                           "Nurse SNF 02", generate(25), generate(25), new_pass, new_pass, ))
snf_nurses = [lucy, suong]

## Provider
subtype = Subtype()
license = License("", "")
jimmy = Provider(subtype, license, profile, assignment,
                demographics=Demographics("{0}{1}{2}".format(provider_name, generate(31), domain),
                                         "Provider SNF 01", generate(31)))
giggs = Provider(subtype, license, profile, assignment,
                 demographics=Demographics("{0}{1}{2}".format(provider_name, generate(34), domain),                                      "Provider SNF 02", generate(34)))
snf_providers = [jimmy, giggs]

# Telepsych
## Nurse
subtype = Subtype("Nurse")
license = License("", "")
sam = Provider(subtype, license, profile, assignment,
                 demographics=Demographics("{0}{1}{2}".format(provider_name, generate(37), domain),
                                           "Nurse Telep 01", generate(37), generate(37), new_pass, new_pass))
robin = Provider(subtype, license, profile, assignment,
                  demographics=Demographics("{0}{1}{2}".format(provider_name, generate(43), domain),
                                            "Nurse Telep 02", generate(43), generate(43), new_pass, new_pass))
stamp = Provider(subtype, license, profile, assignment,
                  demographics=Demographics("{0}{1}{2}".format(provider_name, generate(19), domain),
                                            "Nurse Telep 03", generate(19), generate(19), new_pass, new_pass))
irwin = Provider(subtype, license, profile, assignment,
                  demographics=Demographics("{0}{1}{2}".format(provider_name, generate(23), domain),
                                            "Nurse Telep 04", generate(23), generate(23), new_pass, new_pass))
telepsych_nurses = [sam, robin, stamp, irwin]

## Provider
subtype = Subtype()
license = License("", "")

physician = Provider(subtype, license, profile, assignment,
            demographics=Demographics("{0}{1}{2}".format(provider_name, generate(51), domain),
                                                   "Provider Telep 01", generate(51)))
doctor = Provider(subtype, license, profile, assignment,
         demographics=Demographics("{0}{1}{2}".format(provider_name, generate(54), domain),
                                               "Provider Telep 02", generate(54)))
super_admin = Provider(subtype, license, profile, assignment,
              demographics=Demographics("{0}{1}{2}".format(provider_name, generate(46), domain),
                                           "Super Admin Telep", generate(46)), role='Super admin')
clinic_admin = Provider(subtype, license, profile, assignment,
               demographics=Demographics("{0}{1}{2}".format(provider_name, generate(49), domain),
                                           "Clinic Admin Telep", generate(49)), role='Clinic admin')
support_admin = Provider(subtype, license, profile, assignment,
                demographics=Demographics("{0}{1}{2}".format(provider_name, generate(57), domain),
                                          "Support Admin Telep", generate(57)), role='Support admin')
telepsych_providers = [physician, doctor, super_admin, clinic_admin, support_admin]

# Neuro
## Provider
subtype = Subtype()
license = License("", "")

physician = Provider(subtype, license, profile, assignment,
            demographics=Demographics("{0}{1}{2}".format(provider_name, generate(60), domain),
                                                   "Provider Neuro 01", generate(60)))
doctor = Provider(subtype, license, profile, assignment,
         demographics=Demographics("{0}{1}{2}".format(provider_name, generate(64), domain),
                                               "Provider Neuro 02", generate(64)))
neuro = Provider(subtype, license, profile, assignment,
        demographics=Demographics("{0}{1}{2}".format(provider_name, generate(68), domain),
                                               "Provider Neuro 03", generate(68)))
neuro_providers = [physician, doctor, neuro]

