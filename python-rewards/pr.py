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

s = requests.session()


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
    parser.add_argument("notifyemail", help='The email to send confirmation results to')

    args = parser.parse_args()
    opts = dict()
    if not args.zuser:
        args.zuser = raw_input("Zeek Username: ")
    if not args.zpass:
        args.zpass = getpass.getpass()
    return parser, args

def login(args):
    params = {'username': args.zuser, 'password': args.zpass }
    login_url = full_url(login_path)
    r = s.post(login_url, config=my_config, data=params)
    print r.status_code
    print r.headers
    print r.encoding
    html = r.text.encode("utf-8")
    return html

def click_place_ad(html):
    soup = BeautifulSoup(html)
    elem = soup.find(href=re.compile("ad_options.asp"))
    href = elem['href']

    place_ad_url = backoffice_url(elem["href"])
    #raise Exception(place_ad_url)
    r = s.get(place_ad_url, config=my_config)
    print r.status_code
    print r.headers
    print r.encoding
    html = r.text.encode("utf-8")
    return html

def click_register_ad(html):
    soup = BeautifulSoup(html)
    elem = soup.find(href=re.compile("ad_submit.asp"))
    print elem
    register_ad_url = backoffice_url(elem["href"])
    r = s.get(register_ad_url, config=my_config)
    print r.status_code
    print r.headers
    print r.encoding
    html = r.text.encode("utf-8")
    return html

def submit_ad(html, args):
    url = backoffice_url("ad_submit.asp")
    params = {
        'venue' : "FreeZeekBids.BlogSpot.COM",
        'adtype': "Text Ad",
        'viewableat': args.adurl,
        'Submit' : 'Submit',
        'approvedtext' : ""
    }

    #print html
    soup = BeautifulSoup(html)
    for hidden in "username CD submitting".split():
        elem = soup.find(attrs={"name" : hidden})
        print "search for {0} yielded {1}".format(hidden, elem)
        params[hidden] = elem["value"]

    r = s.post(url, data=params, config=my_config)
    print r.status_code
    print r.headers
    print r.encoding
    html = r.text.encode("utf-8")
    return html

def email_confirmation(email, html, user):
    # Import smtplib for the actual sending function
    import smtplib

    # Import the email modules we'll need
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    text = 'hi there'
    msg = MIMEMultipart('alternative')
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)


    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = 'Zeek posting for {0}'.format(user)
    msg['From'] = 'thequietcenter@gmail.com'
    msg['To'] = email

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP('localhost')
    s.set_debuglevel(1)
    s.sendmail(msg['To'], [msg['From']], msg.as_string())
    s.quit()


if __name__ == '__main__':
    parser, args = parse_command_line()

    html = login(args)
    html = click_place_ad(html) # simulate clicking on "PLACE YOUR AD"
    html = click_register_ad(html) # click on Register your Ad to Qualify for Today's Cash Rewards
    print "*** submitting ad ***"
    html = submit_ad(html,args)
    email_confirmation(args.notifyemail, html, args.zuser)
