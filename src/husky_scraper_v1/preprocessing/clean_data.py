import re
from bs4 import BeautifulSoup


def clean_course_data(course):
    # Clean description
    description = course.get('Description', '')
    course['Description'] = clean_text(description)

    # Clean catalog details
    catalog_details = course.get('Catalog Details', '')
    course['Catalog Details'] = clean_text(catalog_details)

    # Clean prerequisites and co-requisites if they are strings
    prerequisites = course.get('Prerequisites', '')
    if isinstance(prerequisites, str):
        course['Prerequisites'] = clean_text(prerequisites)

    co_requisites = course.get('Co-requisites', '')
    if isinstance(co_requisites, str):
        course['Co-requisites'] = clean_text(co_requisites)

    # Add any additional cleaning steps here

    return course


def clean_text(text):
    # Remove HTML tags
    soup = BeautifulSoup(text, 'lxml')
    cleaned_text = soup.get_text(separator='.', strip=True)
    # Normalize whitespace
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    return cleaned_text
