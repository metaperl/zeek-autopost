#!/usr/bin/python

# system modules
import subprocess

# local modules
import config

for zeekid,userdict in config.users.items():

    # Post an ad to the blogspot.com blog automatically
    ad_url = subprocess.check_output(
        ["./pb.py",
         "--blog", str(config.blog['id']),
         "--username", config.blog['username'],
         "--password", config.blog['password'],
         "--zeekid", zeekid,
         "./posts/"
     ],
        cwd="python-blogger"
    )

    # Record the URL of the newly posted blog
    html_result = subprocess.check_output(
        ["./pr.py",
         "--zuser", zeekid,
         "--zpass", userdict['zeekpass'],
         ad_url,
         userdict['email']
     ],
        cwd="python-rewards"
    )

    print html_result
    print("here it is", ad_url)
