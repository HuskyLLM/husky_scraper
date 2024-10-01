import requests
from bs4 import BeautifulSoup
import logging
import json
from utils import setup_logging, load_json_file

# Set up logging
logger = setup_logging('../../logs/faculty_scraper.log')


# Function to scrape faculty details from a given URL
def scrape_faculty_page(url, faculty_data):
    logger.info(f"Scraping faculty from: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all faculty blocks with the <p> tag and class 'keeptogether'
    faculty_blocks = soup.find_all('p', class_='keeptogether')

    # Loop through each faculty block and extract relevant information
    for faculty in faculty_blocks:
        # Extract the name from the <strong> tag
        name_tag = faculty.find('strong')
        name = name_tag.text.strip() if name_tag else "No name available"

        # Extract the title and department from the remaining text
        title_and_department = faculty.get_text(separator=" ").replace(name, "").strip()

        # Append the data to the faculty_data list
        faculty_data.append({
            "Name": name,
            "Title and Department": title_and_department
        })

    logger.info(f"Finished scraping {len(faculty_blocks)} faculty members from {url}.\n")


# Function to scrape all faculty from multiple URLs
def scrape_all_faculty(urls):
    # Lists to store the faculty data
    faculty_data = []

    # Loop through each URL and scrape the faculty members
    for i, url in enumerate(urls):
        logger.info(f"Scraping faculty page {i + 1}/{len(urls)}: {url}")
        scrape_faculty_page(url, faculty_data)

    # Save the faculty data to a JSON file
    output_file = '../../results/northeastern_faculty_members.json'
    with open(output_file, 'w') as json_file:
        json.dump(faculty_data, json_file, indent=4)

    logger.info(f"All faculty scraping done! Data has been saved to {output_file}.")


# Main function to load the URLs from the config and scrape faculty members
def run_faculty_scraper():
    # Load the config.json file
    config = load_json_file("../../configs/config.json",logger)

    # Extract the URLs from the config for faculty members
    faculty_urls = config["scraping_tasks"]["faculty_members"]["urls"]

    # Run the scraping process for the faculty URLs
    scrape_all_faculty(faculty_urls)


# Run the function when this script is called directly
if __name__ == "__main__":
    run_faculty_scraper()
