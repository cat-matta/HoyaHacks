from flask import Flask, request, render_template
from data import scrape

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/youtube")
def youtube():
    return render_template("youtube.html")

@app.route("/twitter")
def twitter():
    return render_template("twitter.html")
if __name__ == "__main__":
    app.run()