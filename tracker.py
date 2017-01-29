import fastmail
import requests
from pymongo import MongoClient
import os

client = MongoClient(os.environ.get('MONGODB_URI'))
database = client.heroku_zf4q464k
posts = database.posts

for post in posts.find():
    latest = requests.get(post.url)
    previous = post.content

    if latest != previous:
        m = fastmail.FastMailSMTP(os.environ.get('FASTMAIL_USER'), os.environ.get('FASTMAIL_PASSWORD'))
        m.send_message(from_addr='"Site Tracker" <sitetracker@nathansmith.io>',
                       to_addrs=[post.email],
                       msg=latest,
                       subject='Hey! ' + post.url + ' has been updated!'
                       )
