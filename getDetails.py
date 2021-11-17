# this functions gets all first names associated with a last name.

from logger import *
from processHTML import *
from uiAction import *
from csv import reader
import shutil
from sendCloud import *

MIN_BATCH_SIZE = 4   # 128 record pelastname00.html batch


# find the next last name to scrape, go through the last name files.
# go through the file names to find which file should contain the last name.
# go to that file, find the next last name.
# needs to take care of the special case of the last name supplied is the last file .
#
def find_next_file(file_name):
    next_file_name = 'None'
    # names_path = 'C:/CrawlerData/names/'

    file_words = file_name.split('/')
    print(file_words)
    names_path = "/".join(list[0:(len(file_words)-1)])
    print(names_path)
    file_name_only = file_words[len(file_words)-1]
    print(file_name_only)
    nfiles = os.listdir(names_path)
    print(nfiles)

    f_index = nfiles.index(file_name_only)
    print(f_index)

    if f_index != len(nfiles)-1:
        next_file_name = nfiles[f_index+1]
    else:
        next_file_name = 'END'

    print(' the next last name file nameis: ' + (names_path + '/' + next_file_name))
    return (names_path + '/' + next_file_name)


# this function get the next last name and the full name index page to be scraped..
# from last file name and the last line of the last file.
# input:
#        last last name and the last completed full name page index
# output: next last name and page index of the next to-be-scraped page.
def get_next_tbs_full_name(last_full):
    # open the web site, with last name and the designated full name index page.
    next_last = ['Aaberg', 'Catherine', 'C:/CrawlerData/names/fn_aaberg_aaron_2_7_.csv']
    found_index = False

    if last_full[0] != 'None':
        # open the file.
        with open(last_full[2], 'r') as read_obj:
            # pass the file object to reader() to get the reader object
            csv_reader = reader(read_obj)
            names = [fnwords[0] for fnwords in list(csv_reader)]
            first_indices = [i for i, x in enumerate(names) if x == last_full[1]]
            last_indices = [i for i, x in enumerate(names) if x == last_full[0].lower()]
            num_indices = [i for i, x in enumerate(names) if x.isnumeric()]

            print(names)
            print(first_indices)
            print(last_indices)
            print(num_indices)

            # now search for the correct first and last name index
            # match criteria: the matching index of first name and the last name have no number indices in between
            for li in last_indices:
                for fi in first_indices:
                    if fi < li:
                        nis = [ix for ix in num_indices if fi < ix < li]
                        if len(nis) == 0:
                            # we found it.
                            fn_index = fi
                            ln_index = li
                            found_index = True
                            break
                if found_index:
                    break

            if ln_index == fn_index + 1 and ln_index == len(names) - 3:
                # we're already at the last name of the file, need to go to the next file.
                next_last[2] = find_next_file(last_full[2])
                with open(next_last[2], 'r') as next_read_obj:
                    # pass the file object to reader() to get the reader object
                    next_csv_reader = reader(next_read_obj)
                    next_names = [nxfnwords[0] for nxfnwords in list(next_csv_reader)]
                    ns = [i for i, x in enumerate(next_names) if x.isnumeric()]
                    # print(numbers)
                    next_last[1] = next_names[0]
                    next_last[0] = next_names[ns[0]-1]
                next_read_obj.close()
            elif ln_index == fn_index + 1:
                # if the last full name of a page, but not yet at the end of the file, go the next section.
                next_ln_indices = [x for x in num_indices if x > ln_index+2]
                # print('next fn indices---->')
                # print(next_ln_indices)

                next_fn_index = next_ln_indices[0] - 1
                next_last[0] = names[next_fn_index]
                next_last[1] = names[fn_index+4]
                next_last[2] = last_full[2]
            else:
                # if not yet the last full name of a page, simply go to the next first name.
                next_last[0] = last_full[0]
                next_last[1] = names[fn_index+1]
                next_last[2] = last_full[2]
        read_obj.close()
    return next_last

# this function opens a designated last name page, and scrapes all last names on that page.
# and append the names to the last name array.
# input: last_last (last
#          last_names: array of already collected last names for this batch
#                      (each batch has at least 8192 entries)
#        sid - scraper ID
# output: scrape status (SUCCESS/FAILURE), if successfull, the last_names array will be expanded.
def scrape_one_page_of_details(win_loc, last, first, recs, sid='00'):
    # open the web site, with initials and numpages.
    stat = 'SUCCESS'

    url = 'https://www.truepeoplesearch.com/find/' + last + '/' + first
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
    name_recs = get_details_info(full_temp_page)
    # cleanup after procesing...
    print('trying to remove: ' + temp_page_dir)
    shutil.rmtree(temp_page_dir)
    os.remove(full_temp_page)
    log_1(url)
    if len(name_recs) > 0:
        recs.extend(name_recs)
        print('Added records:' + str(len(name_recs)))
    else:
        stat = 'FAILED'
    # now return the results.
    return stat


