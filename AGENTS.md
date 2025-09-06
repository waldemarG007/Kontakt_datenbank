# Agent Instructions

This document provides technical guidance for developers and AI agents working on this repository.

## Project Overview

The project is a Python-based prototype for a contact database application. It uses SQLite for data storage and provides a command-line interface (CLI) for user interaction.

### Core Features
- Contact management (add, view).
- Duplicate detection based on name and email.
- Blacklisting of specific emails and entire provider domains.
- A list to track unreachable email addresses.

## Repository Structure

The repository is organized into the following key files:

- **`database_setup.py`**: A script to initialize the SQLite database (`contacts.db`) and create the necessary tables. This should be run once before the first use.
- **`contact_db.py`**: The main application file. It contains all the core business logic (adding contacts, checking blacklists, etc.), the `Contact` data class, and the CLI menu loop.
- **`test_contact_db.py`**: The unit test suite. It uses Python's `unittest` module to test the functions in `contact_db.py`.
- **`README.md`**: User-facing documentation.
- **`Plan.md`**: A record of the original development plan.

## Key Commands

- **Database Setup**:
  ```bash
  python database_setup.py
  ```
- **Run Application**:
  ```bash
  python contact_db.py
  ```
- **Run Tests**:
  ```bash
  python -m unittest test_contact_db.py
  ```

## Key Design Choices

- **Testability**: The code is designed to be testable. The test suite runs on a separate, temporary database (`test.db`) to ensure tests are isolated and do not interfere with production data. The `database_setup` script was refactored to allow creating databases with different filenames.
- **Separation of Concerns**: Database setup, application logic, and tests are in separate files.
- **Centralized Logic**: The `add_contact` function in `contact_db.py` is the main entry point for adding a contact and orchestrates all necessary validation checks (blacklists, duplicates).
- **Statelessness**: Most functions are stateless and operate directly on the database, simplifying the logic. Database connections are opened and closed within each function call to ensure atomicity.

## Plan Management (`Plan.md`)

- **Do not delete old tasks.** The `Plan.md` file serves as a historical record.
- **Append new tasks.** New high-level tasks or feature requests should be added to the end of the file.
- **Update status.** The status of each major task should be updated as it progresses (e.g., `[To Do]`, `[In Progress]`, `[Done]`).
