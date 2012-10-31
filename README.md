e2openplugin-InfoBarTunerState
==============================

Enigma2 Plugin: Show the tuner states as infobar popup

Features:
Das Plugin soll die InfoBar ergänzen und alle aktuellen Aufnahmen übersichtlich darstellen. Schaut euch einfach die Screenshots an, die sagen ja bekanntlich mehr aus als ...

Jede Zeile enthält standardmässig folgende Informationen:
Icon - Tuner - Sender-Nummer - Sender-Name - Name - Grafischer Fortschrittsbalken - Verbleibende Zeit / Dauer - Streaming Client

Ist alles frei einstellbar!

Die Informationen werden mit der InfoBar ein- und ausgeblendet
Wenn ein Timer startet oder beendet wurde, werden die Informationen angezeigt, es sei den es ist gerade ein Dialog oder Screen aktiv
Die Dauer der Einblendung ist an die E2 Einstellung der InfoBar gekoppelt

Die Einträge werden nun sortiert dargestellt:
- Zuerst nach dem Typ: Laufende Aufnahmen, Fertige Aufnahmen
- Danach nach der verbleibenden Zeit: Aufsteigend

Umschalt Timer werden ignoriert

Laufende Aufnahmen:
Werden mit einem roten Aufnahme-Icon markiert
Die verbleibende Zeit wird automatisch beim Anzeigen aktualisiert
Wird die Aufnahmedauer oder der Endzeitpunkt einer Aufnahme geändert, wird die Anzeige aktualisiert
Für zeitlich unbegrenzte Aufnahmen wird für die verbleibende Zeit das Undendlich-Symbol dargestellt

Sofortaufnahmen mit Aufnahmedauer oder Endzeit:
E2 startet zuerst eine unbegrenzte Aufnahme und ändert dann die Dauer entsprechend, deswegen wird auch zuerst eine zeitlich unbegrenzte Aufnahme dargestellt, die dann aktualisiert wird.

Beendete Aufnahmen:
Werden mit einem grünen Häckchen markiert
Es wird die Aufnahmedauer angezeigt

Streaming:
TBD

Config:
über Erweiterungsmenü (Plugins nicht Extensions) erreichbar
- Aktivieren (Neustart notwendig)
- Add to extension menu:
Bei Aufruf wird IBTS angezeigt
Dauer entspricht dem E2 InfoBar TimeOut (0 ist nicht zulässig, da keine Tasten zugeordnet sind, daher werden 5 Sekunden verwendet)
Wenn kein Event aktiv ist: Info PopUp: Nothing running in IBTS style
Wenn IBTS deaktiviert ist: MessageBox
- Mit InfoBar anzeigen
- Nach Events anzeigen (Aufnahme startet / beendet) ohne InfoBar
- MoviePlayer Integration ist standardmäßig aus, kann jedoch ohne Neustart anktiviert werden. Grund: Teile der InfoBar müssen überschrieben werden.
- Datumsformat wählbar: "HH:MM", "DD.MM HH:MM", "MM/DD HH:MM", "DD.MM.YYYY HH:MM", "YYYY/MM/DD HH:MM"
- Anzahl Aufnahmen = maximale Anzahl beendeter Aufnahmen in der Liste (FIFO, sortiert nach dem Timerende)
- TimeOut Aufnahmen = Maximale Zeit in Sekunden, die eine beendete Aufnahme in der Liste bleibt (0 verbleibt solange bis die maximale Anzahl erreicht ist)
-> Je nach dem was zuerst erreicht wird (Anzahl oder TimeOut), wird ein Eintrag entfernt
- Field Config
- Horizontal Offset: Der Skin kann zusätzlich horizontal verschoben werden
- Vertical Offset: Der Skin kann zusätzlich vertikal verschoben werden
- Content Offset: Linker Abstand des Textes
Background transparency:
E2-Einstellungen:
- Dauer der InfoBar Einblendung
- Benachrichtigung wenn Aufnahmen starten einblenden

Alle Einstellungen können ohne Neustart übernommen werden!

