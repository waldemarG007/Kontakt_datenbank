import sqlite3
from typing import Optional

DATABASE_FILE = 'contacts.db'

def get_db_connection():
    """Stellt eine Verbindung zur Datenbank her und gibt das Verbindungsobjekt zurück."""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

class Contact:
    """Repräsentiert einen Kontakt in der Datenbank."""
    def __init__(self, first_name: str, last_name: str, email: str, address: Optional[str] = None, phone_number: Optional[str] = None, id: Optional[int] = None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.phone_number = phone_number
        self.email = email

    def __repr__(self):
        return f"<Contact({self.id}, {self.first_name} {self.last_name}, {self.email})>"

    def __eq__(self, other):
        if not isinstance(other, Contact):
            return NotImplemented
        return self.first_name == other.first_name and \
               self.last_name == other.last_name and \
               self.email == other.email

def add_contact(contact: Contact) -> tuple[bool, str]:
    """
    Fügt einen neuen Kontakt zur Datenbank hinzu, nachdem auf Blacklist und Duplikate geprüft wurde.
    Gibt ein Tupel zurück: (Erfolg, Nachricht).
    """
    # 1. Auf Blacklist prüfen
    if is_blacklisted(contact.email):
        return (False, f"Fehler: Die E-Mail-Adresse '{contact.email}' oder ihr Provider ist gesperrt.")

    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Auf Duplikate prüfen (gleicher Vorname, Nachname und E-Mail)
    cursor.execute(
        "SELECT id FROM contacts WHERE lower(first_name) = ? AND lower(last_name) = ? AND lower(email) = ?",
        (contact.first_name.lower(), contact.last_name.lower(), contact.email.lower())
    )
    existing_contact = cursor.fetchone()

    if existing_contact:
        conn.close()
        return (False, "Fehler: Ein Kontakt mit diesem Namen und dieser E-Mail-Adresse existiert bereits.")

    # 2. Kontakt einfügen
    try:
        cursor.execute(
            "INSERT INTO contacts (first_name, last_name, address, phone_number, email) VALUES (?, ?, ?, ?, ?)",
            (contact.first_name, contact.last_name, contact.address, contact.phone_number, contact.email)
        )
        conn.commit()
        contact.id = cursor.lastrowid
        message = f"Kontakt '{contact.first_name} {contact.last_name}' erfolgreich hinzugefügt."
        success = True
    except sqlite3.IntegrityError:
        # Dies fängt den Fall ab, dass die E-Mail bereits existiert (UNIQUE constraint),
        # was durch die obige Prüfung eigentlich schon abgedeckt sein sollte, aber als Fallback dient.
        message = f"Fehler: Die E-Mail-Adresse '{contact.email}' existiert bereits."
        success = False
    finally:
        conn.close()

    return (success, message)


def add_email_to_blacklist(email: str) -> tuple[bool, str]:
    """Fügt eine E-Mail-Adresse zur Blacklist hinzu."""
    conn = get_db_connection()
    try:
        conn.execute("INSERT INTO blacklisted_emails (email) VALUES (?)", (email.lower(),))
        conn.commit()
        return (True, f"E-Mail '{email}' zur Blacklist hinzugefügt.")
    except sqlite3.IntegrityError:
        return (False, "Diese E-Mail ist bereits auf der Blacklist.")
    finally:
        conn.close()

def add_provider_to_blacklist(provider_domain: str) -> tuple[bool, str]:
    """Fügt einen E-Mail-Provider zur Blacklist hinzu."""
    conn = get_db_connection()
    domain = provider_domain.lower().replace('@', '')
    try:
        conn.execute("INSERT INTO blacklisted_providers (provider_domain) VALUES (?)", (domain,))
        conn.commit()
        return (True, f"Provider '{domain}' zur Blacklist hinzugefügt.")
    except sqlite3.IntegrityError:
        return (False, "Dieser Provider ist bereits auf der Blacklist.")
    finally:
        conn.close()

def is_blacklisted(email: str) -> bool:
    """Prüft, ob eine E-Mail-Adresse oder ihr Provider auf der Blacklist steht."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Prüfen, ob die genaue E-Mail-Adresse auf der Blacklist steht
    cursor.execute("SELECT id FROM blacklisted_emails WHERE email = ?", (email.lower(),))
    if cursor.fetchone():
        conn.close()
        return True

    # 2. Prüfen, ob der Provider auf der Blacklist steht
    try:
        provider = email.split('@')[1]
        cursor.execute("SELECT id FROM blacklisted_providers WHERE provider_domain = ?", (provider.lower(),))
        if cursor.fetchone():
            conn.close()
            return True
    except IndexError:
        # Ungültige E-Mail-Adresse ohne '@'
        pass

    conn.close()
    return False

def add_email_to_unreachable_list(email: str) -> tuple[bool, str]:
    """Fügt eine E-Mail-Adresse zur Liste der unerreichbaren E-Mails hinzu."""
    conn = get_db_connection()
    try:
        conn.execute("INSERT INTO unreachable_emails (email) VALUES (?)", (email.lower(),))
        conn.commit()
        return (True, f"E-Mail '{email}' zur Liste der unerreichbaren E-Mails hinzugefügt.")
    except sqlite3.IntegrityError:
        return (False, "Diese E-Mail ist bereits als unerreichbar markiert.")
    finally:
        conn.close()

def get_all_contacts() -> list[Contact]:
    """Gibt alle Kontakte aus der Datenbank zurück."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts ORDER BY last_name, first_name")
    contacts = [Contact(**dict(row)) for row in cursor.fetchall()]
    conn.close()
    return contacts

