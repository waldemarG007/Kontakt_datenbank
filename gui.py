import tkinter as tk
from tkinter import ttk, messagebox
import contact_db as db

class ContactApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kontakt-Datenbank")

        # Apply a modern theme
        style = ttk.Style(self.root)
        style.theme_use('clam')

        self.root.geometry("800x600")
        self.selected_contact_id = None

        # Main notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, padx=10, fill="both", expand=True)

        # Create frames for each tab
        self.tab_contacts = ttk.Frame(self.notebook, width=780, height=580)
        self.tab_blacklist = ttk.Frame(self.notebook, width=780, height=580)
        self.tab_unreachable = ttk.Frame(self.notebook, width=780, height=580)

        self.notebook.add(self.tab_contacts, text="Kontakte")
        self.notebook.add(self.tab_blacklist, text="Blacklists")
        self.notebook.add(self.tab_unreachable, text="Unerreichbare E-Mails")

        # Create the content of each tab
        self.create_contacts_tab()
        self.create_blacklist_tab()
        self.create_unreachable_tab()

        # Populate the lists with initial data from the database
        self.populate_all_lists()

    def create_contacts_tab(self):
        # Frame for the list and scrollbar
        list_frame = ttk.LabelFrame(self.tab_contacts, text="Kontaktliste")
        list_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        search_frame = ttk.Frame(list_frame)
        search_frame.pack(fill="x", pady=5, padx=5)
        ttk.Label(search_frame, text="Suche:").pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.on_search)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side="left", fill="x", expand=True, padx=5)

        self.tree_contacts = ttk.Treeview(list_frame, columns=("id", "name", "email", "phone", "address"), show="headings")
        self.tree_contacts.heading("id", text="ID")
        self.tree_contacts.column("id", width=40)
        self.tree_contacts.heading("name", text="Name")
        self.tree_contacts.column("name", width=150)
        self.tree_contacts.heading("email", text="E-Mail")
        self.tree_contacts.column("email", width=200)
        self.tree_contacts.heading("phone", text="Telefon")
        self.tree_contacts.column("phone", width=120)
        self.tree_contacts.heading("address", text="Adresse")
        self.tree_contacts.column("address", width=250)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree_contacts.yview)
        self.tree_contacts.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree_contacts.pack(side="left", fill="both", expand=True)

        # Frame for the form
        form_frame = ttk.LabelFrame(self.tab_contacts, text="Neuen Kontakt anlegen")
        form_frame.pack(side="right", fill="y", padx=10, pady=10)

        labels = ["Vorname:", "Nachname:", "E-Mail:", "Telefon:", "Adresse:"]
        self.contact_entries = {}
        for i, label_text in enumerate(labels):
            label = ttk.Label(form_frame, text=label_text)
            label.grid(row=i, column=0, sticky="w", padx=5, pady=5)
            entry = ttk.Entry(form_frame, width=30)
            entry.grid(row=i, column=1, sticky="ew", padx=5, pady=5)
            self.contact_entries[label_text] = entry

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=len(labels), column=0, columnspan=2, pady=10)

        add_button = ttk.Button(button_frame, text="Hinzufügen", command=self.add_new_contact)
        add_button.pack(side="left", padx=5)

        update_button = ttk.Button(button_frame, text="Aktualisieren", command=self.update_selected_contact)
        update_button.pack(side="left", padx=5)

        delete_button = ttk.Button(button_frame, text="Löschen", command=self.delete_selected_contact)
        delete_button.pack(side="left", padx=5)

        clear_button = ttk.Button(button_frame, text="Leeren", command=self.clear_contact_form)
        clear_button.pack(side="left", padx=5)

        # Bind selection event to the treeview
        self.tree_contacts.bind('<<TreeviewSelect>>', self.on_contact_select)
        # Bind deselection event
        self.tree_contacts.bind('<Button-1>', self.on_deselect)
        list_frame.bind('<Button-1>', lambda e: self.tree_contacts.focus_set() or self.on_deselect(e))


    def create_blacklist_tab(self):
        # Email Blacklist Frame
        email_frame = ttk.LabelFrame(self.tab_blacklist, text="Gesperrte E-Mail-Adressen")
        email_frame.pack(fill="x", padx=10, pady=10, pady_top=5)

        email_entry_frame = ttk.Frame(email_frame)
        email_entry_frame.pack(fill="x", expand=True, pady=5)
        ttk.Label(email_entry_frame, text="E-Mail:").pack(side="left", padx=5)
        self.entry_blacklist_email = ttk.Entry(email_entry_frame, width=40)
        self.entry_blacklist_email.pack(side="left", expand=True, fill="x", padx=5)
        btn_add_email = ttk.Button(email_entry_frame, text="Hinzufügen", command=self.add_to_email_blacklist)
        btn_add_email.pack(side="left", padx=5)
        btn_delete_email = ttk.Button(email_entry_frame, text="Löschen", command=self.delete_from_email_blacklist)
        btn_delete_email.pack(side="left", padx=5)

        self.list_blacklisted_emails = tk.Listbox(email_frame, height=8)
        self.list_blacklisted_emails.pack(fill="x", expand=True, padx=5, pady=5)

        # Provider Blacklist Frame
        provider_frame = ttk.LabelFrame(self.tab_blacklist, text="Gesperrte Provider")
        provider_frame.pack(fill="x", padx=10, pady=10)

        provider_entry_frame = ttk.Frame(provider_frame)
        provider_entry_frame.pack(fill="x", expand=True, pady=5)
        ttk.Label(provider_entry_frame, text="Provider-Domain:").pack(side="left", padx=5)
        self.entry_blacklist_provider = ttk.Entry(provider_entry_frame, width=40)
        self.entry_blacklist_provider.pack(side="left", expand=True, fill="x", padx=5)
        btn_add_provider = ttk.Button(provider_entry_frame, text="Hinzufügen", command=self.add_to_provider_blacklist)
        btn_add_provider.pack(side="left", padx=5)
        btn_delete_provider = ttk.Button(provider_entry_frame, text="Löschen", command=self.delete_from_provider_blacklist)
        btn_delete_provider.pack(side="left", padx=5)

        self.list_blacklisted_providers = tk.Listbox(provider_frame, height=8)
        self.list_blacklisted_providers.pack(fill="x", expand=True, padx=5, pady=5)

    def create_unreachable_tab(self):
        unreachable_frame = ttk.LabelFrame(self.tab_unreachable, text="Unerreichbare E-Mails")
        unreachable_frame.pack(fill="x", padx=10, pady=10)

        entry_frame = ttk.Frame(unreachable_frame)
        entry_frame.pack(fill="x", expand=True, pady=5)
        ttk.Label(entry_frame, text="E-Mail:").pack(side="left", padx=5)
        self.entry_unreachable_email = ttk.Entry(entry_frame, width=40)
        self.entry_unreachable_email.pack(side="left", expand=True, fill="x", padx=5)
        btn_add_unreachable = ttk.Button(entry_frame, text="Hinzufügen", command=self.add_to_unreachable_list)
        btn_add_unreachable.pack(side="left", padx=5)
        btn_delete_unreachable = ttk.Button(entry_frame, text="Löschen", command=self.delete_from_unreachable_list)
        btn_delete_unreachable.pack(side="left", padx=5)

        self.list_unreachable_emails = tk.Listbox(unreachable_frame, height=15)
        self.list_unreachable_emails.pack(fill="x", expand=True, padx=5, pady=5)

    # --- Backend Logic and List Population ---

    def populate_all_lists(self):
        self.populate_contacts_list()
        self.populate_blacklisted_emails()
        self.populate_blacklisted_providers()
        self.populate_unreachable_emails()

    def populate_contacts_list(self, contacts: Optional[list[db.Contact]] = None):
        """Füllt die Kontaktliste im Treeview, optional mit einer gefilterten Liste."""
        for i in self.tree_contacts.get_children():
            self.tree_contacts.delete(i)

        if contacts is None:
            contacts = db.get_all_contacts()

        for contact in contacts:
            self.tree_contacts.insert("", "end", values=(contact.id, f"{contact.first_name} {contact.last_name}", contact.email, contact.phone_number, contact.address))

    def populate_blacklisted_emails(self):
        self.list_blacklisted_emails.delete(0, tk.END)
        for email in db.get_blacklisted_emails():
            self.list_blacklisted_emails.insert(tk.END, email)

    def populate_blacklisted_providers(self):
        self.list_blacklisted_providers.delete(0, tk.END)
        for provider in db.get_blacklisted_providers():
            self.list_blacklisted_providers.insert(tk.END, provider)

    def populate_unreachable_emails(self):
        self.list_unreachable_emails.delete(0, tk.END)
        for email in db.get_unreachable_emails():
            self.list_unreachable_emails.insert(tk.END, email)

    def add_new_contact(self):
        first_name = self.contact_entries["Vorname:"].get()
        last_name = self.contact_entries["Nachname:"].get()
        email = self.contact_entries["E-Mail:"].get()
        phone = self.contact_entries["Telefon:"].get()
        address = self.contact_entries["Adresse:"].get()

        if not first_name or not last_name or not email:
            messagebox.showerror("Eingabefehler", "Vorname, Nachname und E-Mail sind Pflichtfelder.")
            return

        contact = db.Contact(first_name, last_name, email, address, phone)
        success, message = db.add_contact(contact)

        if success:
            messagebox.showinfo("Erfolg", message)
            self.populate_contacts_list()
            for entry in self.contact_entries.values():
                entry.delete(0, tk.END)
        else:
            messagebox.showerror("Fehler", message)

    def clear_contact_form(self):
        """Leert alle Eingabefelder im Kontaktformular und hebt die Auswahl auf."""
        for entry in self.contact_entries.values():
            entry.delete(0, tk.END)

        self.selected_contact_id = None
        # Deselect any selected item in the treeview
        if self.tree_contacts.selection():
            self.tree_contacts.selection_remove(self.tree_contacts.selection())

        # Reset search to show all contacts
        self.search_var.set("")
        self.populate_contacts_list()

    def on_deselect(self, event):
        """Clears the selection if the user clicks on an empty area."""
        region = self.tree_contacts.identify_region(event.x, event.y)
        if region == "nothing":
            self.clear_contact_form()

    def on_search(self, *args):
        """Wird aufgerufen, wenn sich der Text im Suchfeld ändert."""
        query = self.search_var.get()
        searched_contacts = db.search_contacts(query)
        self.populate_contacts_list(searched_contacts)

    def delete_from_email_blacklist(self):
        """Löscht die ausgewählte E-Mail von der Blacklist."""
        selected_indices = self.list_blacklisted_emails.curselection()
        if not selected_indices:
            messagebox.showerror("Fehler", "Bitte wählen Sie eine E-Mail aus der Liste aus.")
            return

        email = self.list_blacklisted_emails.get(selected_indices[0])
        if messagebox.askyesno("Bestätigung", f"Möchten Sie '{email}' wirklich von der Blacklist entfernen?"):
            success, message = db.delete_email_from_blacklist(email)
            if success:
                messagebox.showinfo("Erfolg", message)
                self.populate_blacklisted_emails()
            else:
                messagebox.showerror("Fehler", message)

    def delete_from_provider_blacklist(self):
        """Löscht den ausgewählten Provider von der Blacklist."""
        selected_indices = self.list_blacklisted_providers.curselection()
        if not selected_indices:
            messagebox.showerror("Fehler", "Bitte wählen Sie einen Provider aus der Liste aus.")
            return

        provider = self.list_blacklisted_providers.get(selected_indices[0])
        if messagebox.askyesno("Bestätigung", f"Möchten Sie '{provider}' wirklich von der Blacklist entfernen?"):
            success, message = db.delete_provider_from_blacklist(provider)
            if success:
                messagebox.showinfo("Erfolg", message)
                self.populate_blacklisted_providers()
            else:
                messagebox.showerror("Fehler", message)

    def delete_from_unreachable_list(self):
        """Löscht die ausgewählte E-Mail aus der Unerreichbar-Liste."""
        selected_indices = self.list_unreachable_emails.curselection()
        if not selected_indices:
            messagebox.showerror("Fehler", "Bitte wählen Sie eine E-Mail aus der Liste aus.")
            return

        email = self.list_unreachable_emails.get(selected_indices[0])
        if messagebox.askyesno("Bestätigung", f"Möchten Sie '{email}' wirklich aus der Liste entfernen?"):
            success, message = db.delete_email_from_unreachable_list(email)
            if success:
                messagebox.showinfo("Erfolg", message)
                self.populate_unreachable_emails()
            else:
                messagebox.showerror("Fehler", message)

    def on_contact_select(self, event):
        """Wird aufgerufen, wenn ein Kontakt in der Liste ausgewählt wird."""
        selected_items = self.tree_contacts.selection()
        if not selected_items:
            self.selected_contact_id = None
            return

        selected_item = selected_items[0]
        # Das erste Element in 'values' ist die ID
        self.selected_contact_id = self.tree_contacts.item(selected_item, "values")[0]

        contact = db.get_contact_by_id(self.selected_contact_id)
        if contact:
            # Formularfelder leeren
            for entry in self.contact_entries.values():
                entry.delete(0, tk.END)

            # Formularfelder mit den Kontaktdaten füllen
            self.contact_entries["Vorname:"].insert(0, contact.first_name)
            self.contact_entries["Nachname:"].insert(0, contact.last_name)
            self.contact_entries["E-Mail:"].insert(0, contact.email)
            self.contact_entries["Telefon:"].insert(0, contact.phone_number or "")
            self.contact_entries["Adresse:"].insert(0, contact.address or "")

    def update_selected_contact(self):
        """Aktualisiert den ausgewählten Kontakt mit den Daten aus dem Formular."""
        if self.selected_contact_id is None:
            messagebox.showerror("Fehler", "Bitte wählen Sie zuerst einen Kontakt aus der Liste aus.")
            return

        first_name = self.contact_entries["Vorname:"].get()
        last_name = self.contact_entries["Nachname:"].get()
        email = self.contact_entries["E-Mail:"].get()
        phone = self.contact_entries["Telefon:"].get()
        address = self.contact_entries["Adresse:"].get()

        if not first_name or not last_name or not email:
            messagebox.showerror("Eingabefehler", "Vorname, Nachname und E-Mail sind Pflichtfelder.")
            return

        contact = db.Contact(first_name, last_name, email, address, phone, id=self.selected_contact_id)
        success, message = db.update_contact(contact)

        if success:
            messagebox.showinfo("Erfolg", message)
            self.populate_contacts_list()
        else:
            messagebox.showerror("Fehler", message)

    def delete_selected_contact(self):
        """Löscht den ausgewählten Kontakt."""
        if self.selected_contact_id is None:
            messagebox.showerror("Fehler", "Bitte wählen Sie zuerst einen Kontakt aus der Liste aus.")
            return

        if messagebox.askyesno("Bestätigung", "Möchten Sie den ausgewählten Kontakt wirklich löschen?"):
            success, message = db.delete_contact(self.selected_contact_id)
            if success:
                messagebox.showinfo("Erfolg", message)
                self.populate_contacts_list()
                # Formularfelder leeren
                for entry in self.contact_entries.values():
                    entry.delete(0, tk.END)
                self.selected_contact_id = None
            else:
                messagebox.showerror("Fehler", message)

    def add_to_email_blacklist(self):
        email = self.entry_blacklist_email.get()
        if not email:
            messagebox.showerror("Eingabefehler", "Bitte geben Sie eine E-Mail-Adresse ein.")
            return

        success, message = db.add_email_to_blacklist(email)
        if success:
            messagebox.showinfo("Erfolg", message)
            self.populate_blacklisted_emails()
            self.entry_blacklist_email.delete(0, tk.END)
        else:
            messagebox.showerror("Fehler", message)

    def add_to_provider_blacklist(self):
        provider = self.entry_blacklist_provider.get()
        if not provider:
            messagebox.showerror("Eingabefehler", "Bitte geben Sie eine Provider-Domain ein.")
            return

        success, message = db.add_provider_to_blacklist(provider)
        if success:
            messagebox.showinfo("Erfolg", message)
            self.populate_blacklisted_providers()
            self.entry_blacklist_provider.delete(0, tk.END)
        else:
            messagebox.showerror("Fehler", message)

    def add_to_unreachable_list(self):
        email = self.entry_unreachable_email.get()
        if not email:
            messagebox.showerror("Eingabefehler", "Bitte geben Sie eine E-Mail-Adresse ein.")
            return

        success, message = db.add_email_to_unreachable_list(email)
        if success:
            messagebox.showinfo("Erfolg", message)
            self.populate_unreachable_emails()
            self.entry_unreachable_email.delete(0, tk.END)
        else:
            messagebox.showerror("Fehler", message)


if __name__ == "__main__":
    # Ensure the database exists before starting the GUI
    import os
    if not os.path.exists(db.DATABASE_FILE):
        # We can't use the CLI prompt here. We should show an error.
        # For simplicity in a GUI app, we can try to create it automatically.
        print(f"Datenbank '{db.DATABASE_FILE}' nicht gefunden. Erstelle sie...")
        from database_setup import setup_database
        setup_database()
        print("Datenbank erstellt.")

    root = tk.Tk()
    app = ContactApp(root)
    root.mainloop()
