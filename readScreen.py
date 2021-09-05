import pytesseract
import cv2
from pytesseract import Output
import re
import numpy

def read_full_names(last_name):
    # analyze the screen for the first names.
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\Tesseract.exe'
    # screen_file = 'c:/AmazonSeller/JSRPA/nameaddr/Xing01.png'
    # screen_file = 'c:/AmazonSeller/JSRPA/nameaddr/Smith1001.png'
    # screen_file = 'c:/AmazonSeller/JSRPA/nameaddr/Smith1002.png'
    screen_file = 'c:/AmazonSeller/JSRPA/nameaddr/Smith9301.png'

    img = cv2.imread(screen_file)
    d = pytesseract.image_to_data(img, output_type=Output.DICT)
    for k in d.keys():
        print(k, end='::')
        print(d[k])
    if single_page(d):
        print('single page')
        # find the index of the last occurrence of "Page",
        # then extract all words after which starts with letter LI

        start = subfinder(d["text"], ['Names', 'With', 'Last', 'Name', last_name])
        end = subfinder(d["text"], ['People', 'Directory'])
        start_idx = start[0] + 3
        end_idx = end[0]

        last_names_i = [i for i, ln in enumerate(d['text']) if i > start_idx and i < end_idx and re.match(rf'{last_name}', ln)]
        print(len(last_names_i))
        first_names_i = [x - 1 for x in last_names_i]
        real_first_name_i = [first_names_i[index] for index in range(1, len(first_names_i)-1)]
        print(real_first_name_i)
        first_names = numpy.array(d['text'])[real_first_name_i].tolist()
        print(first_names)
        print(len(first_names))
        first_names.append('single')

    elif single_last_name_page(d):
        print('single last name page')
        # find the index of the last occurance of "Page",
        # then extract all words after which starts with letter LI
        start = subfinder(d["text"], ['People', '/', last_name[0], '/', last_name])
        end = subfinder(d["text"], ['Page:'])
        start_idx = start[0] + 4
        end_idx = end[0]

        last_names_i = [i for i, ln in enumerate(d['text']) if i > start_idx and i < end_idx and re.match(rf'{last_name}', ln)]
        print(len(last_names_i))
        first_names_i = [x - 1 for x in last_names_i]
        real_first_name_i = [first_names_i[index] for index in range(0, len(first_names_i))]
        print(real_first_name_i)
        first_names = numpy.array(d['text'])[real_first_name_i].tolist()
        print(first_names)
        print(len(first_names))
        first_names.append('single')

    elif name_top_page(d):
        print('top half')
        # find the index of the last occurance of "Page",
        # then extract all words after which starts with letter LI
        start = subfinder(d["text"], ['People', '/', last_name[0], '/', last_name])
        print(last_name[0])
        print(start)
        start_idx = start[0] + 4

        last_names_i = [i for i, ln in enumerate(d['text']) if i >= start_idx and re.match(rf'{last_name}', ln)]
        print(len(last_names_i))
        first_names_i = [x - 1 for x in last_names_i]
        real_first_name_i = [first_names_i[index] for index in range(1, len(first_names_i))]
        print(real_first_name_i)
        first_names = numpy.array(d['text'])[real_first_name_i].tolist()
        print(first_names)
        print(len(first_names))
        first_names.append('single')

    elif name_bottom_page(d):
        print('bottom half????')
        # the strategy is to find "e.g John Smith", and "Free Address Lookup"
        # then extract all words in between and filter out false match words.
        start = subfinder(d["text"], ['TruePeopleSearch'])
        end = subfinder(d["text"], ['Search', 'Alphabetically'])
        start_idx = start[0]
        end_idx = end[0]

        last_names_i = [i for i, ln in enumerate(d['text']) if i > start_idx and i < end_idx and re.match(rf'{last_name}', ln)]
        print(len(last_names_i))
        first_names_i = [x - 1 for x in last_names_i]
        real_first_name_i = [first_names_i[index] for index in range(0, len(first_names_i))]
        print(real_first_name_i)
        first_names = numpy.array(d['text'])[real_first_name_i].tolist()
        print(first_names)
        print(len(first_names))
        first_names.append('single')

        start = subfinder(d["text"], ['Page:'])
        end = subfinder(d["text"], ['People', 'Directory'])
        pn_start_idx = start[0]
        end_idx = end[0]
        pn_i = [i for i, ln in enumerate(d['text']) if i > start_idx and i < end_idx and re.match('[0-9].*', ln)]
        pn = numpy.array(d['text'])[pn_i].tolist()
        print(pn)
        pns = []
        for s in pn:
            pns.extend(s.split(','))
        print(pns)
        # now, filter out empty string
        real_pns_i = [i for i, ln in enumerate(pns) if re.match('[0-9].*', ln)]
        print(real_pns_i)
        real_pns = numpy.array(pns)[real_pns_i].tolist()
        print(real_pns)
        print(len(real_pns))

    return

