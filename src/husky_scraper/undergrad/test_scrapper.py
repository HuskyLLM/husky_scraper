from bs4 import BeautifulSoup
from src.husky_scraper.base_scraper import BaseScraper
from src.husky_scraper.utils import fetch_html, save_to_file, replace_unicode
import re
from typing import List, Dict

class UndergradScraper(BaseScraper):
    """
    Scraper for extracting accommodation details, including headings, paragraphs, and table data.
    """

    def parse(self, html: str) -> dict[str, str]:
        self.logger.info("Parsing accommodation details.")

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Extract the title of the page
        title = soup.find('title').get_text(strip=True)

        # Extract phone numbers using regex
        phone_numbers = re.findall(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', soup.get_text())

        # Extract email addresses using regex
        email_addresses = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', soup.get_text())

        # Extract the main content div
        main_content_tag = soup.find('div', {'id': 'textcontainer'})

        # Find all heading and content tags (h1-h6, p, ul, ol, table) to capture headings, paragraphs, and tables
        content_tags = main_content_tag.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'ul', 'ol', 'table'])

        # Initialize dictionary to hold the content and ensure "Content" exists
        content_dict = {"Content": []}
        current_heading = "Content"  # Default heading if none is found
        links = {}

        # Loop over the content and associate paragraphs or tables with headings
        for tag in content_tags:
            # If the tag is a heading, use it as the current key
            if tag.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                current_heading = replace_unicode(tag.get_text(strip=True))
                if current_heading not in content_dict:
                    content_dict[replace_unicode(current_heading)] = []  # Ensure the heading exists in the dictionary
            elif tag.name == 'table':
                # Extract table content and format it as a list of rows
                table_data = []
                rows = tag.find_all('tr')
                for row in rows:
                    columns = [replace_unicode(col.get_text(strip=True)) for col in row.find_all(['th', 'td'])]
                    table_data.append(columns)
                content_dict[current_heading].append({"Table": table_data})
            else:
                # If it's a paragraph or list, add it under the current heading
                text = tag.get_text(separator=".").strip()
                text = replace_unicode(text).replace("\n", ".")

                # Collect links within the content
                for a_tag in tag.find_all('a', href=True):
                    link_text = a_tag.get_text(strip=True)
                    link_href = a_tag['href']
                    if '.' in link_href:
                        links[replace_unicode(link_text)] = link_href

                # Append the text under the current heading
                content_dict[replace_unicode(current_heading)].append(text)

        # Convert list of paragraphs into a single string per heading
        for key, value in content_dict.items():
            if isinstance(value,str):
                content_dict[replace_unicode(key)] = replace_unicode(" ".join(value))
            else:
                content_dict[replace_unicode(key)] = value
        # Return the parsed information as a dictionary
        return {
            title: {
                'Phone Numbers': phone_numbers,
                'Email Addresses': email_addresses,
                'Content': content_dict,  # Content organized by heading
                'Links in Content': links  # Captured links within paragraphs
            }
        }


class UndergradMultiurlScraper(BaseScraper):
    """
    Scraper for extracting accommodation details, including headings, paragraphs, and table data.
    """
    def __init__(self, urls: List[str], output_file: str, logger) -> None:
        """
        Initializes the FacultyScraper with a list of URLs.

        Args:
            urls (List[str]): List of URLs to scrape.
            output_file (str): File to save the scraped data.
            logger: The logger instance for logging.
        """
    def parse(self, html: str) -> dict[str, str]:
        self.logger.info("Parsing accommodation details.")

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Extract the title of the page
        title = soup.find('title').get_text(strip=True)

        # Extract phone numbers using regex
        phone_numbers = re.findall(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', soup.get_text())

        # Extract email addresses using regex
        email_addresses = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', soup.get_text())

        # Extract the main content div
        main_content_tag = soup.find('div', {'id': 'textcontainer'})

        # Find all heading and content tags (h1-h6, p, ul, ol, table) to capture headings, paragraphs, and tables
        content_tags = main_content_tag.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'ul', 'ol', 'table'])

        # Initialize dictionary to hold the content and ensure "Content" exists
        content_dict = {"Content": []}
        current_heading = "Content"  # Default heading if none is found
        links = {}

        # Loop over the content and associate paragraphs or tables with headings
        for tag in content_tags:
            # If the tag is a heading, use it as the current key
            if tag.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                current_heading = replace_unicode(tag.get_text(strip=True))
                if current_heading not in content_dict:
                    content_dict[replace_unicode(current_heading)] = []  # Ensure the heading exists in the dictionary
            elif tag.name == 'table':
                # Extract table content and format it as a list of rows
                table_data = []
                rows = tag.find_all('tr')
                for row in rows:
                    columns = [replace_unicode(col.get_text(strip=True)) for col in row.find_all(['th', 'td'])]
                    table_data.append(columns)
                content_dict[current_heading].append({"Table": table_data})
            else:
                # If it's a paragraph or list, add it under the current heading
                text = tag.get_text(separator=".").strip()
                text = replace_unicode(text).replace("\n", ".")

                # Collect links within the content
                for a_tag in tag.find_all('a', href=True):
                    link_text = a_tag.get_text(strip=True)
                    link_href = a_tag['href']
                    if '.' in link_href:
                        links[replace_unicode(link_text)] = link_href

                # Append the text under the current heading
                content_dict[replace_unicode(current_heading)].append(text)

        # Convert list of paragraphs into a single string per heading
        for key, value in content_dict.items():
            if isinstance(value,str):
                content_dict[replace_unicode(key)] = replace_unicode(" ".join(value))
            else:
                content_dict[replace_unicode(key)] = value
        # Return the parsed information as a dictionary
        return {
            title: {
                'Phone Numbers': phone_numbers,
                'Email Addresses': email_addresses,
                'Content': content_dict,  # Content organized by heading
                'Links in Content': links  # Captured links within paragraphs
            }
        }

class EducationScraper(BaseScraper):
    """
    Scraper for extracting content related to education programs from a webpage.
    """
    def parse(self, html: str) -> dict[str, str]:
        """
        Parses the HTML content of the webpage and extracts headings, paragraphs, and tables.

        Args:
            html (str): The HTML content of the webpage.

        Returns:
            dict: Parsed data containing headings as keys and their respective paragraphs and tables as values.
        """
        self.logger.info("Parsing education program content.")

        # Initialize BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Dictionary to store the content
        content_dict = {}

        # Find all heading and paragraph tags
        main_content = soup.find('div', {'id': 'main-content'})  # Adjust selector based on HTML structure

        if not main_content:
            self.logger.warning("Main content not found in the page.")
            return {}

        # Extract heading and paragraph tags (h1-h6, p, table)
        content_tags = main_content.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'table'])

        current_heading = None  # Keep track of the current heading
        for tag in content_tags:
            if tag.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                # If it's a heading, set it as the current heading
                current_heading = tag.get_text(strip=True)
                content_dict[current_heading] = []  # Initialize an empty list for paragraphs/tables
            elif tag.name == 'p':
                # If it's a paragraph, append the text to the current heading
                if current_heading:
                    content_dict[current_heading].append(tag.get_text(strip=True))
            elif tag.name == 'table':
                # If it's a table, extract table rows and columns
                if current_heading:
                    table_data = []
                    rows = tag.find_all('tr')
                    for row in rows:
                        columns = [col.get_text(strip=True) for col in row.find_all(['th', 'td'])]
                        table_data.append(columns)
                    content_dict[current_heading].append({'Table': table_data})

        return content_dict

