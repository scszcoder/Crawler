
# this functions processes an html file.
from bs4 import BeautifulSoup

from logger import *
import numpy
from readScreen import subfinder
import re
import random
from calendar import isleap


class userAddr:
    def __init__(self):
        self.street = ''
        self.city = ''
        self.state = ''
        self.country = ''
        self.zip = ''
        self.type = ''          # 'R' for residential, 'B' for business


class userInfo:
    def __init__(self):
        self.first_name = ''
        self.last_name = ''
        self.suffix = ''
        self.birth_year = 0
        self.birth_month = 0
        self.birth_day = 0
        self.phones = ''
        self.addresses = []
        self.emails = []
        self.used = False
        self.user = ''
        self.used_date = ''

def get_last_names(html_file):
    last_names = []
    # parse the last name page to obtain a list of last names.
    soup = BeautifulSoup(html_file, 'html.parser')
    print(soup)

    atags = soup.find_all('a')
    pn_i = [i for i, t in enumerate(atags) if len(t.contents) == 1 and not t.contents[0].name]
    pn = numpy.array(atags)[pn_i].tolist()
    n = (o.contents[0] for o in pn)

    start = subfinder(n, ['Name', 'Phone'], 'Address')
    end_name = subfinder(n, ['1'])
    end_number = subfinder(n, ['A', 'B', 'C'])

    start_idx = start[0]+3

    if len(end_name) == 0:
        # this means that the last names are only enough to fill one page.
        end_idx = end_number[0]
    else:
        end_idx = end_name[0]

    last_names_i = [i for i, ln in enumerate(n) if i > start_idx and i < end_idx ]
    print(last_names_i)
    last_names = numpy.array(n)[last_names_i].tolist()
    print(last_names)
    print(len(last_names))

    return last_names


def get_first_name_pages(html_file):
    num_pages = 1
    # parse the last name page to obtain a list of last names.
    soup = BeautifulSoup(html_file, 'html.parser')
    print(soup)

    atags = soup.find_all('a')
    pn_i = [i for i, t in enumerate(atags) if len(t.contents) == 1 and not t.contents[0].name]
    pn = numpy.array(atags)[pn_i].tolist()
    n = (o.contents[0] for o in pn)

    end_name = subfinder(n, ['1'])
    end_number = subfinder(n, ['A', 'B', 'C'])

    if len(end_name) != 0:
        # this means that the last names are only enough to fill one page.
        num_pages_idx = end_number[0] - 1
        num_pages = n[num_pages_idx]

    return num_pages


def get_first_names(html_file):
    full_names = []
    # parse the last name page to obtain a list of last names.
    soup = BeautifulSoup(html_file, 'html.parser')
    print(soup)

    atags = soup.find_all('a')
    pn_i = [i for i, t in enumerate(atags) if len(t.contents) == 1 and not t.contents[0].name]
    pn = numpy.array(atags)[pn_i].tolist()
    n = (o.contents[0] for o in pn)

    start = subfinder(n, ['Name', 'Phone'], 'Address')
    end_name = subfinder(n, ['1'])
    end_number = subfinder(n, ['A', 'B', 'C'])

    start_idx = start[0]+3

    if len(end_name) == 0:
        # this means that the last names are only enough to fill one page.
        end_idx = end_number[0]
    else:
        end_idx = end_name[0]

    last_names_i = [i for i, ln in enumerate(n) if i > start_idx and i < end_idx ]
    print(last_names_i)
    full_names = numpy.array(n)[last_names_i].tolist()
    print(full_names)
    print(len(full_names))

    return full_names


def get_details_info(html_file):
    usr = userInfo()
    addr = userAddr()
    soup = BeautifulSoup(html_file, 'html.parser')
    # all useful information are here:
    useful = soup.findAll('div', {"class": lambda t: t in ('content-label h5', 'content-value')})
    ageuseful = soup.findAll('span', {"class": 'content-value'})
    agewords = ageuseful[0].text.split(' ')
    usr.birth_year = int(agewords[3][0:4])
    usr.birth_month = get_birth_month(agewords[2][1:4])
    days = get_month_days(usr.birth_year, usr.birth_month)
    usr.birth_day = random.randrange(1, days+1)

    # print(agewords[0][1:4])     # ’age'
    # print(agewords[1])          # age in number
    # print(agewords[2][1:4])     # birth month
    # print(agewords[3][0:4])     # birth year

    for item in useful:
        atags = item.find_all('a')
        if len(atags) == 0:
            # deal with email related stuff here
            if re.search('[a-zA-Z].*\@.*\.[a-zA-Z]', item.text):
                usr.emails.append(re.search('[a-zA-Z].*\@.*\..*[a-zA-Z]', item.text).group())
            elif re.search('Age', item.text):
                astring = re.search('Age', item.text).group()
                print(astring)
        else:
            for x in atags:
                a = x.find_all('span')
                for l in a:
                    if l.get('itemprop') == 'streetAddress':
                        addr.street = l.text
                    elif l.get('itemprop') == 'addressLocality':
                        addr.city = l.text
                    elif l.get('itemprop') == 'addressRegion':
                        addr.state = l.text
                    elif l.get('itemprop') == 'postalCode':
                        addr.zip = l.text
                if (addr.street != ''):
                    usr.addresses.append(addr)

    return usr


def get_birth_month(month_word):
    month = 0
    if month_word == 'Jan':
        month = 1
    elif month_word == 'Feb':
        month = 2
    elif month_word == 'Mar':
        month = 3
    elif month_word == 'Apr':
        month = 4
    elif month_word == 'May':
        month = 5
    elif month_word == 'Jun':
        month = 6
    elif month_word == 'Jul':
        month = 7
    elif month_word == 'Aug':
        month = 8
    elif month_word == 'Sep':
        month = 9
    elif month_word == 'Oct':
        month = 10
    elif month_word == 'Nov':
        month = 11
    elif month_word == 'Dec':
        month = 12
    return month


def get_month_days(year, month):
    days = 0
    if month == 1:
        month = 31
    elif month == 'Feb':
        month = 28
        if isleap(year):
            month = 29
    elif month == 'Mar':
        month = 31
    elif month == 'Apr':
        month = 30
    elif month == 'May':
        month = 31
    elif month == 'Jun':
        month = 30
    elif month == 'Jul':
        month = 31
    elif month == 'Aug':
        month = 31
    elif month == 'Sep':
        month = 30
    elif month == 'Oct':
        month = 31
    elif month == 'Nov':
        month = 30
    elif month == 'Dec':
        month = 31
    return days