Infofelder:
Type (Icon)
Type (Text)
Tuner
Tuner Type
Channel Number
Channel Name
Name
Time Left / Duration
Time Left
Time Elapsed
Begin
End
Duration
Timer Progress (Graphical)
Timer Progress (Text)
Destination
Stream Client
Destination / Client
File Size
Free Space
None

Skin:
Die Spaltenbreite und Hintergrund wird dynamisch angepasst.
Der Skin definiert immer nur eine Zeile!

Sonstiges:
Die InfoBar wird mit den Standard-Einstellungen nicht überschrieben.
Das Plugin sollte also mit jedem Image funktionieren und keine Inkompatibilitäten mit anderen Plugins aufweisen.
Das Plugin ist so geschrieben, dass keine Eingaben / Dialoge / Screens blockiert werden sollten.

Setup:
Einfach das IPKG installieren und neustarten.

Experience:
Wenn die InfoBarTunerState trotz laufenden Aufnahmen nicht angezeigt wird, kann es sein das die InfoBar eures Skins die InfoBarTunerState verdeckt, dann erhöht die InfoBarTunerState zPosition im Skin.

ChangeLog:
1.0
Workaround für Textlängenberechnung eingebaut
Streaming Anzeige ist vorerst deaktiviert, da es noch an das OpenWebIf angepasst werden muss.

0.9.6.2
Movie Player Problem behoben
Configscreen: Wenn IBTS deaktiviert wird, werden die Optionen ausgeblendet

0.9.6.1
Autostart Problem behoben

0.9.6
Extension-Menü Eintrag kann dazugeschaltet werden
Abhängigkeiten überarbeitet

0.9.5
Alle Abhängigkeiten werden jetzt beim installieren beachtet.
D.h. beim Installieren werden das WebIf und der StreamProxy auf den richtigen Stand gebracht.

0.9.4
Bugfix: Zeitlich unbegrenzte Timer weren richtig dargestellt

0.9.3
Bugfix: IBTS wird nach einem Neustart nicht mit der InfoBar angezeigt
Bugfix: Extensionmenü Eintrag konnte nicht hinzugefügt werden
Die Streaming Client IP wird jetzt direkt über das neue WebIf ermittelt
Verwendet bitte das neue WebIf 1.7 (>28.12.2011)

0.9.2
Neue Option: Streams können versteckt werden
Bugfix: Hintergrundtransparenz
Bugfix: IBTS wird nun immer automatisch geschlossen, wenn ein Timer startet während man eine Aufnahme schaut

0.9.1
Bugfix: Skin: IBTS zeigte keinen Text

0.9.0
Streaming Interface an neues WebIf angepasst
Locale support, wer will Übersetzungen liefern?
Code Cleanup
Config: neues Feld: StreamClient with Port
Bugfix: IBTS wurde in verschiedenen Szenarien nicht mehr ausgeblendet
Von 0.8.x auf 0.9 sind keine Änderungen am Skin notwendig.
Bei Problemen mit Überlagerungen ändert die IBTS zPosition eures Skins oder wendet euch an den Skinner, die dürfen sich auch gerne bei mir melden.
Grundsätzlich sollte es keine Probleme geben, wenn IBTS die gleiche zPosition wie die InfoBar hat.

0.8.4 Patch
Bugfix: WebIf Streaming

0.8.3 Patch
Bugfix: Wiederholdende Timeraufnahmen wurden nicht als beendet markiert

0.8.2 Patch
Config Spacing Offset Parameter
Bugfix: getTuner is None check
Bugfix: Anzeige der beendeten Aufnahmen mit TimeOut 0

0.8.1 Patch
Bugfix: Tuner A wird nicht dargestellt
Bugfix: Wenn "Show on events" auf "Nein" gestellt wird, dann werden keine Aufnahmen dargestellt

