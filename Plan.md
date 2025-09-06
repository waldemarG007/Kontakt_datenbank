# Entwicklungsplan

Dies ist der ursprüngliche Plan, der für die Entwicklung des Kontakt-Datenbank-Konzepts verwendet wurde.

1.  **Datenbank einrichten.** Ich werde das in Python integrierte `sqlite3`-Modul verwenden, um eine einfache, serverlose Datenbank zu erstellen. Ich erstelle ein Skript, das die erforderlichen Tabellen einrichtet: `contacts`, `blacklisted_emails`, `blacklisted_providers` und `unreachable_emails`.
2.  **Implementierung der Kernlogik für die Kontaktverwaltung.** Ich werde eine Hauptanwendungsdatei erstellen, nennen wir sie `contact_db.py`. Diese Datei wird eine `Contact`-Klasse und Funktionen zur Interaktion mit der Datenbank enthalten.
3.  **Implementierung der Funktion "Kontakt hinzufügen" mit Duplikaterkennung.** Diese Funktion nimmt die Kontaktdaten entgegen, prüft auf Duplikate (basierend auf einer Kombination aus Name und E-Mail) und fügt den Kontakt zur Datenbank hinzu, wenn es sich nicht um ein Duplikat handelt.
4.  **Implementierung der Blacklisting-Funktionalität.** Vor dem Hinzufügen eines neuen Kontakts prüft das System, ob die E-Mail-Adresse oder ihr Anbieter auf den entsprechenden Blacklists stehen.
5.  **Implementierung der Liste für unerreichbare E-Mails.** Ich werde eine Funktion erstellen, um eine E-Mail zur Liste der "Unerreichbaren" hinzuzufügen.
6.  **Erstellung einer einfachen Befehlszeilenschnittstelle (CLI).** Dies wird ein einfaches Menü im Hauptskript sein, um die Funktionen zu demonstrieren: Hinzufügen eines Kontakts, Suchen nach einem Kontakt und Anzeigen der Listen.
7.  **Hinzufügen von Tests.** Ich werde eine separate Testdatei erstellen, um Unit-Tests für die Kernfunktionalitäten zu schreiben und sicherzustellen, dass sie wie erwartet funktionieren.
