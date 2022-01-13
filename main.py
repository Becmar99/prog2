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
rezeptberechnet = []


@app.route("/", methods=['GET', 'POST'])
def hello():
    # rezeptenamen werden hier vom json ins main.py geladen
    r = open("rezepte.json")
    rezepte_list = json.load(r)
    r2 = open("menuwahl.json")
    menuwahl = json.load(r2)
    rezeptenamen = []
    rezepteindex = 0
    # um Menu in Dropdown hinzuzufügen
    for item in rezepte_list:
        rezeptenamen.append(rezepte_list[rezepteindex]["rezeptname"])
        rezepteindex = rezepteindex + 1
    # mit Hilfe einer JSON Datei werden die eigegebenen Daten in die Berechnung übertragen -
    # global variabeln sind dadurch eliminiert
    if request.method == 'POST':
        if request.form.get("eintragen") == "Eintragen":
            menuwahl["menu"] = request.form["rezepteliste"]
            menuwahl["anzahlPersonen"] = request.form["anzahl"]
            menuwahl["name"] = request.form["vorname"]

        with open('menuwahl.json', 'w') as f:
            json.dump(menuwahl, f, indent=4, sort_keys=True)

    return render_template('index.html', rezepteliste=rezeptenamen)


# mit url for die Parameter mitgeben um die global zu überspringen (um gekapselt zu programmieren)
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
        rezeptberechnet[berechnetindex]["menge"] = rezeptberechnet[berechnetindex]["menge"] * int(
            menuwahl["anzahlPersonen"])
        berechnetindex = berechnetindex + 1
    menuwahl["rezept_berechnet"] = rezeptberechnet

    with open('menuwahl.json', 'w') as f:
        json.dump(menuwahl, f, indent=4, sort_keys=True)
    return render_template('begruessung.html', rezeptberechnet=rezeptberechnet, vorname=menuwahl["name"],
                           rezepteliste=menuwahl["menu"], personenzahl=menuwahl["anzahlPersonen"])


@app.route("/einkaufsliste", methods=['GET', 'POST'])
def einkaufsliste():
    r = open("vorratskammer.json")
    vorrats_list = json.load(r)
    r2 = open("menuwahl.json")
    menuwahl = json.load(r2)
    r4 = open("einkaufsliste.json")
    einkaufsliste = json.load(r4)
    benoetigte_anzahl = 0
    mindestbestand_anzahl = 0
    rezeptenamen = []
    buttontoggle = True
    # hier wird die jede Zutat Menge von der rezeptberechnet liste mit der vorratsliste abgeglichen
    if einkaufsliste == []:
        for zutat in vorrats_list:
            print("1")
            for item in menuwahl["rezept_berechnet"]:
                if zutat["zutat"] == item["name"]:
                    zutat["menge"] = zutat["menge"] - item["menge"]
                    if zutat["menge"] < 0:
                        benoetigte_anzahl = zutat["menge"] * -1
                        mindestbestand_anzahl = benoetigte_anzahl + zutat["mindestbestand"]  # zwingend da zu wenig an Lager
                        einkaufsliste.append({"name": item["name"], "benötigte_anzahl": str(benoetigte_anzahl) + " " + zutat["mengenart"],
                                              "mindestbestand_anzahl": str(mindestbestand_anzahl) + " " + zutat["mengenart"]})
                    elif 0 <= zutat["menge"] < zutat["mindestbestand"]:
                        benoetigte_anzahl = 0
                        mindestbestand_anzahl = zutat["mindestbestand"] - zutat[
                            "menge"]  # um immer den Mindestbestand zu füllen
                        einkaufsliste.append({"name": item["name"], "benötigte_anzahl": str(benoetigte_anzahl) + " " + zutat["mengenart"],
                                              "mindestbestand_anzahl": str(mindestbestand_anzahl) + " " + zutat["mengenart"]})
                    print("2")
    if request.method == "POST":
        print("3")
        if request.form.get("benoetigt") == "Benötigte Menge einkaufen":
            buttontoggle = False
            print("4")
            menuwahl["rezept_berechnet"] = []
            for zutat in vorrats_list:
                for eintrag in einkaufsliste:
                    if zutat["zutat"] in eintrag["name"]:
                        print("100")
                        if zutat["menge"] <= 0:
                            print("5")
                            zutat["menge"] = 0
            with open('vorratskammer.json', 'w') as f:
                json.dump(vorrats_list, f, indent=4, sort_keys=True)
            einkaufsliste = []


        if request.form.get("mindestbestand") == "empfohlene Menge einkaufen":
            buttontoggle = False
            print("6")
            menuwahl["rezept_berechnet"] = []
            for zutat in vorrats_list:
                for eintrag in einkaufsliste:
                    if zutat["zutat"] in eintrag["name"]:
                        print("7")
                        zutat["menge"] = zutat["mindestbestand"]
            with open('vorratskammer.json', 'w') as f:
                json.dump(vorrats_list, f, indent=4, sort_keys=True)
            einkaufsliste = []


    with open('einkaufsliste.json', 'w') as f:
        json.dump(einkaufsliste, f, indent=4, sort_keys=True)
    with open('vorratskammer.json', 'w') as f:
        json.dump(vorrats_list, f, indent=4, sort_keys=True)
    with open('menuwahl.json', 'w') as f:
        json.dump(menuwahl, f, indent=4, sort_keys=True)


    return render_template('einkaufsliste.html', buttontoggle=buttontoggle, einkaufsliste=einkaufsliste)


if __name__ == "__main__":
    app.run(debug=True, port=5000)  # 127.0.0.1 ist immer der Home-Browser
