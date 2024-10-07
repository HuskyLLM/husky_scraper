from bs4 import BeautifulSoup
from src.husky_scraper_v3.base_scraper import BaseScraper
import re
from src.husky_scraper_v3.utils import fetch_html, save_to_file, replace_unicode


class UndergradAdmissionRequirements(BaseScraper):
    """
    Scraper for extracting course descriptions from the course catalog page.
    """

    def parse(self, html: str) -> dict[str, str]:
        self.logger.info("Parsing course descriptions.")

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Locate the main content container
        content_section = soup.find('div', {'id': 'textcontainer'})
        data = {}

        if content_section:
            current_heading = None
            content_list = []

            # Find all paragraphs and lists in the content container
            for element in content_section.find_all(['h2', 'h3', 'h4', 'p', 'ul']):
                if element.name in ['h2', 'h3', 'h4']:
                    if current_heading and content_list:
                        # Save previous heading and its content
                        data[current_heading] = ' '.join(content_list)
                    # Set the new heading
                    current_heading = element.text.strip()
                    content_list = []  # Reset content for the new heading
                elif element.name == 'p':
                    # Add paragraph text
                    content_list.append(element.text.strip().replace("\n", " "))
                elif element.name == 'ul':
                    # Add list items (bullet points)
                    bullet_points = [li.text.strip() for li in element.find_all('li')]
                    content_list.append(" ".join(bullet_points))

            # Add the last heading and content
            if current_heading and content_list:
                data[replace_unicode(current_heading)] = replace_unicode(' '.join(content_list))

        return data


class UndergradMilitaryRequirements(BaseScraper):
    """
    Scraper for extracting course descriptions from the course catalog page.
    """

    def parse(self, html: str) -> dict[str, str]:
        self.logger.info("Parsing course descriptions.")

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Extract the title of the page
        title = soup.find('h1').text.strip()

        # Extract the content under the main section related to deferment
        main_content = soup.find('div', {'id': 'textcontainer'}).get_text(separator='.').strip()

        # Create a dictionary with the title as the key and main content as the value
        scraped_data = {replace_unicode(title): replace_unicode(main_content)}

        return scraped_data


class UndergradJohnMartinsonRequirements(BaseScraper):
    """
    Scraper for extracting course descriptions from the course catalog page.
    """

    def parse(self, html: str) -> dict[str, str]:
        self.logger.info("Parsing course descriptions.")

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Try to find the title
        title_tag = soup.find('h1')
        if title_tag is None:
            print("Error: <h1> tag not found.")
            return {}

        title = title_tag.text.strip()

        # Extract the content under the main section related to the John Martinson Honors Program
        main_content_section = soup.find('div', {'id': 'textcontainer'})
        if main_content_section is None:
            print("Error: Main content section not found!")
            return {}

        # Extract all the text content and replace \n with space and &nbsp; with space
        full_content = main_content_section.get_text(separator='.', strip=True).replace('\n', ' ').replace('\xa0', ' ')

        # Extract phone numbers (matching patterns like 617.373.2333 or 617-373-2333)
        phone_numbers = re.findall(r'\(?\d{3}\)?[\.\-\s]\d{3}[\.\-\s]\d{4}', full_content)

        # Extract email addresses
        email_addresses = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', full_content)

        # Extract names of Director and Associate Directors, replace \n with space and &nbsp;
        director_names = []
        for p_tag in main_content_section.find_all('p'):
            text = p_tag.get_text(separator='.').strip().replace('\n', ' ').replace('\xa0', ' ')
            if "Director" in text or "Associate Director" in text:
                director_names.append(text)

        # Create a dictionary with the extracted data
        scraped_data = {
            "Title": replace_unicode(title),
            "Phone Numbers": phone_numbers,
            "Email Addresses": email_addresses,
            "Director and Associate Director Names": director_names,
            "Full Content": replace_unicode(full_content)  # Full content with \n and &nbsp; replaced by spaces
        }

        return scraped_data


class UndergradSpecializedEntry(BaseScraper):
    """
    Scraper for extracting course descriptions from the course catalog page.
    """

    def parse(self, html: str) -> dict[str, str]:
        self.logger.info("Parsing course descriptions.")

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Extract the title
        title_tag = soup.find('h1')
        title = title_tag.text.strip() if title_tag else "No title found"

        # Extract the main content container
        content_section = soup.find('div', {'id': 'textcontainer'})
        if not content_section:
            print("Main content not found!")
            return {}

        # Extract the first paragraph
        first_paragraph = content_section.find('p').get_text(strip=True) if content_section.find(
            'p') else "No first paragraph found"

        # Extract the individual specialized programs
        programs = {}

        # Find all h2 headers and their corresponding paragraphs
        for header in content_section.find_all('h2'):
            program_title = header.text.strip()
            program_details = []
            for sibling in header.find_next_siblings():
                # Stop when another h2 or hr (horizontal rule) is encountered
                if sibling.name == 'h2' or sibling.name == 'hr':
                    break
                # Collect the text of relevant paragraphs
                program_details.append(sibling.get_text(strip=True))
            programs[replace_unicode(program_title)] = replace_unicode(' '.join(program_details))

        # Create a dictionary with the scraped data
        scraped_data = {
            "Title": title,
            "First Paragraph": first_paragraph,
            "Programs": programs
        }

        return scraped_data
