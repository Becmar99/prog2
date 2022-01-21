from flask import Flask
from flask import render_template
from flask import request
import json

# https://www.w3schools.com/python/python_json.asp
# https://www.programiz.com/python-programming/json

app = Flask("Hello World")

rezeptname = ""
rezeptberechnet = []


@app.route("/", methods=['GET', 'POST'])
def hello():
    #die rezeptenamen werden hier von rezepte.json ins main.py geladen
    r = open("rezepte.json")
    rezepte_list = json.load(r)
    r2 = open("menuwahl.json")
    menuwahl = json.load(r2)
    rezeptenamen = []
    rezepteindex = 0
    #um die einzelnen menünamen in die dropdown auswahl hinzuzufügen
    for item in rezepte_list:
        rezeptenamen.append(rezepte_list[rezepteindex]["rezeptname"])
        rezepteindex = rezepteindex + 1
    #die eingetragenen daten im formular auf der index.html seite werden im menuwahl.json abgespeichert
    if request.method == 'POST':
        if request.form.get("eintragen") == "Eintragen":
            menuwahl["menu"] = request.form["rezepteliste"]
            menuwahl["anzahlPersonen"] = request.form["anzahl"]
            menuwahl["name"] = request.form["vorname"]


        with open('menuwahl.json', 'w') as f:
            json.dump(menuwahl, f, indent=4, sort_keys=True)

    return render_template('index.html', rezepteliste=rezeptenamen)

@app.route("/berechnung")
def berechnung():
    r = open("rezepte.json")
    rezepte_list = json.load(r)
    #hier werden die gespeicherten daten aus den menuwahl.json datei geladen
    r2 = open("menuwahl.json")
    menuwahl = json.load(r2)
    rezepteindex2 = 0
    zutatenindex = 0

    rezeptberechnet = []

    for item in rezepte_list:
        if menuwahl["menu"] == rezepte_list[rezepteindex2]["rezeptname"]:
            for item in rezepte_list[rezepteindex2]["zutaten"]:
                rezeptberechnet.append(rezepte_list[rezepteindex2]["zutaten"][zutatenindex])
                zutatenindex = zutatenindex + 1
                #hier wird jede einzelne zutat aus der rezepte.json datei geholt und
                #in die liste rezeptberechnet hinzugefügt
        rezepteindex2 = rezepteindex2 + 1
        #hier wird der prozess für jedes rezept durchgeführt
    berechnetindex = 0
    #hier wird zu jeder zutat in der liste rezeptberechnet die menge mit der anzahl personen multipliziert
    #die berechnung der benötigten menge findet statt
    for item in rezeptberechnet:
        rezeptberechnet[berechnetindex]["menge"] = rezeptberechnet[berechnetindex]["menge"] * int(menuwahl["anzahlPersonen"])
        berechnetindex = berechnetindex + 1
    menuwahl["rezept_berechnet"] = rezeptberechnet

    with open('menuwahl.json', 'w') as f:
        json.dump(menuwahl, f, indent=4, sort_keys=True)
    return render_template('berechnung.html', rezeptberechnet=rezeptberechnet, vorname=menuwahl["name"],
                           rezepteliste=menuwahl["menu"], personenzahl=menuwahl["anzahlPersonen"])


