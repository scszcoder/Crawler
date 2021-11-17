# this file contains a bunch of UI utility functions to be used throughout...
import pyautogui
import cv2
import numpy as np

import os, sys, time, argparse
import subprocess
import xlrd
import pathlib

import pygetwindow as gw

from logger import *

def scroll_then_snap(loc, cnt, fn):
    # read details from the page.
    pyautogui.moveTo(loc[0], loc[1])
    pyautogui.click()
    pyautogui.scroll(cnt)
    im = im = pyautogui.screenshot('fn', region=(0,0, 300, 400))


def click_then_snap(loc, fn):
    # read details from the page.
    pyautogui.moveTo(loc[0], loc[1])
    pyautogui.click()
    im = pyautogui.screenshot('fn', region=(0, 0, 300, 400))


# this function assume a browser window is already brought to the front, the windows location is
# pointed at the html address input field location.
def open_url_then_save_page(win_loc, url, html_path, html_file_name):
    # ss stands for screen save
    log_1(html_path)
    log_1(html_file_name)
    fn = 'C:/CrawlerData/fftemplates/ff_save_as_dialog.png'
    # first, open a html file.
    pyautogui.hotkey('ctrl', 't')
    pyautogui.write(url)
    pyautogui.hotkey('enter')
    time.sleep(8)

    # now save the web page into a file.
    pyautogui.hotkey('ctrl', 's')
    time.sleep(3)

    win_titles = gw.getAllTitles()
    saveas_diag_titles = [i for i in win_titles if 'Save As' in i]

    if len(saveas_diag_titles) >= 1:
        saveas_diag_title = saveas_diag_titles[len(saveas_diag_titles)-1]
        print("window title:", saveas_diag_title)
    else:
        print("Something is Wrong, Save As Not Started.")

    saveas_diag_win = gw.getWindowsWithTitle(saveas_diag_title)[0]
    saveas_diag_win.moveTo(win_loc[0], win_loc[0])
    time.sleep(5)

    pyautogui.screenshot(fn, region=(win_loc[0], win_loc[1], 1600, 900))
    dir_loc = find_dir_name_box(fn)
    # log_1(dir_loc)
    pyautogui.moveTo(dir_loc[1], dir_loc[0])
    time.sleep(1)
    pyautogui.click()
    time.sleep(1)
    pyautogui.press('backspace')
    time.sleep(1)
    # log_1(str(pathlib.PureWindowsPath(html_path)))
    pyautogui.write(str(pathlib.PureWindowsPath(html_path)))
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)

    loc = find_file_name_box(fn)
    # log_1(loc)
    pyautogui.moveTo(loc[1], loc[0])
    time.sleep(1)
    pyautogui.click()
    time.sleep(1)
    pyautogui.press('backspace')
    time.sleep(2)
    pyautogui.write(html_file_name)
    time.sleep(2)

    button_image = 'C:/CrawlerData/fftemplates/page_save_as_save_button.png'
    pyautogui.click(button_image)
    time.sleep(5)
    # close the tab, back to where it was.
    pyautogui.hotkey('ctrl', 'w')
    time.sleep(3)



# input: screen save file name.
# output: on the screen saving image, find and return the location of the file name input box.
def find_dir_name_box(sfn):
    log_1('Searching in: ' + sfn)
    image = cv2.imread(sfn)
    # mat full star, 0.8, match empty star 0.80, match half star 0.8.
    template = cv2.imread('C:/CrawlerData/fftemplates/ff_save_as_dir_entrance.png')
    icon_height = template.shape[0]
    icon_width = template.shape[1]
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    # log_1(result)
    loc = np.where(result >= 0.85)
    count = 0
    # get the full star match count.
    for pt in zip(*loc[::-1]):  # Swap columns and rows
        count = count + 1

    if count > 0:
        log_1('found the dir input location!!!')
        match = (loc[0][0], loc[1][0])
        input_loc = (match[0] + int(0.5 * icon_height), match[1] - 0.5*icon_width)
    else:
        log_1('Error finding the location to input file name.....')
        input_loc = (0, 0)

    return input_loc


