from src.husky_scraper_v3.undergrad.admissions.scraper import UndergradAdmissionRequirements, \
    UndergradMilitaryRequirements, \
    UndergradJohnMartinsonRequirements, UndergradSpecializedEntry
from src.husky_scraper_v3.undergrad.entering_students_info.scraper import EnteringStudentsInfo
from src.husky_scraper_v3.undergrad.financial_information.scraper import FinancialInformation, TuitionRoomBoardFeesScraper
from src.husky_scraper_v3.undergrad.academic_policies.scraper import AcademicPolicies
from utils import load_from_file
from logging_util import LoggerFactory
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict


def run_scraper(scraper_class, config_task, logger, task_name):
    """
    Runs the scraper for a specific task if the task is present in the config.
    """
    if not config_task:
        logger.warning(f"Skipping {task_name}, no configuration found.")
        return
    try:
        logger.info(f"Scraping {task_name} info from {config_task['urls'][0]}")
        scraper = scraper_class(config_task['urls'][0], config_task['output_file'], logger)
        scraper.scrape()
    except Exception as e:
        logger.error(f"Error occurred during scraping {task_name}: {str(e)}")


def run_scraper_batch(scraper_class, tasks, config, logger):
    """
    Runs a batch of scraping tasks using the same scraper class.
    """
    logger.info(f"Running batch for scraper class {scraper_class.__name__}")
    print(config.keys())
    try:
        for task_name in tasks:
            config_task = config['scraping_tasks'].get(task_name)
            run_scraper(scraper_class, config_task, logger, task_name)
    except Exception as e:
        logger.error(f"Error in batch execution for {scraper_class.__name__}: {str(e)}")


def main() -> None:
    """
    Main function to orchestrate the scraping process by loading the config
    and executing the appropriate scrapers concurrently.
    """
    logger = LoggerFactory.get_logger("MainScraper")
    logger.info("Starting the scraping process...")

    # Load scraping tasks from scraper_config.json
    config = load_from_file('../../configs/scraper_config.json', logger)

    # Log the loaded config for debugging
    logger.info(f"Config loaded: {config}")

    if config is None:
        logger.error("Failed to load the configuration file.")
        return

    # Check for scraping_tasks key in the config
    if 'scraping_tasks' not in config or config['scraping_tasks'] is None:
        logger.error("scraping_tasks not found in the config.")
        return

    # Print the loaded config structure for debugging
    logger.info(f"Scraping tasks found: {config['scraping_tasks']}")

    scraping_tasks = defaultdict(lambda: None, config['scraping_tasks'])

    # List of tasks categorized by their scraper class
    scraping_batches = [
        (AcademicPolicies, ['undergrad_academic_requirements', 'undergrad_conditional_admission']),
        (AcademicPolicies, ['undergrad_military_admission']),
        (AcademicPolicies, ['undergrad_john_martinson_admission']),
        (AcademicPolicies, ['specialized_entry_programs']),
        (AcademicPolicies,
         ['disability_accommodation', 'family_programs', 'residential_life', 'health_requirements_uhcs',
          'international', 'information_technology_services', 'office_of_the_registrar', 'nupd',
          'student_orientation', 'we_care']),
        (AcademicPolicies, ['bill_payment', 'financial_aid', 'financing_options']),
        (AcademicPolicies, ['tuition_room_board']),
        (
            AcademicPolicies,
            [
                'academic_integrity', 'academic_consequences_violating_integrity', 'attendance_requirements',
                'campus_transfer', 'clearing_academic_deficiency', 'student_conduct', 'course_credit_guidelines',
                'course_numbering', 'grade_change_policy', 'student_records_transcripts', 'leaves_of_absence',
                'personal_information', 'incomplete_grade_policy', 'retaking_courses',
                'student_rights_responsibilities',
                'ferpa', 'student_responsibility_statement', 'student_right_to_know_act', 'substituting_courses',
                'university_sponsored_travel', 'academic_appeals', 'honors', 'progression_standards',
                'cooperative_education', 'degrees_majors_minors', 'drop_class', 'final_exams_policy',
                'graduation_requirements'
            ]
        )
    ]

    # Process each scraper batch sequentially
    for scraper_class, tasks in scraping_batches:
        run_scraper_batch(scraper_class, tasks, config, logger)


if __name__ == "__main__":
    main()