
# this functions processes an html file.
from bs4 import BeautifulSoup

from logger import *
import numpy
from readScreen import subfinder
import re
import random
from calendar import isleap
import shutil
import json


class userInfo:
    def __init__(self):
        self.first_name = ''
        self.last_name = ''
        self.suffix = ''
        self.birth_year = 0
        self.birth_month = 0
        self.birth_day = 0
        self.phones = []
        self.emails = []
        self.used = False
        self.user = ''
        self.used_date = ''
        self.addresses = []

    def asDict(self):
        dict = self.__dict__
        dict["addresses"] = [child.__dict__ for child in dict["addresses"]]
        return dict

    class userAddr:
        def __init__(self):
            self.street = ''
            self.city = ''
            self.state = ''
            self.country = ''
            self.zip = ''
            self.type = ''  # 'R' for residential, 'B' for business

def get_last_names(html_file):
    last_names = []
    # parse the last name page to obtain a list of last names.
    with open(html_file) as fp:
        soup = BeautifulSoup(fp, 'html.parser')
    # print(soup)

    atags = soup.find_all('a')
    # all a tag with 1 element and no name attribute inside.
    pn_i = [i for i, t in enumerate(atags) if len(t.contents) == 1 and not t.contents[0].name]
    pn = numpy.array(atags)[pn_i].tolist()
    n = [o.contents[0] for o in pn]
    # log_1(n)
    start = subfinder(n, ['Name', 'Phone', 'Address'])
    # log_1(str(start))
    end_name = subfinder(n, ['1'])
    # log_1(str(end_name))
    end_number = subfinder(n, ['A', 'B', 'C'])
    # log_1(str(end_number))

    start_idx = start[0]+3

    if len(end_name) == 0:
        # this means that the last names are only enough to fill one page, such as 'X' initiated last names.
        end_idx = end_number[0]
    else:
        end_idx = end_name[0]

    last_names_i = [i for i, ln in enumerate(n) if i >= start_idx and i < end_idx ]
    # print(last_names_i)
    last_names = numpy.array(n)[last_names_i].tolist()
    # print(last_names)
    # print(len(last_names))

    return last_names


def get_first_name_pages(html_file):
    num_pages = 1
    # parse the last name page to obtain a list of last names.
    with open(html_file) as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    # print(soup)

    atags = soup.find_all('a')
    pn_i = [i for i, t in enumerate(atags) if len(t.contents) == 1 and not t.contents[0].name]
    pn = numpy.array(atags)[pn_i].tolist()
    n = [o.contents[0] for o in pn]

    end_name = subfinder(n, ['1'])
    end_number = subfinder(n, ['A', 'B', 'C'])

    if len(end_name) != 0:
        # this means that the last names are only enough to fill one page.
        num_pages_idx = end_number[0] - 1
        num_pages = n[num_pages_idx]
    log_1(num_pages)
    fp.close()
    return num_pages


def get_first_names(html_file):
    full_names = []
    # parse the last name page to obtain a list of last names.
    with open(html_file) as fp:
        soup = BeautifulSoup(fp, 'html.parser')
    # print(soup)

    atags = soup.find_all('a')
    pn_i = [i for i, t in enumerate(atags) if len(t.contents) == 1 and not t.contents[0].name]
    pn = numpy.array(atags)[pn_i].tolist()
    n = [o.contents[0] for o in pn]

    start = subfinder(n, ['Name', 'Phone', 'Address'])
    end_name = subfinder(n, ['1'])
    end_number = subfinder(n, ['A', 'B', 'C'])

    start_idx = start[0]+3

    if len(end_name) == 0:
        # this means that the last names are only enough to fill one page.
        end_idx = end_number[0]
    else:
        end_idx = end_name[0]

    last_names_i = [i for i, ln in enumerate(n) if i >= start_idx and i < end_idx ]
    print(last_names_i)
    full_names = numpy.array(n)[last_names_i].tolist()
    print(full_names)
    print(len(full_names))

    fp.close()
    return full_names


