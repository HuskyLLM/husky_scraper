from course_scraper import CourseScraper
from faculty_scraper import FacultyScraper
from accreditation_scrapper import AccreditationScraper
from utils import load_from_file
from logging_util import LoggerFactory


def main() -> None:
    """
    Main function to orchestrate the scraping process by loading the config
    and executing the appropriate scrapers.
    """
    logger = LoggerFactory.get_logger("MainScraper")
    logger.info("Starting the scraping process...")

    # Load scraping tasks from scraper_config.json
    config = load_from_file('../../configs/scraper_config.json', logger)
    print(config)
    # Scrape course descriptions
    course_task = config['scraping_tasks'].get('course_description')
    if course_task:
        logger.info(f"Scraping course descriptions from {course_task['urls']}")
        course_scraper = CourseScraper(course_task['urls'], course_task['output_file'], logger)
        course_scraper.scrape()

    # Scrape faculty members
    faculty_task = config['scraping_tasks'].get('faculty_members')
    if faculty_task:
        logger.info(f"Scraping faculty members from multiple URLs")
        faculty_scraper = FacultyScraper(faculty_task['urls'], faculty_task['output_file'], logger)
        faculty_scraper.scrape()

    # Scrape accreditation info
    accreditation_task = config['scraping_tasks'].get('accreditation')
    if accreditation_task:
        logger.info(f"Scraping accreditation info from {accreditation_task['urls'][0]}")
        accreditation_scraper = AccreditationScraper(accreditation_task['urls'][0], accreditation_task['output_file'],
                                                     logger)
        accreditation_scraper.scrape()


if __name__ == "__main__":
    main()