# save last scraped name to the record file: first name, last name, and the full name file name.
# the record file name is: srec_bid_.csv (bid is the bot ID)
def save_details_to_cloud(recs, last, first, file_name, session, bid = '000'):
    # print(recs)
    # send recs to the cloud.
    send_ppl_info_to_cloud(session, recs)

    # after successfully sending infor to the cloud to store, update the scrape record.
    fname = 'C:/CrawlerData/names/srec_' + bid + '_.csv'
    rec_word = last + ', ' + first + ', ' + file_name
    with open(fname, 'w') as file_handler:
        file_handler.write("{}\n".format(rec_word))
    file_handler.close()


# this function checks whether we have obtained all names.
# checks the scrape record srec_bid_.csv file.
# bid is the bot ID.
# input: none
# output: whether all names have been obtained.
def obtained_all_details():
    gotAll = False
    names_path = 'C:/CrawlerData/names/'
    nfiles = os.listdir(names_path)
    nfiles = list(filter(lambda f: f.endswith('.csv'), nfiles))
    nfiles = list(filter(lambda f: f.startswith('srec_'), nfiles))

    # check whether the bot record file exists, and if so, open the file and dig out, the last name and first name,
    # if we have already reached 'William Zick' , then  we are done.
    # parse file name
    if len(nfiles) > 0:
        for fname in nfiles:
            with open((names_path + fname), 'r') as read_obj:
                csv_reader = reader(read_obj)
                lines = list(csv_reader)
                names = lines[0]
                # # print(names)
                last = names[0].strip()
                first = names[1].strip()

                if first == 'Zick' and last == 'William':
                    gotAll = True
            read_obj.close()
            if gotAll:
                break
    return gotAll



# this function return a 2-tuple of last name and index number where we can find the page that contains the name.
# for example,
def get_last_full_name_details(bid = '000'):
    last_full = ['None', 'None', 'None']  #last, first, file_name
    names_path = 'C:/CrawlerData/names/'
    nfiles = os.listdir(names_path)
    nfiles = list(filter(lambda f: f.endswith('_.csv'), nfiles))
    nfiles = list(filter(lambda f: f.startswith('srec_'), nfiles))

    # parse file name
    if len(nfiles) > 0:
        fname = names_path+'srec_' + bid + '_.csv'
        with open(fname, 'r') as read_obj:
            # pass the file object to reader() to get the reader object
            csv_reader = reader(read_obj)
            fullnames = list(csv_reader)[0]
            print(fullnames)
            # Iterate over each row in the csv using reader object
            last_full[0] = fullnames[0].strip()
            last_full[1] = fullnames[1].strip()
            last_full[2] = fullnames[2].strip()

    return last_full


# scrape a batch of full names.
# a batch will contain multiple pages of full names. (no less than 8092, unless its the last page)
def scrape_batch_of_details(win_loc, cloud_session):
    stat = 'SUCCESS'
    batch_count = 0
    PersonRec = []
    # open the last file, read the last line, to obtain the last name and first name to continue.
    # finish the current page, update counter, goes to the next page, update names, and num of names,
    # repeat above until complete 8192 names. eventaully, all name will be save.d
    last_full = get_last_full_name_details()
    while len(PersonRec) < MIN_BATCH_SIZE:
        print('last full----->')
        print(last_full)
        next_last = get_next_tbs_full_name(last_full)
        print('next full----->')
        print(next_last)
        scrape_one_page_of_details(win_loc, next_last[0], next_last[1], PersonRec)
        last_full = next_last
        print('Collected ' + str(len(PersonRec)) + ' records so far!!!')

    save_details_to_cloud(PersonRec, last_full[0], last_full[1], last_full[2], cloud_session)
    return stat


# scrape a batch of last names.
# a batch will contain multiple pages of last names.
# first scrape all last names.
# last names will be organized into last name csv files, file names will be in the format of:
# EndingLastName_StaringLastName_.csv, each file contains 8192 last names.
def scrape_details(win_loc, session):
    stat = 'SUCCESS'
    batch_count = 0
    while not obtained_all_details():
        log_1('scrape a batch...'+str(batch_count))
        stat = scrape_batch_of_details(win_loc, session)
        batch_count = batch_count + 1
        if stat == 'FAILURE':
            log_1('scrape failure')
            break
        if batch_count > 1:
            break
    return stat
