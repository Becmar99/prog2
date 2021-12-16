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

    r = open("rezepte.json")
    rezepte_list = json.load(r)
    rezeptenamen = []
    rezepteindex = 0
    #um Menu in Dropdown hinzuzufügen
    for item in rezepte_list:
        rezeptenamen.append(rezepte_list[rezepteindex]["rezeptname"])
        rezepteindex = rezepteindex + 1
    print(rezeptenamen)
    #Global Funktion um die Variabel in die nächste Seite zu übernehmen
    if request.method == 'POST':
        if request.form.get("eintragen") == "Eintragen":
            global rezeptname
            rezeptname = request.form["rezepteliste"]
            global personenzahl
            personenzahl = request.form["anzahl"]
            global vorname
            vorname = request.form["vorname"]
            global rezepteliste
            rezepteliste = request.form["rezepteliste"]
    return render_template('index.html', rezepteliste=rezeptenamen)

#mit url for die Parameter mitgeben um die global zu überspringen (um gekapselt zu programmieren)
@app.route("/berechnung")
def berechnung():
    r = open("rezepte.json")
    rezepte_list = json.load(r)
    rezepteindex2 = 0
    zutatenindex = 0
    global rezeptname
    global personenzahl
    global vorname
    vorname=vorname
    global rezepteliste
    rezepteliste=rezepteliste
    fixemenge = 0
    # hier werden die Daten aus der Json Datei geholt
    global rezeptberechnet
    global rezeptberechnet1

    for item in rezepte_list:
        if rezeptname == rezepte_list[rezepteindex2]["rezeptname"]:
            for item in rezepte_list[rezepteindex2]["zutaten"]:
                rezeptberechnet.append(rezepte_list[rezepteindex2]["zutaten"][zutatenindex])
                zutatenindex = zutatenindex + 1
        rezepteindex2 = rezepteindex2 + 1

    return render_template('begruessung.html', fixemenge=fixemenge, rezeptberechnet=rezeptberechnet, vorname=vorname, rezepteliste=rezepteliste, personenzahl=personenzahl)



if __name__ == "__main__":
    app.run(debug=True, port=5000)  # 127.0.0.1 ist immer der Home-Browser