def read_last_names(lni):
    # analyze the screen
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\Tesseract.exe'
    screen_file = 'c:/AmazonSeller/JSRPA/nameaddr/X01.png'
    img = cv2.imread(screen_file)
    d = pytesseract.image_to_data(img, output_type=Output.DICT)
    for k in d.keys():
        print(k, end='::')
        print(d[k])
    if single_page(d):
        print('single page')
        # find the index of the last occurrence of "Page",
        # then extract all words after which starts with letter LI

        start = subfinder(d["text"], ['Names', 'Starting', 'With'])
        end = subfinder(d["text"], ['People', 'Directory'])
        start_idx = start[0]+3
        end_idx = end[0]

        last_names_i = [i for i, ln in enumerate(d['text']) if i > start_idx and i < end_idx and re.match(rf'{lni}.+', ln)]
        print(last_names_i)
        last_names = numpy.array(d['text'])[last_names_i].tolist()
        print(last_names)
        print(len(last_names))
        last_names.append('single')

    elif last_name_top_page(d):
        print('top half')
        # find the index of the last occurance of "Page",
        # then extract all words after which starts with letter LI
        page_word_indices = [li for li, wd in enumerate(d["text"]) if wd == 'Page']
        last_page_index = page_word_indices[len(page_word_indices)-1]
        print(page_word_indices)
        print(last_page_index)
        last_names_i = [i for i, ln in enumerate(d['text']) if i > last_page_index and re.match(rf'{lni}.+', ln)]
        print(last_names_i)
        last_names = numpy.array(d['text'])[last_names_i].tolist()
        print(last_names)
        print(len(last_names))
        last_names.append('top')

    elif last_name_bottom_page(d):
        print('bottom half????')
        # the strategy is to find "e.g John Smith", and "Free Address Lookup"
        # then extract all words in between and filter out false match words.
        start = subfinder(d["text"], ['e.g', 'John', 'Smith'])
        end = subfinder(d["text"], ['Free', 'Address', 'Lookup'])
        start_idx = start[0]+3
        end_idx = end[0]

        last_names_i = [i for i, ln in enumerate(d['text']) if i > start_idx and i < end_idx and re.match(rf'{lni}.+', ln)]
        print(last_names_i)
        last_names = numpy.array(d['text'])[last_names_i].tolist()
        print(last_names)
        print(len(last_names))
        last_names.append('bottom')

    return