def get_blacklisted_emails() -> list[str]:
    """Gibt alle E-Mails auf der Blacklist zurück."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM blacklisted_emails ORDER BY email")
    emails = [row['email'] for row in cursor.fetchall()]
    conn.close()
    return emails

def get_blacklisted_providers() -> list[str]:
    """Gibt alle Provider-Domains auf der Blacklist zurück."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT provider_domain FROM blacklisted_providers ORDER BY provider_domain")
    domains = [row['provider_domain'] for row in cursor.fetchall()]
    conn.close()
    return domains

def search_contacts(query: str) -> list[Contact]:
    """Sucht nach Kontakten, deren Vorname, Nachname oder E-Mail den Suchbegriff enthalten."""
    conn = get_db_connection()
    cursor = conn.cursor()
    search_term = f"%{query.lower()}%"
    cursor.execute(
        """SELECT * FROM contacts
           WHERE lower(first_name) LIKE ?
              OR lower(last_name) LIKE ?
              OR lower(email) LIKE ?
           ORDER BY last_name, first_name""",
        (search_term, search_term, search_term)
    )
    contacts = [Contact(**dict(row)) for row in cursor.fetchall()]
    conn.close()
    return contacts

def get_contact_by_id(contact_id: int) -> Optional[Contact]:
    """Holt einen einzelnen Kontakt anhand seiner ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Contact(**dict(row))
    return None

def get_unreachable_emails() -> list[str]:
    """Gibt alle als unerreichbar markierten E-Mails zurück."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM unreachable_emails ORDER BY email")
    emails = [row['email'] for row in cursor.fetchall()]
    conn.close()
    return emails

def update_contact(contact: Contact) -> tuple[bool, str]:
    """Aktualisiert einen bestehenden Kontakt in der Datenbank."""
    if not contact.id:
        return (False, "Fehler: Kontakt-ID für Update nicht vorhanden.")

    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        # Prüfen, ob die neue E-Mail-Adresse bereits von einem ANDEREN Kontakt verwendet wird.
        cursor.execute(
            "SELECT id FROM contacts WHERE lower(email) = ? AND id != ?",
            (contact.email.lower(), contact.id)
        )
        if cursor.fetchone():
            return (False, f"Fehler: Die E-Mail-Adresse '{contact.email}' wird bereits von einem anderen Kontakt verwendet.")

        cursor.execute(
            """UPDATE contacts SET
                first_name = ?,
                last_name = ?,
                address = ?,
                phone_number = ?,
                email = ?
            WHERE id = ?""",
            (contact.first_name, contact.last_name, contact.address, contact.phone_number, contact.email, contact.id)
        )
        conn.commit()
        if cursor.rowcount == 0:
            return (False, f"Fehler: Kein Kontakt mit ID {contact.id} gefunden, um ihn zu aktualisieren.")
        return (True, f"Kontakt '{contact.first_name} {contact.last_name}' erfolgreich aktualisiert.")
    except sqlite3.IntegrityError:
        return (False, f"Fehler: Die E-Mail-Adresse '{contact.email}' existiert bereits.")
    except Exception as e:
        return (False, f"Ein Fehler ist aufgetreten: {e}")
    finally:
        conn.close()

def delete_contact(contact_id: int) -> tuple[bool, str]:
    """Löscht einen Kontakt anhand seiner ID aus der Datenbank."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return (False, f"Fehler: Kein Kontakt mit ID {contact_id} gefunden.")
        return (True, f"Kontakt mit ID {contact_id} erfolgreich gelöscht.")
    except Exception as e:
        return (False, f"Ein Fehler ist aufgetreten: {e}")
    finally:
        conn.close()

def delete_email_from_blacklist(email: str) -> tuple[bool, str]:
    """Löscht eine E-Mail von der Blacklist."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM blacklisted_emails WHERE email = ?", (email.lower(),))
        conn.commit()
        if cursor.rowcount == 0:
            return (False, f"Fehler: E-Mail '{email}' nicht auf der Blacklist gefunden.")
        return (True, f"E-Mail '{email}' erfolgreich von der Blacklist entfernt.")
    except Exception as e:
        return (False, f"Ein Fehler ist aufgetreten: {e}")
    finally:
        conn.close()

