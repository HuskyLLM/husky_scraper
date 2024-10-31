from typing import List, Dict
from bs4 import BeautifulSoup
import re
from src.husky_scraper.base_scraper import BaseScraper
from src.husky_scraper_v3.utils import fetch_html, save_to_file, replace_unicode


def clean_cell_text(text: str, label: str) -> str:
    """
    Cleans the cell text by removing redundant labels (e.g., "Academic Program", "Major Transcript Title").

    Args:
        text (str): The raw text from the cell.
        label (str): The label to remove from the beginning of the cell text.

    Returns:
        str: Cleaned text without the redundant label.
    """
    return text.replace(label, "").strip()


class MajorCIPScraper(BaseScraper):
    """
    Scraper for extracting major CIP codes from the Northeastern University catalog page.
    """

    def __init__(self, urls: List[str], output_file: str, logger) -> None:
        super().__init__(urls[0], output_file, logger)
        self.urls = urls

    def parse(self, html: str) -> List[Dict[str, str]]:
        """
        Parses major CIP codes from the HTML content.

        Args:
            html (str): The HTML content fetched from the URL.

        Returns:
            List[Dict[str, str]]: A list of dictionaries containing major CIP code details.
        """
        self.logger.info("Parsing major CIP codes.")
        soup = BeautifulSoup(html, 'html.parser')

        # Locate the major CIP codes table
        table = soup.find('table', class_='visible grid sc_majorciptable')
        cip_list = []

        # Extract headers for the table
        headers = [header.text.strip() for header in table.find_all('th')]

        # Loop through each row and extract details
        for row in table.find_all('tr')[1:]:  # Skipping the header row
            cols = row.find_all('td')
            if cols:
                data = {
                    headers[0]: replace_unicode(clean_cell_text(cols[0].get_text(strip=True), headers[0])),
                    headers[1]: replace_unicode(clean_cell_text(cols[1].get_text(strip=True), headers[1])),
                    headers[2]: replace_unicode(clean_cell_text(cols[2].get_text(strip=True), headers[2]))
                }
                cip_list.append(data)

        self.logger.info(f"Parsed {len(cip_list)} CIP codes.")
        return cip_list

    def scrape(self) -> None:
        """
        Scrapes major CIP codes from multiple URLs and saves the data.
        """
        cip_data = []
        for url in self.urls:
            self.logger.info(f"Scraping CIP codes from {url}")
            html = fetch_html(url, self.logger)
            if html:
                cip_data.extend(self.parse(html))

        save_to_file(cip_data, self.output_file, self.logger)
        self.logger.info(f"All CIP code data saved to {self.output_file}")
