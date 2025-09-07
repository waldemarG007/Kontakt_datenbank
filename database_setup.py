import sqlite3

def setup_database(db_file='contacts.db'):
    """Erstellt die Datenbank und die erforderlichen Tabellen."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Tabelle für Kontakte
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        address TEXT,
        phone_number TEXT,
        email TEXT NOT NULL UNIQUE
    )
    ''')

    # Tabelle für gesperrte E-Mail-Adressen
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS blacklisted_emails (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL UNIQUE
    )
    ''')

    # Tabelle für gesperrte Provider
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS blacklisted_providers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        provider_domain TEXT NOT NULL UNIQUE
    )
    ''')

    # Tabelle für unerreichbare E-Mail-Adressen
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS unreachable_emails (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL UNIQUE
    )
    ''')

    # --- Tabellen für Kampagnen-Modul ---

    # Tabelle zur Verwaltung von Kampagnen
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS campaigns (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        creation_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        status TEXT NOT NULL DEFAULT 'active' -- z.B. active, archived
    )
    ''')

    # Zuordnungstabelle zwischen Kampagnen und Kontakten
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS campaign_contacts (
        campaign_id INTEGER NOT NULL,
        contact_id INTEGER NOT NULL,
        FOREIGN KEY (campaign_id) REFERENCES campaigns (id),
        FOREIGN KEY (contact_id) REFERENCES contacts (id),
        PRIMARY KEY (campaign_id, contact_id)
    )
    ''')

    # Protokolltabelle für Änderungen innerhalb einer Kampagne
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS campaign_audits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        campaign_id INTEGER NOT NULL,
        contact_id INTEGER NOT NULL,
        field_name TEXT NOT NULL,
        old_value TEXT,
        new_value TEXT,
        change_timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        is_applied INTEGER NOT NULL DEFAULT 0, -- 0 for false, 1 for true
        FOREIGN KEY (campaign_id) REFERENCES campaigns (id),
        FOREIGN KEY (contact_id) REFERENCES contacts (id)
    )
    ''')

    conn.commit()
    conn.close()
    print("Datenbank und Tabellen erfolgreich erstellt.")

if __name__ == '__main__':
    setup_database()
