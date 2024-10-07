from abc import ABC, abstractmethod
from src.husky_scraper.utils import fetch_html, save_to_file


class BaseScraper(ABC):
    """
    Abstract base class for all scrapers. Defines the structure for scrapers to follow.
    """

    def __init__(self, urls: str, output_file: str, logger) -> None:
        """
        Initializes the scraper.

        Args:
            url (str): The URL to scrape.
            output_file (str): The file to save the scraped content to.
            logger: The logger instance for logging.
        """
        self.urls = urls
        self.output_file = output_file
        self.logger = logger

    @abstractmethod
    def parse(self, html: str):
        """
        Abstract method to parse the HTML content. Must be implemented by subclasses.

        Args:
            html (str): The HTML content to parse.

        Returns:
            The parsed content.
        """
        pass

    def scrape(self) -> None:
        """
        Scrapes faculty members from multiple URLs and saves the data.
        """
        all_data = []
        for url in self.urls:
            self.logger.info(f"Scraping faculty members from {url}")
            html = fetch_html(url, self.logger)
            if html:
                all_data.append(self.parse(html))
                save_to_file(all_data, self.output_file, self.logger)
                self.logger.info(f"All data saved to {self.output_file}")
            else:
                self.logger.error(f"Failed to fetch content from {self.url}")
