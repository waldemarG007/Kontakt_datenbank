# Entwicklungsplan

Dieser Plan dokumentiert die Entwicklung des Kontakt-Datenbank-Konzepts.

| Aufgabe                                                                                                                              | Status |
| ------------------------------------------------------------------------------------------------------------------------------------ | :----: |
| **Kernanwendung (CLI)**                                                                                                              |        |
| 1. Datenbank einrichten und Tabellen erstellen.                                                                                      |   ✅   |
| 2. Kernlogik für die Kontaktverwaltung implementieren.                                                                               |   ✅   |
| 3. Funktion "Kontakt hinzufügen" mit Duplikaterkennung implementieren.                                                               |   ✅   |
| 4. Blacklisting-Funktionalität implementieren.                                                                                       |   ✅   |
| 5. Liste für unerreichbare E-Mails implementieren.                                                                                   |   ✅   |
| 6. Eine einfache Befehlszeilenschnittstelle (CLI) erstellen.                                                                         |   ✅   |
| 7. Unit-Tests für die Kernfunktionalitäten hinzufügen.                                                                               |   ✅   |
| **Dokumentation & GUI**                                                                                                              |        |
| 8. `README.md`, `Plan.md` und `AGENTS.md` erstellen und befüllen.                                                                    |   ✅   |
| 9. GUI-Grundstruktur mit Tkinter erstellen.                                                                                          |   ✅   |
| 10. GUI-Widgets und Layout implementieren.                                                                                           |   ✅   |
| 11. GUI mit der Backend-Logik verbinden und Benutzer-Feedback einbauen.                                                                |   ✅   |
| **Zukünftige Features**                                                                                                              |        |
| 12. **Kontakte bearbeiten und löschen:** GUI erweitern, um Kontakte zu ändern oder zu löschen.                                        |   ✅   |
| 13. **Einträge aus Listen entfernen:** Funktion zum Löschen von E-Mails/Providern aus den Blacklists/Unerreichbar-Listen hinzufügen. |   ✅   |
| 14. **Such- und Filterfunktion:** Eine Suchleiste in der GUI implementieren, um die Kontaktliste zu filtern.                           |   ✅   |
| 15. **Allgemeine GUI-Verbesserungen:** Kleinere Optimierungen am Layout und der Benutzerführung.                                      |   ✅   |
| **Kampagnen-Modul (Phase 1: Datenbank)**                                                                                             |        |
| 16. Datenbank-Schema für Kampagnen entwerfen und implementieren (`campaigns`, `campaign_contacts`, `campaign_audits`).                  |   🔄   |
