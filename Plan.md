# Entwicklungsplan

Dieser Plan dokumentiert die Entwicklung des Kontakt-Datenbank-Konzepts.

## Kernanwendung (CLI)

1.  **[Done] Datenbank einrichten.** Das in Python integrierte `sqlite3`-Modul verwenden, um eine einfache, serverlose Datenbank zu erstellen. Ein Skript erstellen, das die erforderlichen Tabellen einrichtet.
2.  **[Done] Implementierung der Kernlogik für die Kontaktverwaltung.** Eine Hauptanwendungsdatei `contact_db.py` erstellen, die eine `Contact`-Klasse und Funktionen zur Interaktion mit der Datenbank enthält.
3.  **[Done] Implementierung der Funktion "Kontakt hinzufügen" mit Duplikaterkennung.** Eine Funktion, die Kontaktdaten entgegennimmt, auf Duplikate prüft und den Kontakt zur Datenbank hinzufügt.
4.  **[Done] Implementierung der Blacklisting-Funktionalität.** Vor dem Hinzufügen eines neuen Kontakts prüfen, ob die E-Mail-Adresse oder ihr Anbieter auf den entsprechenden Blacklists stehen.
5.  **[Done] Implementierung der Liste für unerreichbare E-Mails.** Eine Funktion erstellen, um eine E-Mail zur Liste der "Unerreichbaren" hinzuzufügen.
6.  **[Done] Erstellung einer einfachen Befehlszeilenschnittstelle (CLI).** Ein Menü im Hauptskript, um die Funktionen zu demonstrieren.
7.  **[Done] Hinzufügen von Tests.** Eine separate Testdatei erstellen, um Unit-Tests für die Kernfunktionalitäten zu schreiben.

## GUI-Entwicklung

8.  **[Done] GUI-Struktur entwerfen:** Eine neue Datei, `gui.py`, erstellen und das Hauptfenster der Anwendung mit Tkinter entwerfen.
9.  **[Done] Funktionen anbinden:** Die bestehenden Funktionen aus `contact_db.py` importieren und sie mit den GUI-Elementen verknüpfen.
10. **[Done] Feedback für den Benutzer:** Mechanismen einbauen, um dem Benutzer Feedback zu geben (z.B. über Pop-up-Nachrichten).
