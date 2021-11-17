# This is a sample Python script.
import admin
import os, sys, time, argparse
import subprocess

from PIL import Image

import webbrowser
import subprocess
import pyautogui

import subprocess
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import tkinter
import xlrd
import pygetwindow as gw

import pytesseract
import cv2
from pytesseract import Output
from csv import reader
import webbrowser

from bs4 import BeautifulSoup

from readScreen import subfinder

from readScreen import *

from processHTML import *
from scrapeLastNames import *
from getDetails import *
from scrapeFirstNamesFromLastNames import *
from scrapeMaleFemaleFirstNames import *

from sendCloud import *

# this function scrape names first.
# first scrape all last names.
# last names will be organized into last name csv files, file names will be in the format of:
# EndingLastName_StaringLastName_.csv, each file contains 8192 last names.
#
# names are scraped into csv files, each csv file contains at most 8192 names,
# the name of the CSV files will EndingLastName_EnedingFirstName_StartingLastName_StartingFirstName_.csv
# the csv file will be in the format of:
#  last name, first name, last name page index, first name, page index, single letter status (O for no record, X for completion)
# The last name will be William Zick, if we find this name in our list of files
# that means all names have been obtained.
# first, find the last name and first name done so far, and start from there,
# generate
# input: current record.
# output: an excutable plan





# this function make the plan for the current run.
# Note: because of the duplicated names, a single name could create
# a lot of records.
# To make our API not heavily loaded, we limit each record to
# 16 name records.
# input: current record.
# output: an excutable plan
def make_plans(current_record):
    planTBE = ''
    print("making plans")
    return planTBE


# this function will run a single scraper instance
# input: plans contains a list of names to scrape
# output: scape execution status/record.
def run_single_scraper(plans):
    execRecord = ''
    print("running single scraper")
    return execRecord

# input: plans contains a list of names to scrape
# output: scape execution status/record.
# this function will utilizes multiple ADS power acct+copy to scrape task
def run_multi_scraper(plans):
    execRecord = ''
    print("running multiple scrapers")
    return execRecord

# last names, each page has about 100 last names, so all about 77000 last names. then
# each last name has many pages of first names, each page again has about 100 first names, so


# if not admin.isUserAdmin():
#     admin.runAsAdmin()

# first, obtain all names, due to memory constraint, we'll scrape 8K names or about
# 512KB per csv file.
winloc = [0, 0]
open_portable_firefox(2000, 3000, winloc)
time.sleep(5)

cloud_session = set_up_cloud()
# scrape_full_names(winloc)
# scrape_details(winloc)

# scrape order:
# 1) male female first names
scrape_male_female_first_names(winloc, cloud_session)

# 2) all last names in USA, save in local files.
scrape_last_names(winloc)

# 3) all full names in USA, save in local files.
scrape_full_names(winloc)

# 3) all full names in USA, save in local files.
scrape_details(winloc, cloud_session)

##############################################################################
# code snippet testing graphQL query string format.
##############################################################################
# The following is a proven working string
# important note:
#  *) key needs no quote
#  *) value needs double quote ", not single quote '
#  *) array value []
#  *) date must be XXXX-XX-XX, single digit month or day needs to have 0 in front
#  *) minimum email format is "
# mutation MyMutation {
#   createPeople(input: [{birthday: "1980-02-01", emails: ["abd@def.com"], firstName: "abc", lastName: "def", phones: ["512-333-5555", "512-222-3333"], addrs: [{city: "San Jose", state: "CA", street1: "abc def", zip: "78739", street2: "", endDate: "2000-10-10", startDate: "1998-10-10"}, {city: "San Jose", state: "CA", street1: "abc def", zip: "78739", street2: "", endDate: "2010-12-12", startDate: "1990-11-11"}], middleName: "", suffix: ""}, {birthday: "1980-02-01", emails: ["abd@def.com"], firstName: "abc", lastName: "def", phones: ["512-333-5555", "512-222-3333"], addrs: [{city: "San Jose", state: "CA", street1: "abc def", zip: "78739", street2: "", endDate: "2000-10-10", startDate: "1998-10-10"},
#     {city: "San Jose", state: "CA", street1: "abc def", zip: "78739", street2: "", endDate: "2010-12-12", startDate: "1990-11-11"}], middleName: "", suffix: ""}]) {
#     result
#   }
# }
###################################end of snippet ############################################



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('PyCharm')


# book = xlrd.open_workbook("myfile.xls")
# print("The number of worksheets is {0}".format(book.nsheets))
# print("Worksheet name(s): {0}".format(book.sheet_names()))
# sh = book.sheet_by_index(0)
# print("{0} {1} {2}".format(sh.name, sh.nrows, sh.ncols))
# print("Cell D30 is {0}".format(sh.cell_value(rowx=29, colx=3)))
# for rx in range(sh.nrows):
#     print(sh.row(rx))

# os.system("program_name") # To open any program by their name recognized by windows
#
# os.startfile("path to application or any file") # Open any program, text or office document
#
# os.close(filename);
# os.system("TASKKILL /F /IM firefox.exe")
# subprocess.call(["taskkill","/F","/IM","firefox.exe"])
#
# p1 = subprocess.Popen(['workspace/eclipse/eclipse'])
# p1.terminate()



# Running the aforementioned command and saving its output
# output = os.popen('wmic process get description, processid').read()

# print(gw.getAllTitles())
# print(gw.getAllWindows())