# input: screen save file name.
# output: on the screen saving image, find and return the location of the file name input box.
def find_file_name_box(sfn):

    image = cv2.imread(sfn)
    # mat full star, 0.8, match empty star 0.80, match half star 0.8.
    template = cv2.imread('C:/CrawlerData/fftemplates/page_save_as_file_name.png')
    icon_height = template.shape[0]
    icon_width = template.shape[1]
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    # log_1(result)
    loc = np.where(result >= 0.85)
    count = 0
    # get the full star match count.
    for pt in zip(*loc[::-1]):  # Swap columns and rows
        count = count + 1

    if count > 0:
        # log_1(loc)
        match = (loc[0][0], loc[1][0])
        input_loc = (match[0] + int(0.5 * icon_height), match[1]+2*icon_width)
    else:
        log_1('Error finding the location to input file name.....')
        input_loc = (0, 0)

    return input_loc


# open ADS power, resize the window to the specified size, and move the window to the specified location.
# input: window location, window size
# output: status (whether the window is opened or not)
def open_ads(win_height, win_width, win_loc):
    p_adspower = subprocess.Popen(['C:/Program Files (x86)/AdsPower/AdsPower.exe'])
    time.sleep(8)
    win_titles = gw.getAllTitles()
    wins = gw.getAllWindows()

    ads_titles = [i for i in win_titles if 'AdsPower' in i]
    if len(ads_titles) == 1:
        ads_title = ads_titles[0]
        print("window title:", ads_title)
    else:
        print("Something is Wrong, ADS Power Not Started.")

    ads_idx = [idx for idx, s in enumerate(win_titles) if 'AdsPower' in s][0]

    ads_win = gw.getWindowsWithTitle(ads_title)[0]
    ads_win.resizeTo(win_width, win_height)
    ads_win.moveTo(win_loc[0], win_loc[0])
    time.sleep(5)
    scr = pyautogui.screenshot('c:/my_screenshot.png', region=(win_loc[0], win_loc[0], win_width, win_height))


# open ADS power, resize the window to the specified size, and move the window to the specified location.
# input: window location, window size
# output: status (whether the window is opened or not)
def open_portable_firefox(win_height, win_width, win_loc):
    p_firefox = subprocess.Popen(['C:/Users/scadmin/Downloads/FirefoxPortable/FireFoxPortable.exe'])
    time.sleep(5)
    win_titles = gw.getAllTitles()
    wins = gw.getAllWindows()

    ff_titles = [i for i in win_titles if 'Mozilla Firefox' in i]
    log_1(ff_titles)
    if len(ff_titles) >= 1:
        ff_title = ff_titles[0]
        print("window title:", ff_title)
    else:
        print("Something is Wrong, Firefox Not Started.")

    ff_idx = [idx for idx, s in enumerate(win_titles) if 'Mozilla Firefox' in s][0]

    ff_win = gw.getWindowsWithTitle(ff_title)[0]
    ff_win.resizeTo(win_width, win_height)
    ff_win.moveTo(win_loc[0], win_loc[0])
    time.sleep(3)
    scr = pyautogui.screenshot('c:/CrawlerData/my_screenshot.png', region=(win_loc[0], win_loc[0], win_width, win_height))

# load an account profile list file into ADS, then, open these account into terminals,
# return a list of window handlers.
def load_ads(pfile):
    winhs = []

    # in ads,
    # match 'batch import' and click
    # in the pop up, run tesseract, match 'Click or drag file here to upload' and click,
    # in the pop up, locate file directory path input box, write the file path.
    #               locate file type 'Custom Files' and click, select 'All Files',
    #                in file list, in file name input box, type in file name.
    #               then, click 'open' button
    # in ADS, locate select all check box (next to 'serial number'), click on it, and click on all open icon.


    return winhs

# for each account's opened browser windows, set the widow position and size,
# type in 'Ctrl-T' to open a new tab, after this action, the mouse will be automatically put into the html box, and
# we can type right there.
# return: all of the position and size , and html input box's locations of the windows that are successfully connected.
def set_up_window(url, cwin):
    winp = []
    pyautogui.hotkey('ctrl', 't')
    pyautogui.write(url)
    pyautogui.hotkey('enter')
    # the following sequence brings a window to the front.
    cwin.minimize()
    cwin.restore()
    cwin.activate()



