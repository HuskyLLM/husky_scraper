from bs4 import BeautifulSoup
from src.husky_scraper_v3.base_scraper import BaseScraper
from src.husky_scraper_v3.utils import fetch_html, save_to_file, replace_unicode
import re


class FinancialInformation(BaseScraper):
    """
    Scraper for extracting accommodation details, including headings and their respective paragraphs.
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

        # Find all heading and content tags (h1-h6, p, ul, ol) to capture headings and associated paragraphs
        content_tags = main_content_tag.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'ul', 'ol'])

        # Initialize dictionary to hold the content and ensure "Content" exists
        content_dict = {"Content": []}
        current_heading = "Content"  # Default heading if none is found
        links = {}

        # Loop over the content and associate paragraphs with headings
        for tag in content_tags:
            # If the tag is a heading, use it as the current key
            if tag.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                current_heading = replace_unicode(tag.get_text(strip=True))
                #if current_heading not in content_dict:
                content_dict[replace_unicode(current_heading)] = []  # Ensure the heading exists in the dictionary
            else:
                # If it's a paragraph or list, add it under the current heading
                text = tag.get_text(separator=" ").strip()
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
            content_dict[replace_unicode(key)] = replace_unicode(" ".join(value))

        # Return the parsed information as a dictionary
        return {
            title: {
                'Phone Numbers': phone_numbers,
                'Email Addresses': email_addresses,
                'Content': content_dict,  # Content organized by heading
                'Links in Content': links  # Captured links within paragraphs
            }
        }


class TuitionRoomBoardFeesScraper(BaseScraper):
    """
    Scraper for extracting tuition, room, board, and fees details per semester from the university page, including headings, paragraphs, and tables.
    """

    def parse(self, html: str) -> dict[str, str]:
        self.logger.info("Parsing tuition, room, board, and fees details, including tables.")

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Extract the title of the page
        title = soup.find('title').get_text(strip=True)

        # Extract phone numbers using regex (if any)
        phone_numbers = re.findall(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', soup.get_text())

        # Extract email addresses using regex (if any)
        email_addresses = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', soup.get_text())

        # Extract the main content div where the fee information is stored
        main_content_tag = soup.find('div', {'id': 'textcontainer'})

        # Find all <p>, <h2>, <h3>, <ul>, <ol>, <table> tags to capture paragraphs, headings, bullet points, and tables
        content_parts = main_content_tag.find_all(['p', 'h2', 'h3', 'ul', 'ol', 'table'])

        # Initialize a dictionary to store extracted content
        content_dict = {}

        # Initialize a variable to track the current heading, with a default "Content"
        current_heading = "Content"
        content_dict[current_heading] = []

        # Loop over the content parts and categorize them by heading
        for part in content_parts:
            # If the tag is a heading (<h2>, <h3>), update the current heading
            if part.name in ['h2', 'h3']:
                current_heading = part.get_text(strip=True)
                content_dict.setdefault(current_heading, [])
            elif part.name == 'table':
                # Extract table content and format it as a list of rows
                table_data = []
                rows = part.find_all('tr')
                for row in rows:
                    columns = [replace_unicode(col.get_text(strip=True)) for col in row.find_all(['th', 'td'])]
                    table_data.append(columns)
                content_dict[current_heading].append({"Table": table_data})
            else:
                # Append the text to the current heading
                text = part.get_text(separator=" ").strip()

                # Extract links in the text (if any) and store them as a dictionary with text and href
                links = {a.get_text(strip=True): a['href'] for a in part.find_all('a', href=True) if '.' in a['href']}

                # Store the cleaned text and links
                content_dict.setdefault(current_heading, []).append({
                    "text": replace_unicode(text).replace("\n", " "),
                    "links": links
                })

        # Return the parsed information as a dictionary
        return {
            title: {
                'Phone Numbers': phone_numbers,
                'Email Addresses': email_addresses,
                'Main Content': content_dict
            }
        }
