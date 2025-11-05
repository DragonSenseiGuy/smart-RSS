from flask import Flask, render_template
from feed2json import feed2json

app = Flask(__name__)

@app.route("/")
def home():
    json_feed:dict = feed2json("https://simonwillison.net/atom/everything/")
    
    for item in json_feed["items"]:
        app.logger.debug(item["title"])
    return render_template("home.html", items=json_feed["items"])

if __name__=="__main__":
    app.run()
