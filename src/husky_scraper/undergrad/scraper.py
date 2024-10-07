from bs4 import BeautifulSoup
from src.husky_scraper.base_scraper import BaseScraper
from src.husky_scraper.utils import fetch_html, save_to_file, replace_unicode
import re
from typing import List, Dict


class UndergradScraper(BaseScraper):
    """
    Scraper for extracting ROTC program details, including headings, paragraphs, and table data.
    """
    def parse(self, html: str) -> dict[str, str]:
        self.logger.info("Parsing ROTC program details.")

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Extract the title of the page
        title = soup.find('title').get_text(strip=True)

        # Extract phone numbers using regex
        phone_numbers = re.findall(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', soup.get_text())

        # Extract email addresses using regex
        email_addresses = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', soup.get_text())

        # Define containers for ROTC programs
        rotc_sections = {
            "Army ROTC Program": 'armyrotcprogramtextcontainer',
            "Navy ROTC Program": 'navyrotcprogramtextcontainer',
            "Air Force ROTC Program": 'airforcerotcprogramtextcontainer',
            "overview":'textcontainer',
            "courses": 'coursestextcontainer'
        }

        content_dict = {}

        # Loop through each ROTC section and extract content
        for program, container_id in rotc_sections.items():
            section = soup.find('div', {'id': container_id})
            if section:
                content_dict[program] = self.extract_content(section)

        # Return the parsed information as a dictionary
        return {
            title: {
                'Phone Numbers': phone_numbers,
                'Email Addresses': email_addresses,
                'Programs': content_dict
            }
        }

    def extract_content(self, section) -> dict:
        """
        Extracts headings, paragraphs, and table data from the given section.

        Args:
            section: BeautifulSoup element representing the section to extract.

        Returns:
            dict: A dictionary of headings with their corresponding paragraphs and tables.
        """
        content = {}
        current_heading = None  # No heading at the start

        for tag in section.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'table']):
            # If the tag is a heading, start a new section
            if tag.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                current_heading = replace_unicode(tag.get_text(strip=True))
                if current_heading not in content:
                    content[current_heading] = []

            elif tag.name == 'p' and current_heading:
                # Add paragraphs under the current heading
                paragraph = replace_unicode(tag.get_text(separator=" ").strip())
                if paragraph:
                    content[current_heading].append(paragraph)

            elif tag.name == 'table' and current_heading:
                # Extract table data
                table_data = []
                rows = tag.find_all('tr')
                for row in rows:
                    columns = [replace_unicode(col.get_text(strip=True)) for col in row.find_all(['th', 'td'])]
                    table_data.append(columns)
                content[current_heading].append({"Table": table_data})

        # Flatten paragraphs under each heading into a single string or list of paragraphs
        for key, value in content.items():
            content[key] = value #" ".join(value) if isinstance(value, list) else value

        return content
