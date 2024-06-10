# Customer Data Validation Script

This script is designed to validate customer data in a database. It checks for duplicate entries, invalid emails, and improperly inputted names. The results are saved to a CSV file for further review and correction.

## Features

- Connects to various types of databases using SQLAlchemy.
- Fetches data from a specified table.
- Validates email addresses.
- Validates names to ensure they contain only letters and spaces, and are of reasonable length.
- Identifies duplicate entries.
- Saves problematic entries to a CSV file.
- Provides detailed logging for easy debugging and monitoring.

## Requirements

- Python 3.x
- Pandas
- SQLAlchemy
- A database (e.g., SQLite, PostgreSQL, MySQL)

## Installation

1. Install the necessary Python packages:
    ```sh
    pip install pandas sqlalchemy
    ```

2. Ensure your database is set up and accessible.

## Usage

1. Save the script to a file, for example `validate_customer_data.py`.

2. Run the script from the command line with the required arguments:
    ```sh
    python validate_customer_data.py <connection_string> <table_name> <output_file>
    ```

    - `<connection_string>`: The database connection string (e.g., `sqlite:///your_database.db`, `postgresql://user:password@localhost/dbname`).
    - `<table_name>`: The name of the table to query.
    - `<output_file>`: The path to save the output CSV file containing problematic entries.

### Example

For an SQLite database named `customers.db` with a table named `customers`, and an output file named `problematic_entries.csv`:

```sh
python validate_customer_data.py "sqlite:///customers.db" customers problematic_entries.csv
