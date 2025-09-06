# Kontakt-Datenbank

Dies ist ein einfaches Python-Konzept für eine Kontakt-Datenbankanwendung, die über eine Kommandozeile (CLI) bedient wird.

## Funktionen

- **Kontaktverwaltung**: Hinzufügen neuer Kontakte (Vorname, Nachname, Adresse, Telefon, E-Mail).
- **Duplikaterkennung**: Verhindert das Hinzufügen von Kontakten mit identischem Namen und E-Mail-Adresse.
- **Blacklisting**:
    - Sperren einzelner E-Mail-Adressen.
    - Sperren ganzer E-Mail-Provider (z.B. `@spam.com`).
- **Liste für unerreichbare E-Mails**: Führt eine separate Liste von E-Mail-Adressen, die sich als unerreichbar erwiesen haben.
- **Datenpersistenz**: Nutzt eine SQLite-Datenbank (`contacts.db`) zur Speicherung der Daten.

## Einrichtung

Um die Anwendung zum ersten Mal einzurichten, muss die Datenbankdatei erstellt werden. Führen Sie dazu das folgende Skript aus:

```bash
python database_setup.py
```
Dadurch wird die Datei `contacts.db` im Projektverzeichnis mit allen erforderlichen Tabellen erstellt.

## Anwendung starten

Um die Kommandozeilen-Anwendung zu starten, führen Sie das Hauptskript aus:

```bash
python contact_db.py
```
Sie werden durch ein Menü geführt, über das Sie alle Funktionen der Anwendung nutzen können.

## Tests ausführen

Das Projekt enthält Unit-Tests, um die Kernfunktionalität zu überprüfen. Um die Tests auszuführen, verwenden Sie den folgenden Befehl:

```bash
python -m unittest test_contact_db.py
```
Die Tests werden auf einer separaten Test-Datenbank ausgeführt und beeinflussen nicht die Haupt-Datenbank `contacts.db`.