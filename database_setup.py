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

    conn.commit()
    conn.close()
    print("Datenbank und Tabellen erfolgreich erstellt.")

if __name__ == '__main__':
    setup_database()
