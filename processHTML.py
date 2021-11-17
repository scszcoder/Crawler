
# this functions processes an html file.
import bs4
from bs4 import BeautifulSoup

from logger import *
import numpy
from readScreen import subfinder
import re
import random
from calendar import isleap
import shutil
import json
import time


class userInfo:
    def __init__(self):
        self.firstName = ""
        self.lastName = ""
        self.middleName = ""
        self.suffix = ""
        self.birthday = ""
        self.emails = []
        self.phones = []
        self.addrs = []

    def asDict(self):
        dict = self.__dict__
        dict["addrs"] = [child.__dict__ for child in dict["addrs"]]
        return dict

    def genPrintable(self):
        clsstring = "{ firstName: \"" + self.firstName + "\", "
        clsstring = clsstring + "lastName: \"" + self.lastName + "\", "
        clsstring = clsstring + "middleName: \"" + self.middleName + "\", "
        clsstring = clsstring + "suffix: \"" + self.suffix + "\", "
        clsstring = clsstring + "birthday: \"" + self.birthday + "\", "
        clsstring = clsstring + "emails: " + self.genEmailsString() + ", "
        clsstring = clsstring + "phones: " + self.genPhoneString() + ", "
        clsstring = clsstring + "addrs: " + self.genAddrsString() + " }"
        return clsstring

    def genEmailsString(self):
        emstring = "["
        if len(self.emails) > 0:
            for i in range(len(self.emails)):
                emstring = emstring + "\"" + self.emails[i] + "\""
                if i != len(self.emails) - 1:
                    emstring = emstring + ", "
        else:
            emstring = emstring + "\"e@n\""
        emstring = emstring + "]"
        return emstring

    def genPhoneString(self):
        phstring = "["
        if len(self.phones) > 0:
            for i in range(len(self.phones)):
                phstring = phstring + "\"" + self.phones[i] + "\""
                if i != len(self.phones) - 1:
                    phstring = phstring + ", "
        else:
            phstring = phstring + "\"(510) 888-8888\""
        phstring = phstring + "]"
        return phstring

    def genAddrsString(self):
        adstring = "["
        if len(self.addrs) > 0:
            for i in range(len(self.addrs)):
                adstring = adstring + self.addrs[i].genPrintable()
                if i != len(self.addrs) - 1:
                    adstring = adstring + ", "

        adstring = adstring + "]"
        return adstring

    class userAddr:
        def __init__(self):
            self.street1 = ""
            self.street2 = ""
            self.city = ""
            self.state = ""
            self.zip = ""
            self.startDate = ""  # reside date
            self.endDate = ""

        def genPrintable(self):
            prnter = "{ street1: \"" + self.street1 + "\", "
            prnter = prnter + "street2: \"" + self.street2 + "\", "
            prnter = prnter + "city: \"" + self.city + "\", "
            prnter = prnter + "state: \"" + self.state + "\", "
            prnter = prnter + "zip: \"" + self.zip + "\", "
            prnter = prnter + "startDate: \"" + self.startDate + "\", "
            prnter = prnter + "endDate: \"" + self.endDate + "\"} "
            return prnter

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
    log_1('number of pages: ' + str(num_pages))
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

    last_names_i = [i for i, ln in enumerate(n) if i > start_idx and i < end_idx ]
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
    time.sleep(5)
    with open(html_file, encoding="utf8") as fp:
        soup = BeautifulSoup(fp, 'html.parser')
    # all useful information are here:
    useful = soup.findAll('div', {"class": lambda t: t in ('content-label h5', 'content-value')})
    ageuseful = soup.findAll('span', {"class": 'content-value'})
    nameuseful = soup.findAll('span', {"class": 'h4'})
    moredetails = soup.findAll('div', {"class": "card card-body shadow-form pt-3"})

    print(ageuseful)
    print('**********************************************************')
    print(nameuseful)

    # createa N users according to number of age information found in the html file.
    for i in range(len(ageuseful)):
        usr = userInfo()
        agewords = ageuseful[i].text.split(' ')
        print(agewords)
        if len(agewords) > 4:
            if 'Age' in agewords[0]:
                if agewords[1] == '':
                    birth_year = int(agewords[4][0:4])
                    birth_month = get_birth_month(agewords[3][1:4])
                else:
                    birth_year = int(agewords[3][0:4])
                    birth_month = get_birth_month(agewords[2][1:4])
            elif 'Death' in agewords[0]:
                age = int(agewords[4][0:len(agewords[4])-1])
                death_year = int(agewords[3][0:4])
                death_month = get_birth_month(agewords[2][0:3])
                birth_year = death_year - age
                birth_month = death_month
            # print('Year, Month ', birth_year, ' ', birth_month)
        elif agewords[1] == 'Unknown':
            # in case of unknown age, just randeomly generate one.
            birth_year = 2021 - random.randrange(20, 80)
            birth_month = random.randrange(1, 13)
        # day is randomly generated anyways.
        days = get_month_days(birth_year, birth_month)
        birth_day = random.randrange(1, days + 1)
        usr.birthday = str(birth_year)+'-'+str(birth_month).zfill(2)+'-'+str(birth_day).zfill(2)
        print(usr.birthday)

        # now obtain the name information
        stags = nameuseful[i].find_all('span')
        for stag in stags:
            if stag.get('itemprop') == 'givenName':
                usr.firstName = stag.text
            elif stag.get('itemprop') == 'familyName':
                    usr.lastName = stag.text
        nfields = nameuseful[i].text.split(' ')
        fidx = [i for i, f in enumerate(nfields) if usr.firstName in f][0]
        lidx = [i for i, f in enumerate(nfields) if usr.lastName in f][0]
        if lidx != len(nfields) -1:
            usr.suffix = nfields[len(nfields) - 1].strip()

        # now obtain more detail information,
        print(moredetails[i].get('itemid'))
        # now add the user into the list/record.
        users.append(usr)

    # set up prev_l for later processing.
    # print(useful)
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
                            # print('New Set Of Info.......', i)
                            i = i + 1
                            addr = userInfo.userAddr()
                            addr.street1 = l.text
                            # print(json.dumps(addr.__dict__))
                        elif prev_l.get('itemprop') == 'postalCode':
                            # #print('same person, different address')
                            addr = userInfo.userAddr()
                            addr.street1 = l.text
                            # print(json.dumps(addr.__dict__))
                        # else:
                        #     print('PREVIOUS L is:', prev_l)
                    elif l.get('itemprop') == 'addressLocality':
                        addr.city = l.text
                        # print(json.dumps(addr.__dict__))
                    elif l.get('itemprop') == 'addressRegion':
                        addr.state = l.text
                        # print(json.dumps(addr.__dict__))
                    elif l.get('itemprop') == 'postalCode':
                        addr.zip = l.text
                        # print(json.dumps(addr.__dict__))
                        users[i].addrs.append(addr)
                    elif l.get('itemprop') == 'telephone':
                        users[i].phones.append(l.text)

                    prev_l = l

    # for u in users:
    #     log_1('vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv')
    #     log_1(u.asDict())
    print('collected: ' +  str(len(users)) + 'USERS...')
    return users


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



