from flask import Flask, render_template
from feed2json import feed2json
import os
from dotenv import load_dotenv
import dateutil.parser

app = Flask(__name__)
load_dotenv()

rss_feeds=["https://dragonsensei.is-a.dev/atom/everything/", "https://simonwillison.net/atom/everything/", "https://jb3.dev/feed.xml"]

def get_all_items():
    all_items = []
    for feed_url in rss_feeds:
        json_feed:dict = feed2json(feed_url)
        if "items" in json_feed:
            all_items.extend(json_feed["items"])
    all_items.sort(key=lambda item: dateutil.parser.parse(item.get("date_published", "1970-01-01T00:00:00Z")), reverse=True)
    return all_items

@app.route("/")
def home():
    items = get_all_items()
    return render_template("home.html", items=items)

@app.route("/blog/<int:item_number>")
def blog(item_number):
    items = get_all_items()
    if 0 <= item_number < len(items):
        return render_template("blog.html", item=items[item_number])
    return None

if __name__=="__main__":
    app.run()