# read name address details, note there could multiple same names.
def read_details(fn, ln):
    # analyze the screen for the first names.
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\Tesseract.exe'
    # screen_file = 'c:/AmazonSeller/JSRPA/nameaddr/Xing01.png'
    # screen_file = 'c:/AmazonSeller/JSRPA/nameaddr/Smith1001.png'
    # screen_file = 'c:/AmazonSeller/JSRPA/nameaddr/Smith1002.png'
    screen_file = 'c:/AmazonSeller/JSRPA/nameaddr/RonaldSmithDetails002.png'

    img = cv2.imread(screen_file)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    cv2.imwrite("c:/AmazonSeller/JSRPA/nameaddr/thresh1.png", thresh1)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (151, 3))
    morph0 = cv2.morphologyEx(thresh1, cv2.MORPH_DILATE, kernel)
    cv2.imwrite("c:/AmazonSeller/JSRPA/nameaddr/morph0.png", morph0)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 17))
    morph1 = cv2.morphologyEx(morph0, cv2.MORPH_OPEN, kernel)
    cv2.imwrite("c:/AmazonSeller/JSRPA/nameaddr/morph1.png", morph1)

    kernel1 = numpy.ones((3, 5), numpy.uint8)
    kernel2 = numpy.ones((9, 9), numpy.uint8)
    img1 = cv2.erode(thresh1, kernel1, iterations=1)
    cv2.imwrite("c:/AmazonSeller/JSRPA/nameaddr/img1.png", img1)
    img2 = cv2.dilate(img1, kernel2, iterations=3)
    cv2.imwrite("c:/AmazonSeller/JSRPA/nameaddr/img2.png", img2)
    img3 = cv2.bitwise_and(thresh1, img2)
    cv2.imwrite("c:/AmazonSeller/JSRPA/nameaddr/img3.png", img3)
    img3 = cv2.bitwise_not(img3)
    img4 = cv2.bitwise_and(thresh1, thresh1, mask=img3)
    imgLines = cv2.HoughLinesP(img4, 15, numpy.pi / 180, 10, minLineLength=440, maxLineGap=15)
    cv2.imwrite("c:/AmazonSeller/JSRPA/nameaddr/lines.png", imgLines)
    #rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
    # (1) Create long line kernel, and do morph-close-op
    kernel = numpy.ones((1, 40), numpy.uint8)
    morphed = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
    cv2.imwrite("c:/AmazonSeller/JSRPA/nameaddr/line_detected.png", morphed)

    # (2) Invert the morphed image, and add to the source image:
    dst = cv2.add(gray, (255 - morphed))
    cv2.imwrite("c:/AmazonSeller/JSRPA/nameaddr/line_removed.png", dst)

    # enlarge 3.25 is the minimum ratio that tesseract can reliably offset the underline effect.
    # this works, but takes a large process time hit.
    # new_w = int(img.shape[1]*3.25)
    # new_h = int(img.shape[0]*3.25)
    # dim = (new_w, new_h)
    # new_img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    d = pytesseract.image_to_data(dst, output_type=Output.DICT)
    for k in d.keys():
        print(k, end='::')
        print(d[k])
    start = subfinder(d["text"], ['Age'])
    end = subfinder(d["text"], ['32', 'Psc'])
    # start_idx = start[0]
    # end_idx = end[0]
    print(start)
    print(end)
    start = subfinder(d["text"], ['Current', '&', 'Past', 'Addresses'])
    end = subfinder(d["text"], ['(Current', 'Address)'])

    start = subfinder(d["text"], ['Phone', 'Numbers'])
    end = subfinder(d["text"], ['Also', 'Known', 'As'])

    start = subfinder(d["text"], ['Email', 'Addresses'])
    end = subfinder(d["text"], ['Also', 'Previous', 'Addresses'])

    start = subfinder(d["text"], ['View', 'All', 'Details', 'on'])
    return


# read email addresses (max 3) and the back button location.
def read_all_details(fn, ln):
    # analyze the screen for the first names.
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\Tesseract.exe'
    # screen_file = 'c:/AmazonSeller/JSRPA/nameaddr/Xing01.png'
    # screen_file = 'c:/AmazonSeller/JSRPA/nameaddr/Smith1001.png'
    # screen_file = 'c:/AmazonSeller/JSRPA/nameaddr/Smith1002.png'
    screen_file = 'c:/AmazonSeller/JSRPA/nameaddr/RonaldSmithDetails002.png'

    img = cv2.imread(screen_file)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    cv2.imwrite("c:/AmazonSeller/JSRPA/nameaddr/thresh1.png", thresh1)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (151, 3))
    morph0 = cv2.morphologyEx(thresh1, cv2.MORPH_DILATE, kernel)
    cv2.imwrite("c:/AmazonSeller/JSRPA/nameaddr/morph0.png", morph0)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 17))
    morph1 = cv2.morphologyEx(morph0, cv2.MORPH_OPEN, kernel)
    cv2.imwrite("c:/AmazonSeller/JSRPA/nameaddr/morph1.png", morph1)

    kernel1 = numpy.ones((3, 5), numpy.uint8)
    kernel2 = numpy.ones((9, 9), numpy.uint8)
    img1 = cv2.erode(thresh1, kernel1, iterations=1)
    cv2.imwrite("c:/AmazonSeller/JSRPA/nameaddr/img1.png", img1)
    img2 = cv2.dilate(img1, kernel2, iterations=3)
    cv2.imwrite("c:/AmazonSeller/JSRPA/nameaddr/img2.png", img2)
    img3 = cv2.bitwise_and(thresh1, img2)
    cv2.imwrite("c:/AmazonSeller/JSRPA/nameaddr/img3.png", img3)
    img3 = cv2.bitwise_not(img3)
    img4 = cv2.bitwise_and(thresh1, thresh1, mask=img3)
    imgLines = cv2.HoughLinesP(img4, 15, numpy.pi / 180, 10, minLineLength=440, maxLineGap=15)
    cv2.imwrite("c:/AmazonSeller/JSRPA/nameaddr/lines.png", imgLines)
    #rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
    # (1) Create long line kernel, and do morph-close-op
    kernel = numpy.ones((1, 40), numpy.uint8)
    morphed = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
    cv2.imwrite("c:/AmazonSeller/JSRPA/nameaddr/line_detected.png", morphed)

    # (2) Invert the morphed image, and add to the source image:
    dst = cv2.add(gray, (255 - morphed))
    cv2.imwrite("c:/AmazonSeller/JSRPA/nameaddr/line_removed.png", dst)

    # enlarge 3.25 is the minimum ratio that tesseract can reliably offset the underline effect.
    # this works, but takes a large process time hit.
    # new_w = int(img.shape[1]*3.25)
    # new_h = int(img.shape[0]*3.25)
    # dim = (new_w, new_h)
    # new_img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    d = pytesseract.image_to_data(dst, output_type=Output.DICT)
    for k in d.keys():
        print(k, end='::')
        print(d[k])
    start = subfinder(d["text"], ['Age'])
    end = subfinder(d["text"], ['32', 'Psc'])
    # start_idx = start[0]
    # end_idx = end[0]
    print(start)
    print(end)
    start = subfinder(d["text"], ['Current', '&', 'Past', 'Addresses'])
    end = subfinder(d["text"], ['(Current', 'Address)'])

    start = subfinder(d["text"], ['Phone', 'Numbers'])
    end = subfinder(d["text"], ['Also', 'Known', 'As'])

    start = subfinder(d["text"], ['Email', 'Addresses'])
    end = subfinder(d["text"], ['Also', 'Previous', 'Addresses'])

    start = subfinder(d["text"], ['View', 'All', 'Details', 'on'])
    return


