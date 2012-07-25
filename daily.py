#!/usr/bin/python

import subprocess

import config

for zeekid,zeekpass in config.users.items():
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

    html_result = subprocess.check_output(
        ["./pr.py",
         "--zuser", zeekid,
         "--zpass", zeekpass,
         ad_url
     ],
        cwd="python-rewards"
    )
    print html_result


    print("here it is", ad_url)
