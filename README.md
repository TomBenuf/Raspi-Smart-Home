Tom Barnowsky, Nils Rothenburger, Robin Schmidt - 2018-11-14
Netzwerkgestützte Smart-Home Steuerung via Raspberry Pi

---------------------- RASPI-SMART-HOME-README ----------------------------

This project's documentation and all code remarks are written in German.
For english information contact tom-barnowsky@hls-anlagenbau.de

Das Projekt arbeitet an einer über ein Webinterface gesteuerten Smart-Home
Lichtsteuerung. Keine Weltneuheit, ich weiß, aber lasst uns einfach unseren
Spaß und schickt uns nicht zu einem bestehenden Projekt, das Probleme mit
denen wir uns herumschlagen schon gelöst hat.
Unser Projekt entsteht im Rahmen eines Schulprojekts am BSZ Pirna.

Es gibt der Übersichtlichkeit wegen zwei Ordner. Einen für Python Backend
den anderen für HTML/PHP/CSS Frontend. Der main.py Script liest aus
der status.xml und gibt an die in <signal> festgelegten GPIO Pins das
in <status> bestimmte Signal (an/aus). Dieser Script wird auf der Raspberry
Pi dank Cronjob immer ausgeführt.
Die index.php lässt den Nutzer, solange er im Heimnetzwerk ist, das Smart-
Home System steuern. Es gibt nach Eingabe eines Passworts ein Menü um
die Namen und Reihenfolge der Schaltflächen auf der Website zu verändern.
Wenn Schaltflächen oder Namen geändert werden wird dies in status.xml
geschrieben so dass main.py die entsprechende Aktion ausführt.
Auch Personalisierung im Webinterface wird in der status.xml gespeichert
so dass es auch beim nächsten Aufruf geladen wird.

Alles weitere wird von einer Schaltung gelöst die, wenn die GPIO pins
geschalten werden, mit einem Tyristor 220V Wechselspannung schaltet und
eine Status LED zum Leuchten bringt.
Schaltpläne etc. werden nicht auf GitHub veröffentlicht.

Wer Interesse an weiteren Informationen oder Schaltplänen hat
bitte tom-barnowsky@hls-anlagenbau.de kontaktieren.

Danke fürs Lesen.
