#!/usr/bin/python

# https://www.zeekrewards.com/backoffice/back_office.asp

# post username
# post password

login_host = 'www.zeekrewards.com'
login_path = '/backoffice/back_office.asp'
login_url = "https://{0}{1}".format(login_host, login_path)

#raise Exception(login_url)

class ZeekUser:
    def __init__(self, username, password):
        self.username = username
        self.password = password


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

if __name__ == '__main__':
    parser, args, opts = parse_command_line()

    import requests

    params = {'username': args.zuser, 'password': args.zpass }

    r = requests.post(login_url, data=params)
    print r.status_code
    print r.headers
    print r.encoding
    print r.text.encode("utf-8")
