from flask import Flask
from flask import render_template
from flask import request
import json

# https://www.w3schools.com/python/python_json.asp
# https://www.programiz.com/python-programming/json


# with open('rezepte.json', 'w') as f:
# json.dump(rezepte, f, indent=4, sort_keys=True)


app = Flask("Hello World")

rezeptname = ""
global rezeptberechnet
rezeptberechnet = []
@app.route("/", methods=['GET', 'POST'])
@app.route("/hello", methods=['GET', 'POST'])
def hello():
    #rezeptenamen werden hier vom json ins main.py geladen
    r = open("rezepte.json")
    rezepte_list = json.load(r)
    r2 = open("menuwahl.json")
    menuwahl = json.load(r2)
    rezeptenamen = []
    rezepteindex = 0
    #um Menu in Dropdown hinzuzufügen
    for item in rezepte_list:
        rezeptenamen.append(rezepte_list[rezepteindex]["rezeptname"])
        rezepteindex = rezepteindex + 1
    #mit Hilfe einer JSON Datei werden die eigegebenen Daten in die Berechnung übertragen - global variabeln sind dadurch eliminiert
    if request.method == 'POST':
        if request.form.get("eintragen") == "Eintragen":
            menuwahl["menu"] = request.form["rezepteliste"]
            menuwahl["anzahlPersonen"] = request.form["anzahl"]
            menuwahl["name"] = request.form["vorname"]

        with open('menuwahl.json', 'w') as f:
            json.dump(menuwahl, f, indent=4, sort_keys=True)

    return render_template('index.html', rezepteliste=rezeptenamen)

#mit url for die Parameter mitgeben um die global zu überspringen (um gekapselt zu programmieren)
@app.route("/berechnung")
def berechnung():
    r = open("rezepte.json")
    rezepte_list = json.load(r)
    r2 = open("menuwahl.json")
    menuwahl = json.load(r2)
    rezepteindex2 = 0
    zutatenindex = 0

    # hier werden die Daten aus der Json Datei geholt
    rezeptberechnet = []

    for item in rezepte_list:
        if menuwahl["menu"] == rezepte_list[rezepteindex2]["rezeptname"]:
            for item in rezepte_list[rezepteindex2]["zutaten"]:
                rezeptberechnet.append(rezepte_list[rezepteindex2]["zutaten"][zutatenindex])
                zutatenindex = zutatenindex + 1
        rezepteindex2 = rezepteindex2 + 1
    print(rezeptberechnet)
    berechnetindex = 0
    for item in rezeptberechnet:
        rezeptberechnet[berechnetindex]["menge"] = rezeptberechnet[berechnetindex]["menge"] * int(menuwahl["anzahlPersonen"])
        berechnetindex = berechnetindex + 1
    print(rezeptberechnet)

    return render_template('begruessung.html', rezeptberechnet=rezeptberechnet, vorname=menuwahl["name"], rezepteliste=menuwahl["menu"], personenzahl=menuwahl["anzahlPersonen"])
@app.route("/einkaufsliste")
def einkaufsliste():


    return render_template('einkaufsliste.html')



if __name__ == "__main__":
    app.run(debug=True, port=5000)  # 127.0.0.1 ist immer der Home-Browser
