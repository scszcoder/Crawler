
from logger import *
from processHTML import *
from uiAction import *
from csv import reader
import shutil
from sendCloud import *

cults = ['English', 'Spanish', 'Italian', 'Portuguese', 'German', 'French', 'Russian', 'Polish', 'Dutch', 'Greek', 'Ukrainian', 'Romanian', 'Slovak', 'Finnish', 'Indian', 'Hebrew', 'Iranian', 'Turkish', 'Arabic', 'African']
MIN_BATCH_SIZE = 128

# The strategy is as the following:
# the starting point is the following page:
# https://en.wikipedia.org/wiki/Category:Given_names_by_culture
# from here, go into Africa, Asia, European, Jewish Given Names, Arabic Given Names, Iranian, Egyptian, Turkish

def getNextCulture(this_cult):
    next_cult = 'None'
    index = cults.index(this_cult)
    if index < len(cults) - 1:
        next_cult = cults[index+1]
    return next_cult


# this function get the next inital of the first name page to be scraped..
# and append the names to the last name array.
# input: last_last in the format [last_fn_initial, last_culture]
# last_culture is in the format of "culture_country"
# output: scrape status (SUCCESS/FAILURE), if successfull, the last_names array will be expanded.
def get_next_tbs_page_index(last_first):
    # open the web site, with initials and numpages.
    next_last = ['0', '0']
    if last_first[0] == '0':
        # this means we're just starting.
        print("First Round")
        next_last = ['A', 'English']
    else:
        print("last first : " + last_first[0])
        print("last cult: " + last_first[1])
        if last_first[0][0] == 'Z':
            # this is the last page of a culture, go to the next culture
            next_last[0] = 'A'
            next_last[1] = getNextCulture(last_first[1])
        else:
            # if not yet reached the last index page of a last name initial, just go to the next index page.
            next_last[0] = last_first[0][0]
            next_last[1] = last_first[1]
    log_1(next_last)
    return next_last

# this function opens a designated last name page, and scrapes all last names on that page.
# and append the names to the last name array.
# input: last_last (last
#          last_names: array of already collected last names for this batch
#                      (each batch has at least 8192 entries)
#        sid - scraper ID
# output: scrape status (SUCCESS/FAILURE), if successfull, the last_names array will be expanded.
def scrape_one_page_of_first_names(win_loc, mf, fn, cult, fnames, sid='00'):
    # open the web site, with initials and numpages.
    stat = 'SUCCESS'

    if mf == 'Male':
        url = 'https://en.wikipedia.org/w/index.php?title=Category:' + cult + '_masculine_given_names&from=' + fn[0]
    else:
        url = 'https://en.wikipedia.org/w/index.php?title=Category:' + cult + '_feminine_given_names&from=' + fn[0]
    html_name = 'mffirstname' + sid
    path_name = 'C:/CrawlerData/pages/'
    temp_page = html_name + '.html'
    full_temp_page = path_name + html_name + '.html'
    temp_page_dir = path_name + html_name + '_files'

    #first, delete the existing html file and its associated directory.
    if os.path.isfile(full_temp_page):
        os.remove(full_temp_page)
    if os.path.isdir(temp_page_dir):
        shutil.rmtree(temp_page_dir)
    print(full_temp_page)
    open_url_then_save_page(win_loc, url, path_name, temp_page)
    mffns = get_malefemale_first_names(full_temp_page)
    # cleanup after procesing...
    shutil.rmtree(temp_page_dir)
    os.remove(full_temp_page)
    log_1(url)
    if len(mffns) > 0:
        fnames.extend(mffns)
    else:
        stat = 'FAILED'
    # now return the results.
    return stat


# save a list of last names
def save_mf_first_names_to_file(mffns, mf, cult):
    if mf == 'Male':
        fname = 'C:/CrawlerData/names/male_fn_' + mffns[0][0] + '_' + mffns[len(mffns)-1][0] + '_' + cult + '_.csv'
    else:
        fname = 'C:/CrawlerData/names/female_fn_' + mffns[0][0] + '_' + mffns[len(mffns)-1][0] + '_' + cult + '_.csv'
    with open(fname, 'a') as file_handler:
        for item in mffns:
            # file_handler.write("{}\n".format(item.encode("utf-8")))
            file_handler.write("{}\n".format(item))
    file_handler.close()


