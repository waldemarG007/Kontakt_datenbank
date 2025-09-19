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
| 16. Datenbank-Schema für Kampagnen entwerfen und implementieren (`campaigns`, `campaign_contacts`, `campaign_audits`).                  |   ✅   |
| **Kampagnen-Modul (Phase 2: Backend)**                                                                                               |        |
| 17. Backend-Funktionen für die Kampagnen-Verwaltung implementieren (`create_campaign`, `get_all_campaigns`, etc.).                      |   🔄   |
| 18. Backend-Logik für Änderungsprotokollierung und Daten-Rekonstruktion implementieren.                                                |   📋   |
| 19. Backend-Logik für die Synchronisation von Kampagnen-Änderungen implementieren.                                                     |   📋   |
| 20. Unit-Tests für die neuen Kampagnen-Funktionen erstellen.                                                                           |   📋   |
| **Kampagnen-Modul (Phase 3: GUI)**                                                                                                   |        |
| 21. GUI um einen Kampagnen-Tab erweitern.                                                                                              |   📋   |
| 22. GUI-Ansicht für die Interaktion innerhalb einer Kampagne implementieren.                                                           |   📋   |
| **Follow-Up-Funktion (Phase 4)**                                                                                                     |        |
| 23. Datenbank und Backend für Follow-Ups erweitern.                                                                                    |   📋   |
| 24. GUI für die Verwaltung von Follow-Ups implementieren.                                                                              |   📋   |
