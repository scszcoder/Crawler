# this functions gets all first names associated with a last name.

from logger import *
from processHTML import *
from uiAction import *
from csv import reader
import shutil

MIN_BATCH_SIZE = 256


# find the next last name to scrape, go through the last name files.
# go through the file names to find which file should contain the last name.
# go to that file, find the next last name.
# needs to take care of the special case of the last name supplied is the last file .
#
def find_next_last_name(ln):
    next_ln = 'None'
    names_path = 'C:/CrawlerData/names/'
    nfiles = os.listdir(names_path)
    nfiles = list(filter(lambda f: f.endswith('.csv'), nfiles))
    nfiles = list(filter(lambda f: f.startswith('ln_'), nfiles))

    # parse file name
    print('last name files:')
    print(nfiles)
    if len(nfiles) > 0:
        i = 0
        for ln_file in nfiles:
            # go thru all last names files and find the one that contains the provided last anem.
            names = ln_file.split('_')
            print(names)
            if ln < names[1].lower():
                # if the provided last name is smaller than the ending last name of a file, then the last name should
                # be in this file., so go in and search.
                with open((names_path+ln_file), 'r') as read_obj:
                    # pass the file object to reader() to get the reader object
                    csv_reader = reader(read_obj)
                    names = [fnwords[0] for fnwords in list(csv_reader)]
                    print(names)
                    # Iterate over each row in the csv using reader object
                    index = names.index(ln.capitalize())
                    if names[index+1].isalpha():
                        next_ln = names[index+1]
                    else:
                        # in case of hitting a page index number, skip to the next line.
                        next_ln = names[index + 2]

                # got what's needed, close the file and break out of the loop.
                read_obj.close()
                break
            elif ln == names[1].lower():
                # in case the provided last name is the ending last name of a last name file, go to the next file,
                # and the very first last name in that file is the next to be search last name.
                # if the provided last name is the last name of all last name, then return 'None'.
                if i < len(nfiles) - 1:
                    next_fname = nfiles[i+1]
                    with open((names_path+next_fname), 'r') as read_obj:
                        # pass the file object to reader() to get the reader object
                        csv_reader = reader(read_obj)
                        names = list(csv_reader)
                        next_ln = names[0][0]
                    # got what's needed, close the file and break out of the loop
                    read_obj.close()
                else:
                    print('first name scraped to all of the last name')
                break
            else:
                i = i + 1
    print(' the next last name is: ' + next_ln)
    return next_ln


# this function get the next last name and the full name index page to be scraped..
# from last file name and the last line of the last file.
# input:
#        last last name and the last completed full name page index
# output: next last name and page index of the next to-be-scraped page.
def get_next_tbs_fn_page_index(last_full):
    # open the web site, with last name and the designated full name index page.
    next_last = ['aaberg', '1', '1']

    if last_full[0] != '0':
        if last_full[2] == last_full[1]:
            # if the last full name page index index is the last index of this last name, then go to
            # the 1st index page of the next last name.
            next_last[0] = find_next_last_name(last_full[0]).lower()
            next_last[1] = '1'
            next_last[2] = '0'  # 0 here means number of pages unknown at the moment

        else:
            # if the last full name page index index is not yet the last index of this last name, then go to
            # the next index page of the same last name.
            next_last[0] = last_full[0]
            next_last[1] = str(int(last_full[1])+1)
            next_last[2] = last_full[2]
    return next_last

# this function opens a designated last name page, and scrapes all last names on that page.
# and append the names to the last name array.
# input: last_last (last
#          last_names: array of already collected last names for this batch
#                      (each batch has at least 8192 entries)
#        sid - scraper ID
# output: scrape status (SUCCESS/FAILURE), if successfull, the last_names array will be expanded.
def scrape_one_page_of_full_names(win_loc, last, index, full_names, sid='00'):
    # open the web site, with initials and numpages.
    stat = 'SUCCESS'

    url = 'https://www.truepeoplesearch.com/find/' + last + '/' + index
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
    fns = get_first_names(full_temp_page)
    n_pages = get_first_name_pages(full_temp_page)
    # cleanup after procesing...
    shutil.rmtree(temp_page_dir)
    os.remove(full_temp_page)
    log_1(url)
    if len(fns) > 0:
        first = [fn.split(' ')[0] for fn in fns]
        print('first names')
        print(first)
        print(last)
        full_names.extend(first)  #record the first names only
        full_names.append(last)  # record the last name.
        full_names.append(index)  # append index page of the last name.
        full_names.append(str(n_pages))  # append # pages of the last name.
    else:
        stat = 'FAILED'
    # now return the results.
    return stat


