from bs4 import BeautifulSoup
from src.husky_scraper.base_scraper import BaseScraper
from src.husky_scraper.utils import fetch_html, save_to_file, replace_unicode
from src.husky_scraper.general_information.course_scraper import clean_course_title_and_hours
import re


class UndergradScraper(BaseScraper):
    """
    Scraper for extracting program details, including headings, paragraphs, table data, and links,
    with a single contact_info key for storing emails, phone numbers, and hyperlinks.
    It also captures paragraphs and bullet points that are not associated with headers.
    """

    def parse(self, html: str, url: str) -> dict[str, str]:
        self.logger.info("Parsing program details.")

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Extract the title of the page
        title = soup.find('title').get_text(strip=True)

        # Define containers for the sections to be scraped
        sections_to_scrape_1 = {
            "Army ROTC Program": ['armyrotcprogramtextcontainer'],
            "Navy ROTC Program": ['navyrotcprogramtextcontainer'],
            "Air Force ROTC Program": ['airforcerotcprogramtextcontainer'],
            "Overview": ['textcontainer','overviewtextcontainer'],
            # "Courses": ['coursestextcontainer'],
            "Chair Persons": ["chairstextcontainer"],
            "Programs": ['programrequirementstextcontainer','programstextcontainer'],
            "Minor Requirements": ['newitemtextcontainer','minorrequirementstextcontainer'],
            "Major Requirements": ["majorrequirementstextcontainer"],
            "Plan of Study": ["planofstudytextcontainer"],
            'Communication Sciences and Disorders': ['communicationsciencesanddisorderstextcontainer'],
            'Medical Sciences': ['medicalsciencestextcontainer'],
            'Physical Therapy, Movement, and Rehabilitation Sciences': ['physicaltherapymovementandrehabilitationsciencestextcontainer']
        }

        content_dict = {}  # Initialize dictionary to hold content
        contact_info = {'emails': [], 'phone_numbers': [], 'hyperlinks': []}  # Initialize global contact info
        content_dict['url'] = url
        # Loop through each section and extract content
        for section_name, container_id in sections_to_scrape_1.items():
            for ids in container_id:
                section = soup.find('div', {'id': ids})
                if section:
                    content_dict[section_name] = self.extract_content(section, contact_info)

        # Return the parsed information as a dictionary
        return {
            title: {
                'Content': content_dict,
                'contact_info': contact_info  # Single global contact_info with emails, phone numbers, and hyperlinks
            }
        }

    def extract_content(self, section, contact_info: dict) -> dict:
        """
        Extracts headings, paragraphs, tables, courses, and bullet points from the given section.
        Also captures links, emails, and phone numbers globally within contact_info.
        Content without headings will be placed under a "General Content" section.

        Args:
            section: BeautifulSoup element representing the section to extract.
            contact_info: Dictionary to store the global emails, phone numbers, and hyperlinks.

        Returns:
            dict: A dictionary of headings with their corresponding content (bullet points, paragraphs, tables, courses).
        """
        content = {}
        current_heading = None  # Initialize current heading as None
        found_courses = False  # Flag to check if courses are found

        # Fallback key for content that does not have an associated heading
        if "General Content" not in content:
            content["General Content"] = []

        for tag in section.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'table', 'div', 'ul', 'ol']):
            # If the tag is a heading, start a new section
            if tag.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                current_heading = replace_unicode(tag.get_text(strip=True))
                if current_heading not in content:
                    content[current_heading] = []  # Ensure the heading exists in the dictionary

            elif tag.name == 'table':
                # Extract table data
                table_data = []
                rows = tag.find_all('tr')
                for row in rows:
                    columns = [replace_unicode(col.get_text(strip=True)) for col in row.find_all(['th', 'td'])]
                    table_data.append(columns)
                if current_heading:  # Ensure heading exists before appending content
                    content[current_heading].append({"Table": table_data})
                else:
                    content["General Content"].append({"Table": table_data})  # Append to "General Content" if no heading exists

            elif tag.name == 'div' and 'courseblock' in tag.get('class', []):
                # Extract course data if the tag has 'courseblock' class
                title = tag.find('p', class_='courseblocktitle').text.strip()
                cleaned_title, hours = clean_course_title_and_hours(title)  # Clean the title and extract hours

                # Check if description exists
                description_tag = tag.find('p', class_='cb_desc')
                description = description_tag.text.strip() if description_tag else "No description available"

                # Check if prerequisites exist
                prereq_tag = tag.find('p', class_='courseblockextra')
                prereq = prereq_tag.text.strip() if prereq_tag else "No prerequisites available"

                # Append the course data
                course_data = {
                    "Course Title": replace_unicode(cleaned_title),
                    "Description": replace_unicode(description),
                    "Prerequisites": replace_unicode(prereq),
                    "Hours": hours
                }
                if current_heading:
                    content[current_heading].append(course_data)
                else:
                    content["General Content"].append(course_data)  # Append to "General Content" if no heading exists
                found_courses = True  # Mark that courses are found

            elif tag.name == 'div' and not found_courses:
                # Handle div elements with a specific class or condition
                div_content = replace_unicode(tag.get_text(separator=" ").strip())

                # Collect links within the div
                for a_tag in tag.find_all('a', href=True):
                    link_text = replace_unicode(a_tag.get_text(strip=True))
                    link_href = a_tag['href']
                    if '.' in link_href:
                        contact_info['hyperlinks'].append({'text': link_text, 'url': link_href})

                # Ensure div content is added under the correct heading
                if current_heading:
                    content[current_heading].append(div_content)
                else:
                    content["General Content"].append(div_content)  # Append to "General Content" if no heading exists

            elif tag.name == 'p' and not found_courses:  # Only process paragraphs if no courses are found
                # Add paragraphs under the current heading
                paragraph = replace_unicode(tag.get_text(separator=" ").strip())

                # Collect links within the paragraph
                for a_tag in tag.find_all('a', href=True):
                    link_text = replace_unicode(a_tag.get_text(strip=True))
                    link_href = a_tag['href']
                    if '.' in link_href:
                        contact_info['hyperlinks'].append({'text': link_text, 'url': link_href})

                # Append the paragraph under the correct heading
                if current_heading:
                    content[current_heading].append(paragraph)
                else:
                    content["General Content"].append(paragraph)  # Append to "General Content" if no heading exists

            elif tag.name in ['ul', 'ol'] and current_heading:  # Handle unordered or ordered lists (bullet points) under a valid heading
                bullet_points = []
                for li in tag.find_all('li'):
                    bullet_text = replace_unicode(li.get_text(strip=True))

                    # Capture links within bullet points
                    bullet_links = []
                    for a_tag in li.find_all('a', href=True):
                        link_text = replace_unicode(a_tag.get_text(strip=True))
                        link_href = a_tag['href']
                        if '.' in link_href:
                            bullet_links.append({'text': link_text, 'url': link_href})
                            contact_info['hyperlinks'].append({'text': link_text, 'url': link_href})

                    bullet_points.append({'text': bullet_text, 'links': bullet_links})

                # Append bullet points under the correct heading
                if current_heading:
                    content[current_heading].append(bullet_points)
                else:
                    content["General Content"].append(bullet_points)  # Append to "General Content" if no heading exists

        # Add extracted emails and phone numbers to the global contact_info
        for email in re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', section.get_text()):
            if email not in contact_info['emails']:
                contact_info['emails'].append(email)

        for phone_number in re.findall(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', section.get_text()):
            if phone_number not in contact_info['phone_numbers']:
                contact_info['phone_numbers'].append(phone_number)

        return content
