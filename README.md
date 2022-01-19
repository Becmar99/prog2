# Marc's MenuCalc
# Einleitung
***
Mit Hilfe dieses Programms, werden die Zutaten von Menüs auf die Anzahl der Gäste angepasst.
Dabei berücksichtigt das Programm, welche Zutaten bereits in welcher Menge in der Vorratskammer vorhanden sind 
und generiert entsprechend eine Einkaufsliste um das Menü kochen zu können.

# Flow Chart
***
![_Marc MenuCalc](https://user-images.githubusercontent.com/91119063/139461160-a49a444f-999a-4356-9a2b-d22745d8d365.png)

Die Flow Chart visualisiert den Ablauf des Programms. Es werden die einzelnen Schritte aufgezeigt und welche Eingaben
und Datenabfragen benötigt werden. Die Flowchart dient der besseren Übersicht und zum besseren Verständnis.

# Anwendungen
***
Für die Erstellung des MenuCalc wurden verschiedene Bausteine verwendet. 
Den ganzen Berechnungsaspekt wurde im main.py mit Pycharm abgewickelt. 
Die Darstellung im HTML Format wurde mit Hilfe von Bootstrap Bausteinen erstellt und designed.
Für die Abbildung der Menüs und der manuellen Erweiterung, wurden json Dateien eingesetzt. Die json Datei rezepte.json 
kann durch einfügen weiterer Menüs in der gleichen dict. Struktur beliebig ergänzt werden. Dasselbe gilt bei 
menuwahl.json und vorratskammer.json. Die JSON Datein werden zur Speicherung und Weitergabe verwendet. Besonders bei der
vorratskammer.json Datei ist, dass hier nach betätigen des  Buttons "Benötigte Menge einkaufen" oder "empfohlene Menge 
einkaufen" die Bestände wieder befüllt werden, wie wenn die Zutaten tatsächlich eingekauft werden würden. Damit der
Benutzer seine Einkaufsliste ausgeben kann wurde eine Druckfunktion eingefügt.

# Ablauf des Programms
***
Der Nutzer gibt im ersten Feld seinen Namen ein und wählt das gewünschte Menu und die 
Anzahl Personen für die er kochen möchte aus. Mit dem Eintragen Button werden diese Daten gespeichert.
Durch das klicken des Berechnen Buttons wird aufgelistet, welche Zutaten und Mengen er für dieses Menu benötigt.
In der HTML Seite Berechnung wird die Tabelle mit den Zutaten und den berechneten Mengen angegeben.
Durch das Abgleichen mit der Vorratskammer, wird dem Nutzer eine Einkaufsliste erstellt und ausgegeben.
Der Nutzer weiss somit, wieviel er noch einkaufen muss. Er kann danach entschieden, ob er die mindestens benötigte Menge 
für das Menü mit den Anzahl Personen kaufen will, oder die empfohlene Menge, um auch den Mindestbestand zu füllen. 
Nachdem eine der Optionen gewählt wurde kann der User über den Button "Neu starten" wieder mit der Auswahl eines Menüs 
beginnen.
# Kollaboration
***
Dieses Programm wurde im Rahmen des PROG2 Moduls an der FHGR erstellt. 
Es kann beliebig verwendet werden und ist free downloadable. 
Es werden jedoch keine Updates folgen.
> Der Hintergrundgedanken beim MenuCalc von Marc ist es, der Lebensmittelverschwendung
> den Kampf anzusagen und dadurch einen Beitrag zur Nachhaltigkeit in Haushalten
> zu liefern.

Danke an die Dozierenden und Mitstudierenden, welche mich auf dem Weg unterstützt haben.
