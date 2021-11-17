
from logger import *
from processHTML import *
from uiAction import *
from csv import reader
import shutil

# total of
page_index = {'a': 35, 'b': 64, 'c': 56, 'd': 45, 'e': 18, 'f': 27, 'g': 38, 'h': 43, 'i': 7,
              'j': 11, 'k': 35, 'l': 42, 'm': 70, 'n': 16, 'o': 17, 'p': 37, 'q': 3, 'r': 37,
              's': 77, 't': 28, 'u': 5, 'v': 19, 'w': 26, 'x': 1, 'y': 5, 'z': 8}

MIN_BATCH_SIZE = 256


# this function get the next inital and index page to be scraped..
# and append the names to the last name array.
# input: last_last in the format [last_initial, last_index]
# output: scrape status (SUCCESS/FAILURE), if successfull, the last_names array will be expanded.
def get_next_tbs_page_index(last_last):
    # open the web site, with initials and numpages.
    next_last = ['0', '0']
    if last_last[0] == '0':
        # this means we're just starting.
        print("First Round")
        next_last = ['a', '1']
    else:
        print("initial: " + last_last[0][0])
        print("page index: " + str(page_index[last_last[0][0]]))
        print("last last1: " + str(int(last_last[1])))
        if page_index[last_last[0][0]] == int(last_last[1]):
            # this is the last index page of a last name initial, go to the next last name initial letter
            next_last[0] = chr(ord(last_last[0]) + 1)
            next_last[1] = '1'
        else:
            # if not yet reached the last index page of a last name initial, just go to the next index page.
            next_last[0] = last_last[0]
            next_last[1] = str(int(last_last[1])+1)
    log_1(next_last)
    return next_last

# this function opens a designated last name page, and scrapes all last names on that page.
# and append the names to the last name array.
# input: last_last (last
#          last_names: array of already collected last names for this batch
#                      (each batch has at least 8192 entries)
#        sid - scraper ID
# output: scrape status (SUCCESS/FAILURE), if successfull, the last_names array will be expanded.
def scrape_one_page_of_last_names(win_loc, initial, index, last_names, sid='00'):
    # open the web site, with initials and numpages.
    stat = 'SUCCESS'

    url = 'https://www.truepeoplesearch.com/find/' + initial + '/' + index + ' '
    html_name = 'lastname' + sid
    path_name = 'C:/CrawlerData/pages/'
    temp_page = html_name + '.html'
    full_temp_page = path_name + html_name + '.html'
    temp_page_dir = path_name + html_name + '_files'

    #first, delete the existing html file and its associated directory.
    if os.path.isfile(full_temp_page):
        os.remove(full_temp_page)
    if os.path.isdir(temp_page_dir):
        shutil.rmtree(temp_page_dir)
    open_url_then_save_page(win_loc, url, path_name, temp_page)
    lns = get_last_names(full_temp_page)
    # cleanup after procesing...
    shutil.rmtree(temp_page_dir)
    os.remove(full_temp_page)
    log_1(url)
    if len(lns) > 0:
        last_names.extend(lns)
        last_names.append(index)
    else:
        stat = 'FAILED'
    # now return the results.
    return stat


# save a list of last names
def save_last_names_to_file(lns):
    fname = 'C:/CrawlerData/names/ln_' + lns[len(lns)-2] + '_' + lns[len(lns)-1] + '_' + lns[0] + '_.csv'
    with open(fname, 'a') as file_handler:
        for item in lns:
            file_handler.write("{}\n".format(item))
    file_handler.close()


# scrape a batch of last names.
# a batch will contain multiple pages of last names.
def scrape_batch_of_last_names(win_loc):
    stat = 'SUCCESS'
    batch_count = 0
    nameRec = []
    # open the last file, read the last line, to obtain the last name and first name to continue.
    # finish the current page, update counter, goes to the next page, update names, and num of names,
    # repeat above until complete 8192 names. eventaully, all name will be save.d
    last_last = get_last_last_name()
    while len(nameRec) < MIN_BATCH_SIZE:
        log_1('Current Batch Size: ' + str(len(nameRec)))

        log_1("Last scraped last name: ", last_last)
        next_last = get_next_tbs_page_index(last_last)
        log_1("Next to be scraped last name: "+next_last[0]+" AND "+next_last[1])
        scrape_one_page_of_last_names(win_loc, next_last[0], next_last[1], nameRec)
        if nameRec[len(nameRec)-1] == 'Zick':
            # stop, after fetching the last last name.
            break
        else:
            last_last = next_last

    save_last_names_to_file(nameRec)
    return stat


def obtained_all_last_names():
    gotAll = False
    names_path = 'C:/CrawlerData/names'
    nfiles = os.listdir(names_path)
    nfiles = list(filter(lambda f: f.endswith('.csv'), nfiles))
    nfiles = list(filter(lambda f: f.startswith('ln_'), nfiles))

    # parse file name
    if len(nfiles) > 0:
        names = nfiles[len(nfiles)-1].split('_')
        if len(names) == 4 and names[1] == 'Zick' and names[2] == 'William':
            gotAll = True
    else:
        log_1('Not even started yet...')
    return gotAll


# this function return a 2-tuple of last name and index number where we can find the page that contains the name.
# for example,
def get_last_last_name():
    last_last = ['0', '0']
    names_path = 'C:/CrawlerData/names/'
    nfiles = os.listdir(names_path)
    nfiles = list(filter(lambda f: f.endswith('.csv'), nfiles))
    nfiles = list(filter(lambda f: f.startswith('ln_'), nfiles))

    # parse file name
    if len(nfiles) > 0:
        fname = nfiles[len(nfiles)-1]
        with open((names_path+fname), 'r') as read_obj:
            # pass the file object to reader() to get the reader object
            csv_reader = reader(read_obj)
            names = list(csv_reader)
            # Iterate over each row in the csv using reader object
            # the last item will be a page index number, the 2nd to the last item will be just completed last name.
            last_last = [names[len(names)-2][0][0].lower(), names[len(names)-1][0]]
            # print(last_last)
            # actually we return something like this: [['Ackroyd'], ['3']]
            # CSV reader will automatically put line fields into list.

    return last_last


# scrape a batch of last names.
# a batch will contain multiple pages of last names.
# first scrape all last names.
# last names will be organized into last name csv files, file names will be in the format of:
# EndingLastName_StaringLastName_.csv, each file contains 8192 last names.
def scrape_last_names(win_loc):
    stat = 'SUCCESS'
    batch_count = 0
    while not obtained_all_last_names():
        log_1('scrape a batch...')
        stat = scrape_batch_of_last_names(win_loc)
        batch_count = batch_count + 1
        print('BATCH count: ' + str(batch_count))
        if stat == 'FAILURE':
            log_1('scrape failure')
            break
        if batch_count > 2:
            break
    return stat

