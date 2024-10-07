from typing import List, Any, Dict
from bs4 import BeautifulSoup
from from src.husky_scraper_v3.base_scraper import BaseScraper
from src.husky_scraper_v3.utils import replace_unicode


class AccreditationScraper(BaseScraper):
    """
    Scraper for extracting accreditation information from the accreditation page.
    """

    def parse(self, html: str) -> list[Any] | list[dict[str, str | Any]]:
        """
        Parses accreditation information from the HTML content.

        Args:
            html (str): The HTML content fetched from the URL.

        Returns:
            List[str]: A list of strings containing the accreditation details.
        """
        self.logger.info("Parsing accreditation information.")
        soup = BeautifulSoup(html, 'html.parser')
        accreditation_section = soup.find('div', id='textcontainer')
        accreditation_content = []

        # Extract all sections of the page (colleges, schools, and departments)
        headers = accreditation_section.find_all('h2')  # College/Department names are in <h2> tags

        # Loop through each section and extract accreditation info
        for header in headers:
            college_name = header.get_text().strip()

            # Find the table following the header
            table = header.find_next('table', class_='tbl_Accreditation')
            if table:
                rows = table.find_all('tr')

                for row in rows[1:]:  # Skipping the header row
                    columns = row.find_all('td')
                    program = columns[0].get_text(strip=True)
                    accrediting_agency = columns[1].get_text(strip=True)

                    accreditation_content.append({
                        "College": replace_unicode(college_name),
                        "Program": replace_unicode(program),
                        "Accrediting Agency": replace_unicode(accrediting_agency)
                    })

        self.logger.info(f"Parsed {len(accreditation_content)} accreditation paragraphs.")
        return accreditation_content