def delete_provider_from_blacklist(provider_domain: str) -> tuple[bool, str]:
    """Löscht einen Provider von der Blacklist."""
    conn = get_db_connection()
    domain = provider_domain.lower().replace('@', '')
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM blacklisted_providers WHERE provider_domain = ?", (domain,))
        conn.commit()
        if cursor.rowcount == 0:
            return (False, f"Fehler: Provider '{domain}' nicht auf der Blacklist gefunden.")
        return (True, f"Provider '{domain}' erfolgreich von der Blacklist entfernt.")
    except Exception as e:
        return (False, f"Ein Fehler ist aufgetreten: {e}")
    finally:
        conn.close()

def delete_email_from_unreachable_list(email: str) -> tuple[bool, str]:
    """Löscht eine E-Mail aus der Liste der unerreichbaren E-Mails."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM unreachable_emails WHERE email = ?", (email.lower(),))
        conn.commit()
        if cursor.rowcount == 0:
            return (False, f"Fehler: E-Mail '{email}' nicht in der Liste der unerreichbaren E-Mails gefunden.")
        return (True, f"E-Mail '{email}' erfolgreich aus der Liste der unerreichbaren E-Mails entfernt.")
    except Exception as e:
        return (False, f"Ein Fehler ist aufgetreten: {e}")
    finally:
        conn.close()

def main_menu():
    """Zeigt das Hauptmenü an und verarbeitet die Benutzereingaben."""
    while True:
        print("\n--- Kontakt-Datenbank Hauptmenü ---")
        print("1. Neuen Kontakt hinzufügen")
        print("2. E-Mail zur Blacklist hinzufügen")
        print("3. Provider zur Blacklist hinzufügen")
        print("4. E-Mail als unerreichbar markieren")
        print("5. Alle Kontakte anzeigen")
        print("6. Blacklisted E-Mails anzeigen")
        print("7. Blacklisted Provider anzeigen")
        print("8. Unerreichbare E-Mails anzeigen")
        print("9. Beenden")

        choice = input("Bitte wählen Sie eine Option: ")

        if choice == '1':
            print("\n--- Neuen Kontakt hinzufügen ---")
            first_name = input("Vorname: ")
            last_name = input("Nachname: ")
            email = input("E-Mail: ")
            address = input("Adresse (optional): ")
            phone = input("Telefon (optional): ")
            contact = Contact(first_name, last_name, email, address, phone)
            success, message = add_contact(contact)
            print(message)
        elif choice == '2':
            email = input("E-Mail zur Blacklist hinzufügen: ")
            success, message = add_email_to_blacklist(email)
            print(message)
        elif choice == '3':
            provider = input("Provider-Domain zur Blacklist hinzufügen (z.B. example.com): ")
            success, message = add_provider_to_blacklist(provider)
            print(message)
        elif choice == '4':
            email = input("E-Mail als unerreichbar markieren: ")
            success, message = add_email_to_unreachable_list(email)
            print(message)
        elif choice == '5':
            print("\n--- Alle Kontakte ---")
            contacts = get_all_contacts()
            if not contacts:
                print("Keine Kontakte gefunden.")
            for contact in contacts:
                print(f"- {contact.first_name} {contact.last_name}, {contact.email}")
        elif choice == '6':
            print("\n--- Blacklisted E-Mails ---")
            emails = get_blacklisted_emails()
            if not emails:
                print("Keine E-Mails auf der Blacklist.")
            for email in emails:
                print(f"- {email}")
        elif choice == '7':
            print("\n--- Blacklisted Provider ---")
            providers = get_blacklisted_providers()
            if not providers:
                print("Keine Provider auf der Blacklist.")
            for provider in providers:
                print(f"- {provider}")
        elif choice == '8':
            print("\n--- Unerreichbare E-Mails ---")
            emails = get_unreachable_emails()
            if not emails:
                print("Keine unerreichbaren E-Mails gefunden.")
            for email in emails:
                print(f"- {email}")
        elif choice == '9':
            print("Anwendung wird beendet.")
            break
        else:
            print("Ungültige Auswahl. Bitte versuchen Sie es erneut.")

if __name__ == '__main__':
    # Stellt sicher, dass die Datenbank und Tabellen existieren
    import os
    if not os.path.exists(DATABASE_FILE):
        print("Datenbank nicht gefunden. Führe 'database_setup.py' zuerst aus.")
    else:
        main_menu()