def single_page(txt_data):
    single_page_info = False
    print(txt_data)
    if "Last" in txt_data['text'] and "Names" in txt_data['text']:
        if "With" in txt_data['text'] and "People" in txt_data['text'] and "Directory" in txt_data['text']:
            single_page_info = True
    return single_page_info

def detail_top_page(txt_data):
    detail_top_page = False
    print(txt_data)
    if "We" in txt_data['text'] and "Found" in txt_data['text'] and "Names" in txt_data['text']:
        if "Starting" in txt_data['text'] and "With" in txt_data['text']:
            detail_top_page = True
    return detail_top_page

def detail_bottom_page(txt_data):
    detail_bottom_page = False
    print(txt_data)
    if ("Sponsored" in txt_data['text'] and "Links" in txt_data['text']) or ("advertisement" in txt_data['text']):
        detail_bottom_page = True
    return detail_bottom_page



def last_name_top_page(txt_data):
    last_name_top_info = False
    print(txt_data)
    if "Page" in txt_data['text'] and "Last" in txt_data['text'] and "Names" in txt_data['text']:
        if "Starting" in txt_data['text'] and "With" in txt_data['text']:
            last_name_top_info = True
    return last_name_top_info


def last_name_bottom_page(txt_data):
    last_name_bottom_page_info = False
    if "Page:" in txt_data['text'] and "Search" in txt_data['text'] and "Alphabetically" in txt_data['text']:
        last_name_bottom_page_info = True
    return last_name_bottom_page_info


def name_top_page(txt_data):
    last_name_top_info = False
    print(txt_data)
    if "Page" in txt_data['text'] and "People" in txt_data['text'] and "City," in txt_data['text']:
        if "State" in txt_data['text'] and "Zip" in txt_data['text']:
            last_name_top_info = True
    return last_name_top_info


def name_bottom_page(txt_data):
    last_name_bottom_page_info = False
    if "Page:" in txt_data['text'] and "Search" in txt_data['text'] and "Alphabetically" in txt_data['text']:
        last_name_bottom_page_info = True
    return last_name_bottom_page_info


def name_num_top_page(txt_data):
    last_name_top_info = False
    print(txt_data)
    if "Page" in txt_data['text'] and "People" in txt_data['text'] and "City," in txt_data['text']:
        if "State" in txt_data['text'] and "Zip" in txt_data['text']:
            last_name_top_info = True
    return last_name_top_info


def single_last_name_page(txt_data):
    single_page_info = False
    print(txt_data)
    if "City," in txt_data['text'] and "Zip" in txt_data['text'] and "People" in txt_data['text']:
        if "Page" in txt_data['text'] and "Search" in txt_data['text'] and "Alphabetically" in txt_data['text']:
            single_page_info = True
    return single_page_info

# find a sublist from a list.
def subfinder(mylist, pattern):
    match_loc = []
    for i in range(len(mylist) - len(pattern) + 1):
        if mylist[i] == pattern[0] and mylist[i:i+len(pattern)] == pattern:
            match_loc.append(i)
    return match_loc

