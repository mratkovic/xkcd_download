#!/usr/bin/env python

import sys
import os
import re
import json


if sys.version_info > (3, 0):
    # Python 3
    from urllib.request import urlopen, urlretrieve
else:
    # Python 2
    from urllib import urlopen, urlretrieve


JSON_DIR = 'json_files'
IMG_DIR = 'xkcd_imgs'


def main():
    init_dirs()
    os.chdir(IMG_DIR)

    latest_downloaded = get_downloaded_max()
    latest_available = get_most_recent()

    for cnt in range(latest_downloaded + 1, latest_available + 1):
        if cnt == 404:
            continue  # lol
        get_img(cnt)


def create_dir(dir_path):
    """ Creates directory if one doesn't exist """

    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)
        print("Created {} directory".format(dir_path))

def init_dirs():
    """ Creates directories for storing JSON files and images """

    create_dir(JSON_DIR)
    create_dir(IMG_DIR)


def get_downloaded_max():
    """ Gets index of latest downloaded comic """

    get_num = lambda path:  int(re.sub(r"\..+", "", path))  # 1.png to 1
    return max([0] + [get_num(img) for img in os.listdir('.')])


def get_most_recent():
    """ Gets index of latest commic available on xkcd web site """

    print("Fetching home page: Getting latest comic")

    req = urlopen("http://xkcd.com/info.0.json")
    line_entry = req.read().decode("utf-8")   # json

    json_entry = json.loads(line_entry)
    num = int(json_entry['num'])

    print("Latest comic is: #{}".format(num))
    return num


def get_img(number):
    """ Downloades and stores comic with given number from xkcd site """

    print("Getting image for comic: #{}".format(number))

    # get page
    url = "http://xkcd.com/{}/info.0.json".format(number)
    req = urlopen(url)
    comic_str_entry = req.read().decode("utf-8")

    # get json and extract img url
    comic_json_entry = json.loads(comic_str_entry)
    img_url = comic_json_entry['img']
    ext = img_url.split('.')[-1]

    # download the img
    filename = "{}.{}".format(number, ext)
    urlretrieve(img_url, filename)

    # save json
    json_out = "../{}/{}.json".format(JSON_DIR, number)
    with open(json_out, 'w') as fout:
        fout.write(comic_str_entry)

    print("Downloaded:  #{}\n".format(number))

if __name__ == '__main__':
    main()
