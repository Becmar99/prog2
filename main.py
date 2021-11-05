from flask import Flask
from flask import render_template

app = Flask("Hello World")


@app.route("/hello")
def hello():
    return render_template('index.html', name="Marc")

@app.route("/test")
def test():
    return "Super - wie immer"

@app.route("/menu")
def menu():
    text = "Tomaten"
    return text


@app.route("/flammkuchen")
def flammkuchen():
    return "Zwiebeln, Speck, Creme"


if __name__ == "__main__":
    app.run(debug=True, port=5000) #127.0.0.1 ist immer der Home-Browser
