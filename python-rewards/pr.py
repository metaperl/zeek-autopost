#!/usr/bin/python

# https://www.zeekrewards.com/backoffice/back_office.asp

# post username
# post password

import re
import sys

from BeautifulSoup import BeautifulSoup
import requests

login_host = 'www.zeekrewards.com'
login_path = '/backoffice/back_office.asp'

my_config = {'verbose': sys.stderr}

#raise Exception(login_url)

class ZeekUser:
    def __init__(self, username, password):
        self.username = username
        self.password = password

def full_url(path):
    return "http://{0}/{1}".format(login_host, path)

def backoffice_url(path):
    return full_url("{0}/{1}".format("backoffice", path))

def parse_command_line():
    import getpass

    import argparse

    parser = argparse.ArgumentParser(description='Post zeek ad url')

    parser.add_argument("--zuser", help='Zeek Rewards username')
    parser.add_argument("--zpass", help='Zeek Rewards password')
    parser.add_argument("adurl", help='The URL of the ad you posted today')

    args = parser.parse_args()
    opts = dict()
    if not args.zuser:
        args.zuser = raw_input("Zeek Username: ")
    if not args.zpass:
        args.zpass = getpass.getpass()
    return parser, args, opts

def login(args):
    params = {'username': args.zuser, 'password': args.zpass }
    login_url = full_url(login_path)
    r = requests.post(login_url, data=params)
    print r.status_code
    print r.headers
    print r.encoding
    html = r.text.encode("utf-8")
    return html

def place_ad(html):
    soup = BeautifulSoup(html)
    elem = soup.find(href=re.compile("ad_options.asp"))
    print elem
    place_ad_url = backoffice_url(elem["href"])
    r = requests.get(place_ad_url, config=my_config)
    print r.status_code
    print r.headers
    print r.encoding
    html = r.text.encode("utf-8")
    return html

def register_ad(html):
    soup = BeautifulSoup(html)
    elem = soup.find(href=re.compile("ad_submit.asp"))
    print elem
    register_ad_url = backoffice_url(elem["href"])
    r = requests.get(register_ad_url, config=my_config)
    print r.status_code
    print r.headers
    print r.encoding
    html = r.text.encode("utf-8")
    return html



if __name__ == '__main__':
    parser, args, opts = parse_command_line()

    html = login(args)
    html = place_ad(html) # simulate clicking on "PLACE YOUR AD"
    html = register_ad(html) # click on Register your Ad to Qualify for Today's Cash Rewards
    print html