@app.route("/einkaufsliste", methods=['GET', 'POST'])
def einkaufsliste():
    #alle benötigten json datein werden geladen
    r = open("vorratskammer.json")
    vorrats_list = json.load(r)
    r2 = open("menuwahl.json")
    menuwahl = json.load(r2)
    r3 = open("einkaufsliste.json")
    einkaufsliste = json.load(r3)
    benoetigte_anzahl = 0
    mindestbestand_anzahl = 0
    rezeptenamen = []
    #mit buttontoggle wird gesteurt, wann die einkaufsmöglichkeitsbutton angezeigt werden
    buttontoggle = True
    #hier wird für jede Zutat die menge von der rezeptberechnet liste mit der vorratsliste abgeglichen
    if einkaufsliste == []:
        for zutat in vorrats_list:
            for item in menuwahl["rezept_berechnet"]:
                #die berechnete menge wird hier mit dem bestand im vorrat abgeglichen
                if zutat["zutat"] == item["name"]:
                    zutat["menge"] = zutat["menge"] - item["menge"]
                    if zutat["menge"] < 0:
                        benoetigte_anzahl = zutat["menge"] * -1 #durch multiplizieren mit Faktor -1 wird der bestand 0 erreicht
                        mindestbestand_anzahl = benoetigte_anzahl + zutat["mindestbestand"]  #die benötigte anzahl wir mit dem mindestbestand addiert um den Vorrat zu füllen
                        #einaufsliste.json wird erstellt. die zutaten werden mit benötigter sowie mindestbestand anzahl aufgelistet
                        einkaufsliste.append({"name": item["name"], "benötigte_anzahl": str(benoetigte_anzahl) + " " + zutat["mengenart"],
                                              "mindestbestand_anzahl": str(mindestbestand_anzahl) + " " + zutat["mengenart"]})
                    elif 0 <= zutat["menge"] < zutat["mindestbestand"]:
                        benoetigte_anzahl = 0 #wenn die abgeglichene Menge zwischen 0 und dem mindestbestand liegt wird
                        #die benötigte anzahl auf 0 gesetzt, da man die zutat nicht einkaufen muss
                        mindestbestand_anzahl = zutat["mindestbestand"] - zutat[
                            "menge"]  #um immer den mindestbestand zu füllen, damit der vorrat immer voll ist
                        einkaufsliste.append({"name": item["name"], "benötigte_anzahl": str(benoetigte_anzahl) + " " + zutat["mengenart"],
                                              "mindestbestand_anzahl": str(mindestbestand_anzahl) + " " + zutat["mengenart"]})
    if request.method == "POST":
        if request.form.get("benoetigt") == "benötigte Menge einkaufen":
            buttontoggle = False #durch dieses statement werden die zwei einkaufsbutton verschwinden
            menuwahl["rezept_berechnet"] = []#menuwahl.json liste wird bereinigt, da ansonsten die bestehende Liste
            #immer weiter ausgebaut wird
            #hier werden die betroffenen zutaten welche <= 0 sind in der vorratsliste auf 0 gesetzt
            #(die benötigte menge wurde eingekauft)
            for zutat in vorrats_list:
                for eintrag in einkaufsliste:
                    if zutat["zutat"] in eintrag["name"]:
                        if zutat["menge"] <= 0:
                            zutat["menge"] = 0
            with open('vorratskammer.json', 'w') as f:
                json.dump(vorrats_list, f, indent=4, sort_keys=True)
            einkaufsliste = [] #die einkaufsliste wird geleert


        if request.form.get("mindestbestand") == "empfohlene Menge einkaufen":
            buttontoggle = False #durch dieses statement werden die zwei einkaufsbutton verschwinden
            menuwahl["rezept_berechnet"] = [] #menuwahl.json liste wird bereinigt, da ansonsten die bestehende Liste
            # immer weiter ausgebaut wird

            #hier werden die betroffenen zutaten in der vorratsliste auf den mindestbestand gesetzt
            #(die empfohlene menge wurde eingekauft)
            for zutat in vorrats_list:
                for eintrag in einkaufsliste:
                    if zutat["zutat"] in eintrag["name"]:
                        zutat["menge"] = zutat["mindestbestand"]
            with open('vorratskammer.json', 'w') as f:
                json.dump(vorrats_list, f, indent=4, sort_keys=True)
            einkaufsliste = [] #die einkaufsliste wird geleert


    with open('einkaufsliste.json', 'w') as f:
        json.dump(einkaufsliste, f, indent=4, sort_keys=True)
    with open('vorratskammer.json', 'w') as f:
        json.dump(vorrats_list, f, indent=4, sort_keys=True)
    with open('menuwahl.json', 'w') as f:
        json.dump(menuwahl, f, indent=4, sort_keys=True)


    return render_template('einkaufsliste.html', buttontoggle=buttontoggle, einkaufsliste=einkaufsliste)


if __name__ == "__main__":
    app.run(debug=True, port=5000)  # 127.0.0.1 ist immer der Home-Browser
