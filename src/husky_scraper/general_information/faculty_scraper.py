from typing import List, Dict
from bs4 import BeautifulSoup
from src.husky_scraper.base_scraper import BaseScraper
from src.husky_scraper.utils import fetch_html, save_to_file, replace_unicode


class FacultyScraper(BaseScraper):
    """
    Scraper for extracting faculty member information from multiple URLs.
    """

    def __init__(self, urls: List[str], output_file: str, logger) -> None:
        """
        Initializes the FacultyScraper with a list of URLs.

        Args:
            urls (List[str]): List of URLs to scrape.
            output_file (str): File to save the scraped data.
            logger: The logger instance for logging.
        """
        super().__init__(urls[0], output_file, logger)  # Use first URL for the base class
        self.urls = urls

    def parse(self, html: str) -> List[Dict[str, str]]:
        """
        Parses faculty members from the HTML content.

        Args:
            html (str): The HTML content fetched from the URL.

        Returns:
            List[Dict[str, str]]: A list of dictionaries containing faculty member details.
        """
        self.logger.info("Parsing faculty members.")
        soup = BeautifulSoup(html, 'html.parser')
        # Find all faculty blocks with the <p> tag and class 'keeptogether'
        faculty_blocks = soup.find_all('p', class_='keeptogether')
        faculty_list = []
        # Loop through each faculty block and extract relevant information
        for faculty in faculty_blocks:
            # Extract the name from the <strong> tag
            name_tag = faculty.find('strong')
            name = name_tag.text.strip() if name_tag else "No name available"

            # Extract the title and department from the remaining text
            title_and_department = faculty.get_text(separator=" ").replace(name, "").strip()

            # Append the data to the faculty_data list
            faculty_list.append({
                "Name":replace_unicode(name),
                "Title and Department": replace_unicode(title_and_department)
            })
        self.logger.info(f"Parsed {len(faculty_list)} faculty members.")
        return faculty_list

    def scrape(self) -> None:
        """
        Scrapes faculty members from multiple URLs and saves the data.
        """
        all_faculty = []
        for url in self.urls:
            self.logger.info(f"Scraping faculty members from {url}")
            html = fetch_html(url, self.logger)
            if html:
                all_faculty.extend(self.parse(html))

        save_to_file(all_faculty, self.output_file, self.logger)
        self.logger.info(f"All faculty data saved to {self.output_file}")