# save a list of last names
def save_full_names_to_file(fns):
    # print(fns)
    numbers = [ele for ele in fns if ele.isnumeric()]
    # print(numbers)
    n0 = int(numbers[0])
    # print(n0)
    ixs = fns.index(numbers[0])
    start_last = fns[ixs-1]
    print(start_last)
    fname = 'C:/CrawlerData/names/fn_' + start_last + '_' + fns[len(fns)-3] + '_' + fns[len(fns)-2] + '_' + fns[len(fns)-1] + '_.csv'
    with open(fname, 'w') as file_handler:
        for item in fns:
            file_handler.write("{}\n".format(item))
    file_handler.close()


# this function checks whether we have obtained all names.
# obtain all csv files, sort alphabatically, and check the last one.
# input: none
# output: whether all names have been obtained.
def obtained_all_full_names():
    gotAll = False
    names_path = 'C:/CrawlerData/names'
    nfiles = os.listdir(names_path)
    nfiles = list(filter(lambda f: f.endswith('.csv'), nfiles))
    nfiles = list(filter(lambda f: f.startswith('fn_'), nfiles))

    # parse file name
    if len(nfiles) > 0:
        names = nfiles[len(nfiles)-1].split('_')
        if len(names) == 6 and names[1] == 'Zick' and names[2] == 'William':
            gotAll = True
    return gotAll



# this function return a 2-tuple of last name and index number where we can find the page that contains the name.
# for example,
def get_last_full_name():
    last_full = ['0', '0', '0']
    names_path = 'C:/CrawlerData/names/'
    nfiles = os.listdir(names_path)
    nfiles = list(filter(lambda f: f.endswith('.csv'), nfiles))
    nfiles = list(filter(lambda f: f.startswith('fn_'), nfiles))

    # parse file name
    if len(nfiles) > 0:
        fname = names_path+nfiles[len(nfiles)-1]
        with open(fname, 'r') as read_obj:
            # pass the file object to reader() to get the reader object
            csv_reader = reader(read_obj)
            fullnames = list(csv_reader)
            # Iterate over each row in the csv using reader object
            last_full[0] = fullnames[len(fullnames) - 3][0]
            last_full[1] = fullnames[len(fullnames) - 2][0]
            last_full[2] = fullnames[len(fullnames) - 1][0]

    return last_full


# scrape a batch of full names.
# a batch will contain multiple pages of full names. (no less than 8092, unless its the last page)
def scrape_batch_of_full_names(win_loc):
    stat = 'SUCCESS'
    batch_count = 0
    fullnameRec = []
    # open the last file, read the last line, to obtain the last name and first name to continue.
    # finish the current page, update counter, goes to the next page, update names, and num of names,
    # repeat above until complete 8192 names. eventaully, all name will be save.d
    last_full = get_last_full_name()
    while len(fullnameRec) < MIN_BATCH_SIZE:
        print(last_full)
        next_last = get_next_tbs_fn_page_index(last_full)
        print(next_last)
        scrape_one_page_of_full_names(win_loc, next_last[0], next_last[1], fullnameRec)
        last_full = next_last
        # update the total number of pages under this last name.
        last_full[2] = fullnameRec[len(fullnameRec)-1]

    save_full_names_to_file(fullnameRec)
    return stat


# scrape a batch of last names.
# a batch will contain multiple pages of last names.
# first scrape all last names.
# last names will be organized into last name csv files, file names will be in the format of:
# EndingLastName_StaringLastName_.csv, each file contains 8192 last names.
def scrape_full_names(win_loc):
    stat = 'SUCCESS'
    batch_count = 0
    while not obtained_all_full_names():
        log_1('scrape a batch...'+str(batch_count))
        stat = scrape_batch_of_full_names(win_loc)
        batch_count = batch_count + 1
        if stat == 'FAILURE':
            log_1('scrape failure')
            break
        if batch_count > 2:
            break
    return stat