0.8
LiveTV Stream Anzeige
Beendete Streams werden wie beendete Filme je nach Einstellung aufgelistet
Fortschrittsbalken für Aufnahmen
Icon und Fortschritsbalken können als Feld ausgewählt werden
- Eine doppelte Auswahl ist nicht erlaubt und wird beim Beenden geprüft
Unbegrenzte Aufnahmen haben keine Dauer, keine Restlaufzeit und keinen Fortschrittsbalken
Neue Felder:
Tuner Type: DVB-S, DVB-C, ...
Stream Client: Name des Clients. Wenn der Name nicht ermittelt werden kann, wird die IP dargestellt.
Geänderte Felder:
Begin, End, Duration: Wird auch für Streams berechnet
Kombinierte Felder:
Time Left / Duration: Während der Aufnahme: Verbleibende Zeit, danach: Gesamtzeit
Destination / Client: Für Aufnahmen: Aufnahmeordner, für Streams: Client Rechner
Skin Änderungen:
Optionaler Parameter screen padding: Abstand zum linken Rand
Optionaler Parameter screen spacing: Abstand zwischen den Elementen
widget name="Type" ist nun ein MultiPixmap
widget name="Progress"
Neue PNGs Stream und Info
ProgressBar wird innerhalb der Zeile vertikal zentriert.
backgroundColor="#ffrrggbb" ff wird wegen der Transparenz benötigt
Config Änderungen:
Horizontal Offset, Vertical Offset, Content Offset, Add to extension menu, Background transparency
Bugfix: Timer blocking weiter minimiert, liegt an den lokalen timer und iRecordableService Objekt Kopien
Bugfix: Berechnung der Kanalnummer bei langen Kanallisten verursachte Verzögerungen der InfoBar Anzeige
Bugfix: getTuner
Danke Zombi für das Streaming Icon

Einmaliger Aufruf in das extendedPluginMenü (IBTS wird ohne InfoBar eingeblendet)
Funktioniert auch mit dem MultiQuickButton Plugin (Dafür muss die Option Extension Menü nicht an sein)
Funktioniert auch im Extension Menü des EnhancedMovieCenter Players

0.7
Config:
Plugin kann ohne Neustart aktiviert/deaktiviert werden
Felder können einzeln konfiguriert werden (D.h. Felder können ein-/ausgeblendet und umsortiert werden)
Das Icon ist immer fix
Zu den bestehenden Infofeldern:
Tuner, Channel Number, Channel Name, Name, Time Left
Kommen folgende Infofelder dazu:
- Time Elapsed, Timer Begin, Timer End, Timer Duration, Destination, File Size, Free Space
Das Datum-/Zeitformat für Timer Begin / End kann eingestellt werden
Sonstiges: Bei zeitlich unbegrenzten Aufnahmen wird der Name nicht mehr aktualisiert (E2 benennt die Datei auch nicht um)
Für die neuen Features waren einige Skin Änderungen notwendig

0.6
MoviePlayer Integration
Config:
MoviePlayer Integration ist standardmäßig aus, kann jedoch ohne Neustart anktiviert werden. Grund: Teile der InfoBar müssen überschrieben werden
Voreingestellte Anzahl beendeter Timer ist nun 5
Bugfix: Text: Enable InfoBarTunerState
Bugfix: Wiederholende Timer blockieren nach der Aufnahme die Tuner nicht mehr
Bugfix: Wiederholende Timer werden nach der Aufnahme als Beendet markiert

0.5
Für beendete Aufnahmen wird nun die Aufnahmedauer angezeigt
IPKG-Release (Danke für die Anleitung coolman)
Skin: zPosition erhöht auf 5 wegen Inkompatibilität mit der InfoBar in manchen Skins (Danke für deine Tests Joachim_Ernst mit Skin Infinity HD)
Skin: InfoBarTunerState Position angepasst, wegen des Lautstärkebalkens (Danke für den Hinweis Zombi mit Skin HD1R3)
ConfigScreen über Erweiterungsmenü (Plugins nicht Extensions) erreichbar
- Aktivieren (Neustart notwendig)
- Mit InfoBar anzeigen
- Nach Events anzeigen (Aufnahme startet / beendet) ohne InfoBar
- Anzahl Aufnahmen = maximale Anzahl beendeter Aufnahmen in der Liste (FIFO, sortiert nach dem Timerende)
- TimeOut Aufnahmen = Maximale Zeit in Sekunden, die eine beendete Aufnahme in der Liste bleibt (0 verbleibt solange bis die maximale Anzahl erreicht ist)
-> Je nach dem was zuerst erreicht wird, wird ein Eintrag entfernt
Bugfix: InfoBarTunerState wurde zu früh ausgeblendet, wenn die InfoBar eingeblendet wurde und der Benutzer dann auf einen anderen Kanal zappt

