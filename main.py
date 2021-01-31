from flask import Flask, render_template
from flask_ngrok import run_with_ngrok
# from data import scrape

app = Flask(__name__)
run_with_ngrok(app)

@app.route("/")
def home():
    return render_template("index.html")

# currently not needed
# @app.route("/youtube")
# def youtube():
#     return render_template("youtube.html")

# @app.route("/twitter")
# def twitter():
#     return render_template("twitter.html")

if __name__ == "__main__":
    app.run()