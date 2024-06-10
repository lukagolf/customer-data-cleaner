import pandas as pd
import re
import argparse
import logging
from sqlalchemy import create_engine

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

def connect_to_database(connection_string):
    """
    Connect to the database using SQLAlchemy and return the connection engine.

    Parameters:
    connection_string (str): The connection string for the database.

    Returns:
    sqlalchemy.engine.Engine: A connection engine to the database.
    """
    try:
        engine = create_engine(connection_string)
        return engine
    except Exception as e:
        logging.error(f"Error connecting to database: {e}")
        return None


def fetch_data(engine, table_name):
    """
    Fetch data from the specified table and return it as a DataFrame.

    Parameters:
    engine (sqlalchemy.engine.Engine): The connection engine to the database.
    table_name (str): The name of the table from which to fetch data.

    Returns:
    pandas.DataFrame: A DataFrame containing the data from the specified table.
    """
    query = f"SELECT * FROM {table_name}"
    try:
        df = pd.read_sql_query(query, engine)
        return df
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        return pd.DataFrame()


def is_valid_email(email):
    """
    Check if the email is valid.

    Parameters:
    email (str): The email address to validate.

    Returns:
    bool: True if the email is valid, False otherwise.
    """
    regex = r"^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    return re.match(regex, email) is not None


def is_valid_name(name):
    """
    Check if the name is valid.

    Parameters:
    name (str): The name to validate.

    Returns:
    bool: True if the name is valid, False otherwise.
    """
    return bool(re.match(r"^[A-Za-z\s]{1,50}$", name))


def identify_issues(df):
    """
    Identify duplicates, invalid emails, and improperly inputted names.

    Parameters:
    df (pandas.DataFrame): The DataFrame containing customer data.

    Returns:
    tuple: A tuple containing:
        - problematic_entries (pandas.DataFrame): A DataFrame with problematic
                                                  entries.
        - num_duplicates (int): The number of duplicate entries.
        - num_invalid_emails (int): The number of entries with invalid emails.
        - num_invalid_names (int): The number of entries with invalid names.
    """
    duplicates = df[df.duplicated(subset=["name", "last_name", "email"], keep=False)]
    invalid_emails = df[~df["email"].apply(is_valid_email)]
    invalid_names = df[
        ~df["name"].apply(is_valid_name) | ~df["last_name"].apply(is_valid_name)
    ]

    problematic_entries = pd.concat(
        [duplicates, invalid_emails, invalid_names]
    ).drop_duplicates()
    return problematic_entries, len(duplicates), len(invalid_emails), len(invalid_names)


def save_to_csv(df, file_path):
    """
    Save the DataFrame to a CSV file.

    Parameters:
    df (pandas.DataFrame): The DataFrame to save.
    file_path (str): The file path to save the CSV file to.
    """
    df.to_csv(file_path, index=False)
    logging.info(f"Saved all problematic entries to '{file_path}'")


def main(connection_string, table_name, output_file):
    """
    Main function to run the data validation process.

    Parameters:
    connection_string (str): The connection string for the database.
    table_name (str): The name of the table to query.
    output_file (str): The file path to save the problematic entries CSV file.
    """
    engine = connect_to_database(connection_string)
    if not engine:
        return

    df = fetch_data(engine, table_name)
    if df.empty:
        logging.warning("No data fetched from the database.")
        return

    problematic_entries, num_duplicates, num_invalid_emails, num_invalid_names = (
        identify_issues(df)
    )

    logging.info(f"Found {num_duplicates} duplicate entries")
    logging.info(f"Found {num_invalid_emails} entries with invalid emails")
    logging.info(f"Found {num_invalid_names} entries with invalid names")

    save_to_csv(problematic_entries, output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process customer data for issues.")
    parser.add_argument(
        "connection_string",
        type=str,
        help="Database connection string (e.g., sqlite:///your_database.db, postgresql://user:password@localhost/dbname)",
    )
    parser.add_argument("table_name", type=str, help="Name of the table to query")
    parser.add_argument(
        "output_file", type=str, help="Path to save the output CSV file"
    )

    args = parser.parse_args()

    main(args.connection_string, args.table_name, args.output_file)
