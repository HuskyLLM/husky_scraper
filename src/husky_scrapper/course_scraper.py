import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import json
import logging
from utils import setup_logging

# Set up logging
logger = setup_logging('../../logs/course_scraper.log')

# Base URL for the website
base_url = "https://catalog.northeastern.edu/course-descriptions/"


# Function to clean the course title and extract hours (handling cases like '1-4 Hours')
def clean_course_title_and_hours(title):
    # Modify the regex to capture ranges of hours (e.g., '1-4 Hours' or '4 Hours')
    hours_match = re.search(r'\((\d+-\d+|\d+)\s*Hours\)', title)
    hours = hours_match.group(1) if hours_match else "No hours available"

    # Remove the hours part from the title
    cleaned_title = re.sub(r'\s*\(.*?\)\s*$', '', title)

    return cleaned_title, hours


# Function to scrape course details from each link
def scrape_course_page(url, course_data):
    logger.info(f"Scraping courses from: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all course blocks
    courses = soup.find_all('div', class_='courseblock')

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
        course_data.append({
            "Course Title": cleaned_title,
            "Description": description,
            "Prerequisites": prereq,
            "Hours": hours
        })

    logger.info(f"Finished scraping {len(courses)} courses from {url}.\n")


# Function to scrape all courses from the main page
def scrape_all_courses():
    # Notify that the request is being sent to the base URL
    logger.info(f"Fetching main page: {base_url}")
    response = requests.get(base_url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all anchor tags (<a>) for departments and extract href attributes
    links = []
    for a_tag in soup.find_all('a', href=True):
        link = a_tag['href']
        # Filter for only course description links
        if 'course-descriptions' in link and link not in links:
            links.append(link)

    logger.info(f"Found {len(links)} department links.")

    # Full URLs for the course pages
    full_urls = [f"https://catalog.northeastern.edu{link}" for link in links]

    # Lists to store the course data
    course_data = []

    # Loop through each department link and scrape the courses
    for i, url in enumerate(full_urls):
        logger.info(f"Scraping department {i + 1}/{len(full_urls)}: {url}")
        scrape_course_page(url, course_data)

    # Save the course data to a JSON file
    output_file = '../../results/northeastern_course_descriptions.json'
    with open(output_file, 'w') as json_file:
        json.dump(course_data, json_file, indent=4)

    logger.info(f"All scraping done! Data has been saved to {output_file}.")


# Run the function when this script is called directly
if __name__ == "__main__":
    scrape_all_courses()