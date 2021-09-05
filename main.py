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
from scrapeFirstNamesFromLastNames import *

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



# this function opens the browser for further work
# for single scraping, use portable firefox.
# for parallel scraping, use ADS power.
#
def open_browser(mode):
    if mode == 'single':
        # open portable firefox, IP burger extension and the account with ipb should've been set up already.
        p_firefox = subprocess.Popen(['C:/Users/scadmin/Downloads/FirefoxPortable/FireFoxPortable.exe'])
        time.sleep(1)
    else:
        print('parallel work')
        p_adspower = subprocess.Popen(['C:/Program Files (x86)/AdsPower/AdsPower.exe'])
        time.sleep(1)

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
scrape_last_names(winloc)
# a = get_last_names('C:/CrawlerData/pages/lastname00.html')
# a = get_first_name_pages('C:/CrawlerData/pages/fullname00.htm')
# b = get_first_names('C:/CrawlerData/pages/fullname00.htm')
# c = get_details_info('C:/CrawlerData/pages/details00.htm')
# print(a)


# Windows
#chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
# webbrowser.get(chrome_path).open(url)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('PyCharm')

#open ADS power

# p_adspower = subprocess.Popen(['C:/Program Files (x86)/AdsPower/AdsPower.exe'])
# time.sleep(1)

# now click on batch input icon
# pyautogui.click('c:/AmazonSeller/JSRPA/aidata/batchinput.png')
# time.sleep(2)

# now select platform, set it to 'other'
# pyautogui.click('c:/AmazonSeller/JSRPA/aidata/adsplatformsel.png')
# time.sleep(1)
# pyautogui.move(0, 90)
# pyautogui.scroll(-1000)
# time.sleep(1)
# pyautogui.move(0, 400)
# pyautogui.click()
# time.sleep(1)

# pyautogui.click('c:/AmazonSeller/JSRPA/aidata/othersite.png')
# time.sleep(1)
# pyautogui.write('www.google.com')



# at the pop-up, click on upload icon
# pyautogui.click('c:/AmazonSeller/JSRPA/aidata/upload0.png')
# time.sleep(2)

# at the dialog window, do 3 things:
# 1) set the profile directory connect. 'C:/AmazonSeller/SelfSwipe' :
# 2) set the file type correctly 'All Files'
# 3) set the file name correctly 'user_list2021-06-03_47_56'
# pyautogui.click('c:/AmazonSeller/JSRPA/aidata/finput0_cn.png')
# time.sleep(1)
# pyautogui.write('C:\\AmazonSeller\\SelfSwipe\\')
# time.sleep(1)
# pyautogui.click()
# time.sleep(1)
# pyautogui.press('enter')
# time.sleep(1)
#
# pyautogui.click('c:/AmazonSeller/JSRPA/aidata/ftype0_cn.png')
# time.sleep(1)
# pyautogui.move(0, 90)
# time.sleep(1)
# pyautogui.click()
# time.sleep(1)

# pyautogui.click('c:/AmazonSeller/JSRPA/aidata/fninput0_cn.png')
# time.sleep(1)
# pyautogui.write('user_list2021-06-03_47_56.xls')
# time.sleep(1)
# # pyautogui.press('enter')
# time.sleep(1)

# ftype_button = pyautogui.locateOnScreen('ftype0_cn.png')
# ftype_loc = pyautogui.center(ftype_button)
# pyautogui.moveTo(ftype_loc)
# pyautogui.move(320, 60)
#
# pyautogui.click()
# time.sleep(1)
#
# pyautogui.click('c:/AmazonSeller/JSRPA/aidata/adsok0.png')
# time.sleep(5)
#
# pyautogui.click('c:/AmazonSeller/JSRPA/aidata/adspopok0.png')

# -----------------------
# pyautogui.click('c:/AmazonSeller/JSRPA/aidata/sncheckbox0.png')
# time.sleep(1)
# pyautogui.move(-120, -12)
# time.sleep(1)
# pyautogui.click()
# time.sleep(2)
# pyautogui.click('c:/AmazonSeller/JSRPA/aidata/openall0.png')
#
# time.sleep(60)
#
# # 'NNN - SunBrowser' will be the window title, ex: '291 - SunBrowser'
# print(gw.getAllTitles())

# -----------------------

# take a snap shot again.

# analyze the screen again,
# before "Search Alphabetically" are the names.
# find all "last name", then each one of them, the immediately word before, if not null, then
# it's the first name.
# all the digits between "Page:" and "People Directory" are the # of pages.


#im = Image.open("c:/AmazonSeller\JSRPA\nameaddr\A01.PNG")
#im.show()
#im.close()
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\Tesseract.exe'
#
# print(pytesseract.image_to_string(Image.open('c:\AmazonSeller\JSRPA\Capture.JPG')))
#
#
# print(pytesseract.image_to_boxes(Image.open('c:\AmazonSeller\JSRPA\Capture.JPG')))
#



# img = cv2.imread('c:\AmazonSeller\JSRPA\Capture.JPG')

#left is the distance from the upper-left corner of the bounding box, to the left border of the image.
#top is the distance from the upper-left corner of the bounding box, to the top border of the image.
#width and height are the width and height of the bounding box.
#conf is the model's confidence for the prediction for the word within that bounding box.
# If conf is -1, that means that the corresponding bounding box contains a block of text,
# rather than just a single word.
# d = pytesseract.image_to_data(img, output_type=Output.DICT)
# n_boxes = len(d['level'])
# for i in range(n_boxes):
#     (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
#     cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
#
# cv2.imshow('img', img)
# cv2.waitKey(0)
#
# time.sleep(3)


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
# p2 = subprocess.Popen(['../../usr/bin/jvisualvm'])
# p3 = subprocess.Popen(['docker-compose', '-f', 's3_dynamodb.yml', 'up'])

# p3.terminate()
# p2.terminate()
# p1.terminate()



# Running the aforementioned command and saving its output
# output = os.popen('wmic process get description, processid').read()

# Displaying the output
# print(output)

# print(gw.getAllTitles())

# print(gw.getAllWindows())