# scrape a batch of last names.
# a batch will contain multiple pages of last names.
def scrape_batch_of_mf_first_names(win_loc, mf, session):
    stat = 'SUCCESS'
    # done = False
    batch_count = 0
    nameRec = []
    # open the last file, read the last line, to obtain the last name and first name to continue.
    # finish the current page, update counter, goes to the next page, update names, and num of names,
    # repeat above until complete 8192 names. eventaully, all name will be save.d
    last_first = get_last_first_name(mf)
    while len(nameRec) < MIN_BATCH_SIZE:
        log_1('Current Batch Size: ' + str(len(nameRec)))

        log_1("Last scraped last name: ")
        print(last_first)
        next_first = get_next_tbs_page_index(last_first)
        if next_first[1] == 'None':
            log_1("we are done with getting first names.")
            # done = True
            break
        else:
            log_1("Next to be scraped last name: "+next_first[0]+" AND "+next_first[1])
            scrape_one_page_of_first_names(win_loc, mf, next_first[0], next_first[1], nameRec)
            print(nameRec)
            if nameRec[len(nameRec)-1][0] == 'Z':
                # stop, after fetching the last last name.
                break
            else:
                if nameRec[len(nameRec)-1][0] == next_first[0][0]:
                    # a bit of hack here, set Z and the get_next_tbs_page_index func will get to the next culture clement.
                    last_first[0] = 'ZZZ' + next_first[1]
                    nameRec.append('ZZZ' + next_first[1])
                    break
                else:
                    last_first = next_first

    # if not done:
    send_mf_info_to_cloud(session, nameRec, mf, next_first[1])
    # save_mf_first_names_to_file(nameRec, mf, next_first[1])
    return stat


# file names are formatted as "male_fn_startingInitial_endingInitial_culture_.csv"
def obtained_all_mf_first_names(mf):
    gotAll = False
    names_path = 'C:/CrawlerData/names'
    nfiles = os.listdir(names_path)
    nfiles = list(filter(lambda f: f.endswith('.csv'), nfiles))
    if mf == 'Male':
        nfiles = list(filter(lambda f: f.startswith('male_fn_'), nfiles))
    else:
        nfiles = list(filter(lambda f: f.startswith('female_fn_'), nfiles))
    # parse file name
    if len(nfiles) > 0:
        names = nfiles[len(nfiles)-1].split('_')
        if len(names) == 5 and names[3] == 'Z':
            gotAll = True
    else:
        log_1('Not even started yet...')
    return gotAll


# this function return a 2-tuple of last name and index number where we can find the page that contains the name.
# for example,
def get_last_first_name(mf):
    last_first = ['0', '0']
    names_path = 'C:/CrawlerData/names/'
    nfiles = os.listdir(names_path)
    nfiles = list(filter(lambda f: f.endswith('.csv'), nfiles))
    if mf == 'Male':
        nfiles = list(filter(lambda f: f.startswith('male_fn_'), nfiles))
    else:
        nfiles = list(filter(lambda f: f.startswith('female_fn_'), nfiles))

    # parse file name
    if len(nfiles) > 0:

        file_cult_list = [x.split('_')[4] for x in nfiles]
        print(file_cult_list)
        file_cults = list(dict.fromkeys(file_cult_list))  # remove duplicates
        print(file_cults)
        cult_indices = [cults.index(c) for c in file_cults]
        print(cult_indices)
        last_cult_index = max(cult_indices)
        last_cult = file_cults[cult_indices.index(last_cult_index)]
        print('Last:CULT:'+last_cult)

        nfiles = list(filter(lambda f: f.endswith(last_cult+'_.csv'), nfiles))

        fname = nfiles[len(nfiles) - 1]       # potential bug here, not a good way to find the last file as 21 will be less than 9

        with open((names_path+fname), 'r') as read_obj:
            # pass the file object to reader() to get the reader object
            csv_reader = reader(read_obj)
            names = list(csv_reader)
            # Iterate over each row in the csv using reader object
            # the last item will be a page index number, the 2nd to the last item will be just completed last name.
            last_first = [names[len(names)-1][0], last_cult]
            print('>>>>>>>>>>')
            print(last_first)
            # actually we return something like this: [['Ackroyd'], ['3']]
            # CSV reader will automatically put line fields into list.

    return last_first


# scrape a batch of last names.
# a batch will contain multiple pages of last names.
# first scrape all last names.
# last names will be organized into last name csv files, file names will be in the format of:
# EndingLastName_StaringLastName_.csv, each file contains 8192 last names.
def scrape_male_female_first_names(win_loc, session):
    stat = 'SUCCESS'
    batch_count = 0
    while not obtained_all_mf_first_names('Male'):
        log_1('scrape a batch...')
        stat = scrape_batch_of_mf_first_names(win_loc, 'Male', session)
        batch_count = batch_count + 1
        print('BATCH count: ' + str(batch_count))
        if stat == 'FAILURE':
            log_1('scrape failure')
            break
        if batch_count > 2:
            break

    while not obtained_all_mf_first_names('Female'):
        log_1('scrape a batch...')
        stat = scrape_batch_of_mf_first_names(win_loc, 'Female', session)
        batch_count = batch_count + 1
        print('BATCH count: ' + str(batch_count))
        if stat == 'FAILURE':
            log_1('scrape failure')
            break
        if batch_count > 2:
            break
    return stat

