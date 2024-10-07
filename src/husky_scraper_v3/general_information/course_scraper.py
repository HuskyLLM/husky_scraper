from typing import List, Dict
from bs4 import BeautifulSoup
from from src.husky_scraper_v3.base_scraper import BaseScraper
import re
from src.husky_scraper_v3.utils import fetch_html, save_to_file, replace_unicode


def clean_course_title_and_hours(title):
    # Modify the regex to capture ranges of hours (e.g., '1-4 Hours' or '4 Hours')
    hours_match = re.search(r'\((\d+-\d+|\d+)\s*Hours\)', title)
    hours = hours_match.group(1) if hours_match else "No hours available"

    # Remove the hours part from the title
    cleaned_title = re.sub(r'\s*\(.*?\)\s*$', '', title)
    return cleaned_title, hours


class CourseScraper(BaseScraper):
    """
    Scraper for extracting course descriptions from the course catalog page.
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
        Parses course descriptions from the HTML content.

        Args:
            html (str): The HTML content fetched from the URL.

        Returns:
            List[Dict[str, str]]: A list of dictionaries containing course details.
        """
        self.logger.info("Parsing course descriptions.")
        soup = BeautifulSoup(html, 'html.parser')

        # Find all course blocks
        courses = soup.find_all('div', class_='courseblock')
        course_list = []

        # Loop through each course and extract the title, description, prerequisites, and hours
        for course in courses:
            title = course.find('p', class_='courseblocktitle').text.strip()
            cleaned_title, hours = clean_course_title_and_hours(title)  # Clean the title and extract hours

            # Check if description exists
            description_tag = course.find('p', class_='cb_desc')
            description = description_tag.text.strip() if description_tag else "No description available"

            # Check if prerequisites exist
            prereq_tag = course.find('p', class_='courseblockextra')
            prereq = prereq_tag.text.strip() if prereq_tag else "No prereq available"

            # Append the data to the course_data list
            course_list.append({
                "Course Title": replace_unicode(cleaned_title),
                "Description": replace_unicode(description),
                "Prerequisites": replace_unicode(prereq),
                "Hours": hours
            })

        self.logger.info(f"Parsed {len(course_list)} courses.")
        return course_list

    def scrape(self) -> None:
        """
        Scrapes course descriptions from multiple URLs and saves the data.
        """
        # Find all anchor tags (<a>) for departments and extract href attributes
        links = []
        course_data = []
        for url in self.urls:
            self.logger.info(f"Scraping course description from {url}")
            html = fetch_html(url, self.logger)
            soup = BeautifulSoup(html, 'html.parser')
            if html:
                for a_tag in soup.find_all('a', href=True):
                    link = a_tag['href']
                    # Filter for only course description links
                    if 'course-descriptions' in link and link not in links:
                        links.append(link)
                for link in links:
                    html = fetch_html(f"https://catalog.northeastern.edu{link}", self.logger)
                    course_data.extend(self.parse(html))

        save_to_file(course_data, self.output_file, self.logger)
        self.logger.info(f"All faculty data saved to {self.output_file}")
