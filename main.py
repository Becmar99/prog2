from flask import Flask
from flask import render_template
from flask import request
import json
# https://www.w3schools.com/python/python_json.asp
# https://www.programiz.com/python-programming/json

# a Python object (dict):
rezepte = {
  "Tomatensuppe": {
    "titel": "Tomatensuppe",
    "anzahl_personen": 2,
    "menge_1": 700,
    "mass_1": "gramm",
    "artikel_1:": ">Tomaten",
    "menge_2": 2,
    "mass_2": "dl",
    "artikel_2": "Rahm",
    "menge_3": 6,
    "mass_3": "dl",
    "artikel_3": "Bouillon"}
}

with open('rezepte.json', 'w') as f:
  json.dump(rezepte, f, indent=4, sort_keys=True)

app = Flask("Hello World")


@app.route("/hello", methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        ziel_person = request.form['vorname']
        rueckgabe_string_name = "" + ziel_person + ""
        ziel_person = request.form['menu']
        rueckgabe_string = " " + ziel_person + " "
        ziel_anzahl = request.form['anzahl']
        rueckgabe_string1 = " " + ziel_anzahl + " Personen"
#dict holen nach rezept suchen und dann berechen und mengen anpassen
        return render_template("begruessung.html", ansprechperson=rueckgabe_string_name, menu=rueckgabe_string, anzahl=rueckgabe_string1)

    return render_template('index.html')


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