def get_malefemale_first_names(html_file):
    mffnames = []
    name_starts = False
    time.sleep(5)
    with open(html_file, encoding="utf8") as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    #for elem in soup(text=re.compile("next page")):
    # elems = soup.find_all(text=re.compile("next page"))
    # print(elems)
    # print('hello.......')
    # for elem in elems:
    #     print(soup.findParent(elem))
    #     # print(elem.sourceline)
    #     print("-------------")

    # all useful information are here:
    li_tags = soup.find_all('li')
    div_tags = soup.find_all('div', attrs={'id' : 'mw-pages'})
    a_tags = soup.find_all('a')

    # print('========================================================')
    c0 = 0
    for item in div_tags:
        # inner_text = [element for element in item if isinstance(element, bs4.element.NavigableString)]
        # eles = [string for string in inner_text if 'next page' in string]
        inner_atags = item.find_all('a')
        for atag in inner_atags:
            inner_atext = [ele for ele in atag if isinstance(ele, bs4.element.NavigableString)]
            # print(inner_atext)
            # print(len(inner_atext))
            pps = [string for string in inner_atext if 'previous page' in string]
            # print(atag.sourceline)
            # print(pps)
            # print(len(pps))
            if len(pps) > 0:
                c0 = c0 + 1
                # print('hohoho000000000000000000000000000000000000000000000000000000')
                # print(item)
                # print(atag.sourceline)
                if c0 == 1:
                    start_line = atag.sourceline
                elif c0 == 2:
                    end_line = atag.sourceline
                # print(pps)
            # print('>>>>>>>>>>>>>>>>>>>>>')
        # print(inner_text)
    print('Start line:', start_line)
    print('End line:', end_line)

    for item in li_tags:
        id_tags = item.find_all('id')
        style_tags = item.find_all('style')
        if len(id_tags) == 0 and len(style_tags) == 0 and not item.has_attr('id') and not item.has_attr('style'):
            # print(item.sourceline)
            if item.sourceline > start_line and item.sourceline <= end_line:
                mffnames.append((item.text.split())[0])
                # mffnames.pop()




        # if len(eles) > 0:
        #     print(inner_text)
        #     print(item.sourceline)
        #     print(soup.find(item))
        #     print('<=========================>>', c1, ' ', c2)


    # print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    # for item in a_tags:
    #     if item.text == 'next page' and item.has_attr('href'):
    #         next_link = item.get('href')

    return mffnames