def get_details_info(html_file):
    users = []
    usr = userInfo()
    addr = userInfo.userAddr()
    with open(html_file, encoding="utf8") as fp:
        soup = BeautifulSoup(fp, 'html.parser')
    # all useful information are here:
    useful = soup.findAll('div', {"class": lambda t: t in ('content-label h5', 'content-value')})
    ageuseful = soup.findAll('span', {"class": 'content-value'})
    print(ageuseful)

    # createa N users according to number of age information found in the html file.
    for i in range(len(ageuseful)):
        usr = userInfo()
        agewords = ageuseful[i].text.split(' ')
        usr.birth_year = int(agewords[3][0:4])
        usr.birth_month = get_birth_month(agewords[2][1:4])
        print('Year, Month ', usr.birth_year, ' ', usr.birth_month)
        days = get_month_days(usr.birth_year, usr.birth_month)
        usr.birth_day = random.randrange(1, days+1)
        users.append(usr)

    # set up prev_l for later processing.
    prev_l = useful[0]
    found = False
    # print('how many are useful? ', len(useful))
    for obj in useful:
        a0tags = obj.find_all('a')
        if len(a0tags) != 0:
            for y in a0tags:
                b = y.find_all('span')
                for k in b:
                    if k.get('itemprop') == 'relatedTo':
                        prev_l = k
                        print('previousL:', prev_l)
                        found = True
                        break
                if found:
                    break
            if found:
                break

    print('===========================================================')

    i = -1
    for item in useful:
        atags = item.find_all('a')
        if len(atags) == 0:
            # deal with email related stuff here
            if re.search('[a-zA-Z].*\@.*\.[a-zA-Z]', item.text):
                usr.emails.append(re.search('[a-zA-Z].*\@.*\..*[a-zA-Z]', item.text).group())
                print('@@@@'+item.text)
            elif re.search('Age', item.text):
                astring = re.search('Age', item.text).group()
                print('AGE::::' + astring)
        else:
            for x in atags:
                a = x.find_all('span')

                # parse through info line by line.
                for l in a:
                    if l.get('itemprop') == 'streetAddress':
                        if prev_l.get('itemprop') == 'relatedTo':
                            print('New Set Of Info.......', i)
                            i = i + 1
                            addr = userInfo.userAddr()
                            addr.street = l.text
                            print(json.dumps(addr.__dict__))
                        elif prev_l.get('itemprop') == 'postalCode':
                            print('same person, different address')
                            addr = userInfo.userAddr()
                            addr.street = l.text
                            print(json.dumps(addr.__dict__))
                        # else:
                        #     print('PREVIOUS L is:', prev_l)
                    elif l.get('itemprop') == 'addressLocality':
                        addr.city = l.text
                        print(json.dumps(addr.__dict__))
                    elif l.get('itemprop') == 'addressRegion':
                        addr.state = l.text
                        print(json.dumps(addr.__dict__))
                    elif l.get('itemprop') == 'postalCode':
                        addr.zip = l.text
                        print(json.dumps(addr.__dict__))
                        users[i].addresses.append(addr)
                    elif l.get('itemprop') == 'telephone':
                        users[i].phones.append(l.text)

                    prev_l = l

    # for u in users:
    #     log_1('vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv')
    #     log_1(u.asDict())
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
        days = 31
    elif month == 2:
        days = 28
        if isleap(year):
            print('leap year')
            days = 29
    elif month == 3:
        days = 31
    elif month == 4:
        days = 30
    elif month == 5:
        days = 31
    elif month == 6:
        days = 30
    elif month == 7:
        days = 31
    elif month == 8:
        days = 31
    elif month == 9:
        days = 30
    elif month == 10:
        days = 31
    elif month == 11:
        days = 30
    elif month == 12:
        days = 31
    else:
        log_1('Error: Invalid Month')
    return days



