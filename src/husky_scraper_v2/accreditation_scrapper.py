import requests
from bs4 import BeautifulSoup
import json
import logging
from src.husky_scraper.utils import setup_logging, load_json_file

# Set up logging
logger = setup_logging('../../logs/accreditation_scraper.log')


# Function to scrape accreditation details from a given URL
def scrape_accreditation_page(url, accreditation_data):
    logger.info(f"Scraping accreditation data from: {url}")

    # Send a GET request to the page
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 200:
        logger.error(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the main accreditation content
    content = soup.find('div', id='textcontainer')

    if not content:
        logger.error(f"No accreditation information found on {url}")
        return

    # Extract all sections of the page (colleges, schools, and departments)
    headers = content.find_all('h2')  # College/Department names are in <h2> tags

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

                accreditation_data.append({
                    "College": college_name,
                    "Program": program,
                    "Accrediting Agency": accrediting_agency
                })

    logger.info(f"Extracted accreditation data from {url}.")


# Function to scrape all accreditation details from multiple URLs
def scrape_all_accreditation(urls, config):
    accreditation_data = []

    for i, url in enumerate(urls):
        logger.info(f"Scraping accreditation page {i + 1}/{len(urls)}: {url}")
        scrape_accreditation_page(url, accreditation_data)

    # Save the scraped data to a JSON file
    output_file = f'../../results/{config["scraping_tasks"]["accreditation"]["output_file"]}.json'
    with open(output_file, 'w') as json_file:
        json.dump(accreditation_data, json_file, indent=4)

    logger.info(f"All accreditation scraping done! Data has been saved to {output_file}.")


# Main function to load URLs from config and run the scraper
def run_accreditation_scraper():
    # Load the config.json file
    config = load_json_file("../../configs/scraper_config.json", logger)

    # Extract the URLs from the config for accreditation pages
    accreditation_urls = config["scraping_tasks"]["accreditation"]["urls"]

    # Run the scraping process for the URLs
    scrape_all_accreditation(accreditation_urls, config)


# Run the scraper when the script is executed directly
if __name__ == "__main__":
    run_accreditation_scraper()
