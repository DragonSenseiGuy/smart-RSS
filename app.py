from flask import Flask, render_template, request, redirect
from feed2json import feed2json
import os
from dotenv import load_dotenv
import dateutil.parser

app = Flask(__name__)
load_dotenv()

rss_feeds=[]

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

@app.route("/settings")
def settings():
    return render_template("settings.html")

@app.route("/add_feed", methods=["POST"])
def add_feed():
    feed_url = request.form.get("feed_url")
    if feed_url:
        rss_feeds.append(feed_url)
    return redirect("/settings?success=True")

if __name__=="__main__":
    app.run()