0.4
Skin Änderungen
-nach links verschoben
-neuer Hintergrund
-zPosition erhöht wegen InfoBar Skin Inkompatibilitäts Problemen
Intern: eTimer überarbeitet
Bugfix: Einträge werden nun korrekt nach einer Minute entfernt
Bugfix: Bei Aufnahmen, die vor dem Pluginstart, begonnen haben, fehlte die Kanalnummer

0.3
Fertige Aufnahmen haben jetzt ein grünes Häkchen
Fertige Aufnahmen verbleiben für 1 Minute in der Liste, man hat also genügend Zeit die InfoBar nochmals zu öffnen.
Für fertige Aufnahmen wird für den Tuner ein Platzhalter "-" eingeblendet, der Tuner ist ja auch bereits freigegeben
Die Hintergrundbreite wird dynamisch angepasst
Die Einträge werden nun sortiert dargestellt:
- Zuerst nach dem Typ: Laufende Aufnahmen, Fertige Aufnahmen
- Danach nach der verbleibenden Zeit: Aufsteigend
Wird die Aufnahmedauer oder der Endzeitpunkt eines Timers geändert, wird die Anzeige sofort aktualisiert
(Wenn etwas anderes geändert wird, wird die laufende Aufnahme beendet und eine neue gestartet)
Bei zeitlich unbegrenzten Aufnahmen wird der Title automatisch aktualisiert (betrifft nur die Anzeige)
Umschalt Timer werden ignoriert
Bugfix: Anzeigefehler Direkt-Aufnahme mit Aufnahmelänge behoben
Bugfix: Infobar Anzeigedauer ohne TimeOut, InfoBarTunerState bleibt angezeigt bis die InfoBar geschlossen wird
Bugfix: Aufnahmen die gestartet wurden, bevor das Plugin geladen wurde, wurden nicht gelistet.

0.2
Unnötige Events entfernt (Sollte die Meldung: "Keine freier Tuner verfügbar" verhindern)
Fertige Aufnahmen werden noch ein letztes Mal in der Liste angezeigt und dann erst entfernt: grünes Stop Symbol
Fertige Aufnahmen haben als verbleibende Zeit ein "-"

0.1
Laufende Aufnamen werden mit Icon, Tuner, Kanalnummer, Sendername, Titel und ihrer verbleibende Zeit eingeblendet
Die verbleibende Zeit wird automatisch beim Anzeigen aktualisiert.
Für zeitlich unbegrenzte Aufnahmen wird für die verbleibende Zeit das Undendlich-Symbol dargestellt.
Die Informationen werden immer mit der InfoBar ein- und ausgeblendet.
Wenn ein Timer startet oder beendet wurde, werden die Informationen angezeigt, es sei den es ist gerade ein Dialog oder Screen aktiv.
Die Dauer der Einblendung ist an die E2 Einstellung der InfoBar gekoppelt.
Die Spaltenbreite wird dynamisch angepasst.
Transparenter Hintergrund

Known Bugs:
Wenn eine MoviePlayer Integration aktiviert ist, kann die LiveTV InfoBar Integration nicht ausgeschalten werden
Bei events kann es zu Screen Überlagerungen kommen.
Wenn ein Skin eine tranparente Fullscreen InfoBar verwendet, kann IBTS überlagert werden (zPosition>5)
Bei Problemen mit Überlagerungen ändert die IBTS zPosition eures Skins oder meldet euch bei euren Skin-Erstellern, die dürfen sich auch gerne an mich wenden.
Wenn ein Sender mehreren Bouquets zugeordnet ist, gibt es keine Möglichkeit herauszufinden welcher Sender gemeint ist, es wird dann der erste Treffer und dessen Sendernummer verwendet.