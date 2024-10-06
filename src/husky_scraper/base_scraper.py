from abc import ABC, abstractmethod
from src.husky_scraper.utils import fetch_html, save_to_file


class BaseScraper(ABC):
    """
    Abstract base class for all scrapers. Defines the structure for scrapers to follow.
    """

    def __init__(self, url: str, output_file: str, logger) -> None:
        """
        Initializes the scraper.

        Args:
            url (str): The URL to scrape.
            output_file (str): The file to save the scraped content to.
            logger: The logger instance for logging.
        """
        self.url = url
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
        Fetches the HTML content, parses it using the `parse` method,
        and saves the parsed content to the specified output file.
        """
        self.logger.info(f"Starting scraping for URL: {self.url}")
        html = fetch_html(self.url, self.logger)
        if html:
            parsed_content = self.parse(html)
            save_to_file(parsed_content, self.output_file, self.logger)
            self.logger.info(f"Scraping successful. Data saved to {self.output_file}")
        else:
            self.logger.error(f"Failed to fetch content from {self.url}")
