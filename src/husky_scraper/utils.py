import requests
import json
import sys
import re


def fetch_html(url: str, logging) -> str:
    """
    Fetches the HTML content from the provided URL.

    Args:
        url (str): The URL to fetch the HTML from.
        logging: The logger instance used for logging information and errors.

    Returns:
        str: The HTML content fetched from the URL, or None if an error occurred.
    """
    try:
        logging.info(f"Fetching HTML content from: {url}")
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        logging.error(f"Error fetching URL {url}: {e}, {sys.exc_info()}")
        return None


def save_to_file(data: dict, output_file: str, logging) -> None:
    """
    Saves the data to the specified output file.

    Args:
        data (dict): The data to save.
        output_file (str): The file path to save the data to.
        logging: The logger instance used for logging information and errors.
    """
    try:
        logging.info(f"Saving data to {output_file}")
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        logging.error(f"Error saving to {output_file}: {e}, {sys.exc_info()}")


def load_from_file(input_file: str, logging) -> dict:
    """
    Loads the data from the specified input file.

    Args:
        input_file (str): The file path to load the data from.
        logging: The logger instance used for logging information and errors.

    Returns:
        dict: The data loaded from the file, or None if an error occurred.
    """
    try:
        logging.info(f"Loading data from {input_file}")
        with open(input_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading from {input_file}: {e}, {sys.exc_info()}")
        return None


def replace_unicode(text: str) -> str:
    """
    Replaces any non-ASCII (Unicode) characters in the given text with a space.

    Args:
        text (str): The input text containing Unicode characters.

    Returns:
        str: The cleaned text with all Unicode characters replaced by spaces.
    """
    # Use re.sub to replace all non-ASCII characters
    return re.sub(r'[^\x00-\x7F]+', ' ', text)
