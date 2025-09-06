import unittest
import os
import contact_db
from database_setup import setup_database
from contact_db import Contact

class TestContactDB(unittest.TestCase):

    def setUp(self):
        """Set up a temporary database for testing."""
        self.db_file = 'test.db'
        contact_db.DATABASE_FILE = self.db_file
        setup_database(self.db_file)

    def tearDown(self):
        """Remove the temporary database after tests."""
        os.remove(self.db_file)

    def test_add_contact_success(self):
        """Test adding a new contact successfully."""
        contact = Contact("John", "Doe", "john.doe@example.com", "123 Main St", "555-1234")
        success, message = contact_db.add_contact(contact)
        self.assertTrue(success)
        self.assertIn("erfolgreich hinzugefügt", message)

        # Verify the contact is in the database
        contacts = contact_db.get_all_contacts()
        self.assertEqual(len(contacts), 1)
        self.assertEqual(contacts[0].email, "john.doe@example.com")

    def test_add_contact_duplicate(self):
        """Test preventing a duplicate contact from being added."""
        contact1 = Contact("Jane", "Doe", "jane.doe@example.com")
        contact_db.add_contact(contact1)

        contact2 = Contact("Jane", "Doe", "jane.doe@example.com")
        success, message = contact_db.add_contact(contact2)

        self.assertFalse(success)
        self.assertIn("existiert bereits", message)

        contacts = contact_db.get_all_contacts()
        self.assertEqual(len(contacts), 1)

    def test_email_blacklist(self):
        """Test that a contact with a blacklisted email cannot be added."""
        blacklisted_email = "spam@spammer.com"
        contact_db.add_email_to_blacklist(blacklisted_email)

        contact = Contact("Spam", "Bot", blacklisted_email)
        success, message = contact_db.add_contact(contact)

        self.assertFalse(success)
        self.assertIn("gesperrt", message)

        # Verify it was not added
        contacts = contact_db.get_all_contacts()
        self.assertEqual(len(contacts), 0)

    def test_provider_blacklist(self):
        """Test that a contact with a blacklisted provider cannot be added."""
        blacklisted_provider = "block-this-domain.com"
        contact_db.add_provider_to_blacklist(blacklisted_provider)

        contact = Contact("Test", "User", f"user@{blacklisted_provider}")
        success, message = contact_db.add_contact(contact)

        self.assertFalse(success)
        self.assertIn("gesperrt", message)

    def test_unreachable_email_list(self):
        """Test adding an email to the unreachable list."""
        email = "unreachable@example.com"
        success, message = contact_db.add_email_to_unreachable_list(email)
        self.assertTrue(success)

        # Verify it's in the list
        unreachable_list = contact_db.get_unreachable_emails()
        self.assertIn(email, unreachable_list)

        # Test adding it again
        success, message = contact_db.add_email_to_unreachable_list(email)
        self.assertFalse(success)
        self.assertIn("bereits als unerreichbar markiert", message)

if __name__ == '__main__':
    unittest.main()
