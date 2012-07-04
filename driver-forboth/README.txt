# USAGE

1. Get the blog id:

  cd ..\python-blogger
  python pb.py --listblogs --username $GOOGLE_EMAIL --password $GOOGLE_PASSWORD
  # take note of the BLOG_ID
  
  python pb.py --blog $BLOG_ID \
    --username thequietcenter@gmail.com --password gelgelgelg1 \
    --zeekid $ZEEK_ID