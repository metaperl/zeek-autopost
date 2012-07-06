# here we go

# https://www.zeekrewards.com/backoffice/back_office.asp

# post username 
# post password

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
        opts['zuser'] = raw_input("Zeek Username: ")
    if not args.zpass:
        opts['zpass'] = getpass.getpass()
    return parser, args, opts

if __name__ == '__main__':
    parser, args, opts = parse_command_line()

    import httplib, urllib

    params = urllib.urlencode({'@username': opts.zuser, '@password': opts.zpass })
    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}
    conn = httplib.HTTPSConnection("www.zeekrewards.com")
    conn.request("POST", "", params, headers)
    response = conn.getresponse()
    print response.status, response.reason

    data = response.read()
    print data
