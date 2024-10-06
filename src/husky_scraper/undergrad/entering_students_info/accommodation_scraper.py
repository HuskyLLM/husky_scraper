from bs4 import BeautifulSoup
from src.husky_scraper.base_scraper import BaseScraper
from src.husky_scraper.utils import fetch_html, save_to_file, replace_unicode
import re


class Accommodation(BaseScraper):
    """
    Scraper for extracting course descriptions from the course catalog page.
    """

    def parse(self, html: str) -> dict[str, str]:
        self.logger.info("Parsing course descriptions.")

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Extract the title of the page
        title = soup.find('title').get_text(strip=True)

        # Extract phone numbers using regex
        phone_numbers = re.findall(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', soup.get_text())

        # Extract email addresses using regex
        email_addresses = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', soup.get_text())

        # Extract the main text content (other information), and replace '\n' with spaces
        main_content = soup.find('div', {'id': 'textcontainer'}).get_text(separator=" ").strip()

        # Extract the first href link from the main content
        main_content_tag = soup.find('div', {'id': 'textcontainer'})
        first_link = main_content_tag.find('a', href=True)['href'] if main_content_tag.find('a', href=True) else None

        return {
            title: {
                'Phone Numbers': phone_numbers,
                'Email Addresses': email_addresses,
                'Main Content': replace_unicode(main_content),
                'First Link': first_link
        }
    }
