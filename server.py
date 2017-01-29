from flask import Flask, render_template, request
from pymongo import MongoClient
import requests
import os
app = Flask(__name__)

client = MongoClient(os.environ.get('MONGODB_URI'))
database = client.heroku_zf4q464k


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        url = request.form['url']
        saveToDatabase(email, url)
    return render_template('index.html')


def saveToDatabase(email, url):
    content = requests.get(url).text

    posts = database.posts
    post = {"email": email, "url": url, "content": content}
    posts.insert_one(post)

    print("email: " + email)
    print("url: " + url)
    print("content: " + content)

if __name__ == "__main__":
    app.run()
