from flask import Flask, request, render_template
from data import scrape

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello world"

if __name__ == "__main__":
    app.run()