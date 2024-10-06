from src.husky_scraper.undergrad.admissions.undergrad_admissions_requirements import UndergradAdmissionRequirements, \
    UndergradMilitaryRequirements, \
    UndergradJohnMartinsonRequirements, UndergradSpecializedEntry
from src.husky_scraper.undergrad.entering_students_info.accommodation_scraper import Accommodation
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
    '''course_task = config['scraping_tasks'].get('course_description')
    if course_task:
        logger.info(f"Scraping course descriptions from {course_task['urls']}")
        scraper = CourseScraper(course_task['urls'], course_task['output_file'], logger)
        scraper.scrape()

    # Scrape faculty members
    faculty_task = config['scraping_tasks'].get('faculty_members')
    if faculty_task:
        logger.info(f"Scraping faculty members from multiple URLs")
        scraper = FacultyScraper(faculty_task['urls'], faculty_task['output_file'], logger)
        scraper.scrape()

    # Scrape accreditation info
    accreditation_task = config['scraping_tasks'].get('accreditation')
    if accreditation_task:
        logger.info(f"Scraping accreditation info from {accreditation_task['urls'][0]}")
        scraper = AccreditationScraper(accreditation_task['urls'][0], accreditation_task['output_file'],
                                                     logger)
        scraper.scrape()'''

    # Scrape undergrad info
    undergrad_academic_requirements = config['scraping_tasks'].get('undergrad_academic_requirements')
    if undergrad_academic_requirements:
        logger.info(f"Scraping Undergrad Admission info from {undergrad_academic_requirements['urls'][0]}")
        scraper = UndergradAdmissionRequirements(undergrad_academic_requirements['urls'][0],
                                                 undergrad_academic_requirements['output_file'],
                                                 logger)
        scraper.scrape()

    # Scrape undergrad info
    undergrad_conditional_admission = config['scraping_tasks'].get('undergrad_conditional_admission')
    if undergrad_academic_requirements:
        logger.info(f"Scraping Undergrad Admission info from {undergrad_conditional_admission['urls'][0]}")
        scraper = UndergradAdmissionRequirements(undergrad_conditional_admission['urls'][0],
                                                 undergrad_conditional_admission['output_file'],
                                                 logger)
        scraper.scrape()

    # Scrape undergrad info
    undergrad_military_admission = config['scraping_tasks'].get('undergrad_military_admission')
    if undergrad_academic_requirements:
        logger.info(f"Scraping Undergrad Admission info from {undergrad_military_admission['urls'][0]}")
        scraper = UndergradMilitaryRequirements(undergrad_military_admission['urls'][0],
                                                undergrad_military_admission['output_file'],
                                                logger)
        scraper.scrape()

    # Scrape undergrad info
    undergrad_john_martinson_admission = config['scraping_tasks'].get('undergrad_john_martinson_admission')
    if undergrad_john_martinson_admission:
        logger.info(f"Scraping Undergrad Admission info from {undergrad_john_martinson_admission['urls'][0]}")
        scraper = UndergradJohnMartinsonRequirements(undergrad_john_martinson_admission['urls'][0],
                                                     undergrad_john_martinson_admission['output_file'],
                                                     logger)
        scraper.scrape()

    # Scrape undergrad info
    specialized_entry_programs = config['scraping_tasks'].get('specialized_entry_programs')
    if specialized_entry_programs:
        logger.info(f"Scraping Undergrad Admission info from {specialized_entry_programs['urls'][0]}")
        scraper = UndergradSpecializedEntry(specialized_entry_programs['urls'][0],
                                            specialized_entry_programs['output_file'],
                                            logger)
        scraper.scrape()

    # Scrape undergrad info
    disability_accommodation = config['scraping_tasks'].get('disability_accommodation')
    if disability_accommodation:
        logger.info(f"Scraping Undergrad Admission info from {disability_accommodation['urls'][0]}")
        scraper = Accommodation(disability_accommodation['urls'][0],
                                disability_accommodation['output_file'],
                                logger)
        scraper.scrape()


if __name__ == "__main__":
    main()
