from src.husky_scraper.undergrad.scraper import UndergradScraper
from src.husky_scraper.general_information.accreditation_scrapper import AccreditationScraper
from src.husky_scraper.general_information.course_scraper import CourseScraper
from src.husky_scraper.general_information.faculty_scraper import FacultyScraper
from utils import load_from_file
from logging_util import LoggerFactory
from collections import defaultdict
import traceback


def run_scraper(scraper_class, config_task, logger, task_name):
    """
    Runs the scraper for a specific task if the task is present in the config.
    """
    if not config_task:
        logger.warning(f"Skipping {task_name}, no configuration found.")
        return
    try:
        logger.info(f"Scraping {task_name} info from {config_task['urls']}")
        scraper = scraper_class(config_task['urls'], config_task['output_file'], logger)
        scraper.scrape()
    except Exception as e:
        logger.error(f"Error occurred during scraping {task_name}: {str(e)} - {traceback.format_exc()} ")


def run_scraper_batch(scraper_class, tasks, config, logger):
    """
    Runs a batch of scraping tasks using the same scraper class.
    """
    logger.info(f"Running batch for scraper class {scraper_class.__name__}")
    print(config['scraping_tasks'].keys())
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
        (AccreditationScraper, ['accreditation']),
        (CourseScraper, ['course_description']),
        (FacultyScraper, ['faculty_members']),
        (UndergradScraper,
         ['major_cip_codes', 'notifications_disclosures',
          'authorizations', 'undergrad_academic_requirements', 'undergrad_conditional_admission',
          'undergrad_military_admission', 'undergrad_john_martinson_admission', 'specialized_entry_programs',
          'disability_accommodation', 'family_programs', 'residential_life', 'health_requirements_uhcs',
          'international', 'information_technology_services', 'office_of_the_registrar', 'nupd', 'student_orientation',
          'we_care', 'bill_payment', 'financial_aid', 'financing_options', 'tuition_room_board', 'academic_integrity',
          'academic_consequences_violating_integrity', 'attendance_requirements', 'campus_transfer',
          'clearing_academic_deficiency', 'student_conduct', 'course_credit_guidelines', 'course_numbering',
          'grade_change_policy', 'student_records_transcripts', 'leaves_of_absence', 'personal_information',
          'incomplete_grade_policy', 'retaking_courses', 'student_rights_responsibilities', 'ferpa',
          'student_responsibility_statement', 'student_right_to_know_act', 'substituting_courses',
          'university_sponsored_travel', 'academic_appeals', 'honors', 'progression_standards', 'cooperative_education',
          'degrees_majors_minors', 'drop_class', 'final_exams_policy', 'graduation_requirements',
          'registration_taking_courses', 'student_evaluation_of_courses', 'army_air_force_navy_rotc',
          'education_program', 'experiential_learning', 'nu_explore', 'general_studies_program', 'global_experience',
          'honors_program', 'living_learning_program', 'nupath', 'prelaw_preparation',
          'premedical_preprofessional_health_career', 'research_creative_activity', 'service_learning', 'degrees',
          'undergraduate_internships', 'university_wide_requirements', 'world_languages_center', 'architecture_bs',
          'architectural_studies_bs', 'architectural_studies_design_bs', 'architecture_english_bs',
          'civil_engineering_architectural_studies_bsce',
          'environmental_sustainability_sciences_landscape_architecture_bs',
          'environmental_engineering_landscape_architecture_bsenve', 'landscape_architecture_bla',
          'architectural_history_minor', 'architectural_design_minor', 'architectural_science_systems_minor',
          'urban_landscape_studies_minor', 'Art BA', 'English and Design BA', 'Media Art BA',
          'Media Arts and Communication Studies BA', 'Design BFA', 'Game Art Animation BFA', 'Game Design BFA',
          'Media Arts BFA', 'Studio Art BFA', 'Architectural Studies and Design BS',
          'Behavioral Neuroscience and Design BS', 'Business Administration and Design BS',
          'Communication Studies and Design BS', 'Computer Science and Design BS',
          'Computer Science and Game Development BS', 'Computer Science and Media Arts BS',
          'Data Science and Design BS', 'Design and Mathematics BS', 'Design and Theatre BS',
          'Game Design and Music Technology BS', 'Journalism and Design BS', 'Psychology and Design BS',
          'Mechanical Engineering and Design BSME', 'Music BA', 'Music and Communication Studies - Industry BS',
          'Music Industry BS', 'Music Technology BS', 'Computer Science and Music BS',
          'Computer Science - Music Composition Technology BS', 'Electrical Engineering - Music Technology BSEE',
          'Game Design and Music Technology BS 2', 'Physics and Music BS', 'Psychology and Music BS', 'Music Minor',
          'Ethnomusicology Minor', 'Music Composition Minor', 'Music Industry Minor', 'Music Performance Minor',
          'Music Recording Minor', 'Music Technology Minor', 'Songwriting Minor', 'Performing Arts Minor',
          'Communication Studies BA', 'Communication Studies Graphic Information Design BA',
          'Communication and Media Studies BA', 'Communication Studies and Sociology BA',
          'Communication Studies and Theatre BA', 'English and Communication Studies BA',
          'Human Services and Communications BA', 'Journalism and Communication Studies BA',
          'Linguistics and Communication Studies BA', 'Media and Screen Studies BA',
          'Political Science and Communication Studies BA', 'Public Health and Communication Studies BA',
          'Africana Studies and Media and Screen Studies BA', 'Media and Screen Studies English BA',
          'Media and Screen Studies History BA', 'Media and Screen Studies Journalism BA',
          'Media and Screen Studies Media Art BA', 'Media and Screen Studies Philosophy BA',
          'Media and Screen Studies Political Science BA', 'Media and Screen Studies Sociology BA',
          'Media and Screen Studies Theatre BA', 'Media and Screen Studies Theatre BS',
          'Media Arts and Communication Studies BA 2', 'Business Administration and Communication Studies BS',
          'Communication Studies Design BS', 'Communication Studies Speech Language Pathology BS',
          'Computer Science Communication Studies BS', 'Health Science and Communication Studies BS',
          'Argumentation and Law Minor', 'Cinema Studies Minor', 'Communication Studies Minor',
          'Digital Communications Minor', 'Film Production Minor', 'Film Studies Minor', 'Human Communication Minor',
          'Improvisation Storytelling Minor', 'Media Production Minor', 'Media Screen Studies Minor',
          'Oratory and Public Speaking Minor', 'Political Communication Minor', 'Rhetoric Minor',
          'Social Activism Minor', 'Sports Media Communication Minor', 'Africana Studies and Journalism BA',
          'Journalism BA', 'Journalism and Communication Studies BA 2', 'Journalism and Cultural Anthropology BA',
          'Journalism and English BA', 'Journalism and International Affairs BA', 'Journalism and Political Science BA',
          'Journalism and Sociology BA', 'Media and Screen Studies and Journalism BA',
          'Public Health and Journalism BA', 'Public Relations BA', 'Theatre and Journalism BA',
          'Computer Science and Journalism BS', 'Criminal Justice and Journalism BS', 'Data Science and Journalism BS',
          'Economics and Journalism BS', 'Environmental Sustainability Sciences and Journalism BS',
          'Journalism and Design BS 2', 'Journalism Practice Minor', 'Journalism Studies Minor',
          'Photojournalism Minor', 'Public Relations Minor', 'Sports Media and Communication Minor',
          'Journalism and Interaction Design BS', 'Theatre BA', 'Communication Studies and Theatre BA 2',
          'Cultural Anthropology and Theatre BA', 'English and Theatre BA', 'Media Screen Studies and Theatre BA',
          'Theatre and Journalism BA 2', 'Theatre BS', 'American Sign Language and Theatre BS',
          'Computer Science and Theatre BS', 'Design and Theatre BS 2', 'Media Screen Studies and Theatre BS',
          'Performance Extended Realities BS', 'Psychology and Theatre BS', 'Theatre Minor',
          'Global Fashion Studies Minor', 'Improvisation Storytelling Minor 2', 'Performing Arts Minor 2',
          'Playwriting Minor', 'Theatre Performance and Social Change Minor', 'Theatrical Design Minor',
          'Theatre Interaction Design BA', 'Theatre Interaction Design BS',
          'Accelerated Bachelor/Graduate Degree Programs', 'Performance and Extended Realities BS',
          'Creativity in Theory and Practice Minor', "D'Amore McKim School of Business", 'Business Administration BSBA',
          'International Business BSIB', 'Business Administration and Law BS', 'Interdisciplinary Studies BS',
          'Business Administration and Communication Studies BS 2', 'Business Administration and Criminal Justice BS',
          'Business Administration and Design BS 2', 'Business Administration and Psychology BS',
          'Business Administration and Public Health BS', 'Computer Science and Business Administration BS',
          'Cybersecurity and Business Administration BS', 'Data Science and Business Administration BS',
          'Economics and Business Administration BS', 'Economics and International Business BS',
          'Health Science and Business Administration BS', 'Industrial Engineering and Business Administration BSIE',
          'International Affairs and International Business BS', 'Mathematics and Business Administration BS',
          'Political Science and Business Administration BS',
          'Politics Philosophy and Economics and Business Administration BS', 'Accounting',
          'Accounting Advisory Services', 'Brand Management', 'Business Analytics', 'Corporate Innovation',
          'Entrepreneurial Startups', 'Family Business', 'Finance', 'Fintech', 'Global Business Strategy',
          'Healthcare Management Consulting', 'International Business', 'Management', 'Management Information Systems',
          'Marketing', 'Marketing Analytics', 'Social Innovation and Entrepreneurship', 'Supply Chain Management',
          'Accounting Advisory Services Minor', 'Brand Management Minor', 'Business Administration Minor',
          'Business Analytics Minor', 'Consulting Minor', 'Corporate Innovation Minor', 'Emerging Markets Minor',
          'Entrepreneurial Startups Minor', 'Family Business Minor', 'Management Information Systems Minor',
          'Managing Human Capital Minor', 'Marketing Analytics Minor', 'Marketing Minor',
          'Social Innovation and Entrepreneurship Minor', 'Strategy Minor', 'Supply Chain Management Minor',
          'Sustainable Business Practices Minor', 'Accelerated Bachelor/Graduate Degree Programs 2', 'Khoury',
          'Computer Science', 'Cybersecurity', 'Data Science', 'Combined Majors', 'BSCS', 'BACS',
          'Computing and Law BS', 'Interdisciplinary Studies BS 2', 'Computer Science Minor', 'Cyber Security BS',
          'Data Science BS', 'Data Science Minor', 'Computer Science Behavioral Neuroscience',
          'Computer Science Biology', 'Computer Science Business Administration',
          'Computer Science Cognitive Psychology', 'Computer Science Communication Studies',
          'Computer Science Criminal Justice', 'Computer Science Design', 'Computer Science Economics',
          'Computer Science English', 'Computer Science Environmental Sustainability Sciences',
          'Computer Science Game Development', 'Computer Science History', 'Computer Science Journalism',
          'Computer Science Linguistics', 'Computer Science Mathematics', 'Computer Science Media Arts',
          'Computer Science Music', 'Computer Science Music Composition Technology', 'Computer Science Philosophy',
          'Computer Science Physics', 'Computer Science Political Science',
          'Computer Science Politics Philosophy Economics', 'Computer Science Sociology',
          'Computer Science Speech Language Pathology Audiology', 'Computer Science Theatre',
          'Cybersecurity Business Administration', 'Cybersecurity Criminal Justice', 'Cybersecurity Economics',
          'Data Science Behavioral Neuroscience', 'Data Science Biochemistry', 'Data Science Biology',
          'Data Science Business Administration', 'Data Science Chemistry', 'Data Science Criminal Justice',
          'Data Science Design', 'Data Science Ecology Evolutionary Biology', 'Data Science Economics',
          'Data Science Environmental Sustainability Sciences', 'Data Science Health Science',
          'Data Science International Affairs', 'Data Science Journalism', 'Data Science Linguistics',
          'Data Science Mathematics', 'Data Science Philosophy', 'Data Science Physics', 'Data Science Psychology',
          'Data Science Public Health', 'Data Science Speech Language Pathology Audiology',
          'Chemical Engineering Computer Science', 'Chemical Engineering Data Science',
          'Civil Engineering Computer Science', 'Computer Engineering Computer Science',
          'Environmental Engineering Data Science', 'Industrial Engineering Computer Science',
          'Mechanical Engineering Computer Science', 'Accelerated Bachelor/Graduate Degree Programs Khoury',
          'First_Year_Engineering', 'Bioengineering_BSBioE', 'Bioengineering_Biochemistry_BSBioE',
          'Chemical_Engineering_Bioengineering_BSCHE', 'Mechanical_Engineering_Bioengineering_BSME',
          'Chemical_Engineering_Biochemistry_BS', 'Chemical_Engineering_Computer_Science_BSCHE',
          'Chemical_Engineering_Data_Science_BSCHE', 'Chemical_Engineering_Environmental_Engineering_BSCHE',
          'Chemical_Engineering_Physics_BSCHE', 'Chemical_Engineering_BSCHE',
          'Environmental_Engineering_Chemical_Engineering_BSENVE', 'Biochemical_Engineering_Minor',
          'Civil_Engineering_BSCE', 'Civil_Engineering_Architectural_Studies_BSCE',
          'Civil_Engineering_Computer_Science_BSCE', 'Chemical_Engineering_Environmental_Engineering_BSCHE 2',
          'Environmental_Engineering_BSENVE', 'Environmental_Engineering_Chemical_Engineering_BSENVE 2',
          'Environmental_Engineering_Data_Science_BSENVE', 'Environmental_Engineering_Health_Sciences_BSENVE',
          'Environmental_Engineering_Landscape_Architecture_BSENVE', 'Architectural_Engineering_Minor',
          'Civil_Engineering_Minor', 'Environmental_Chemistry_Minor', 'Environmental_Engineering_Minor',
          'Electrical_Computer_Engineering_BSCMPE', 'Computer_Engineering_BSCOMPE',
          'Computer_Engineering_Computer_Science_BSCOMPE', 'Computer_Engineering_Physics_BSCOMPE',
          'Electrical_Computer_Engineering_BSEE', 'Electrical_Engineering_BSEE',
          'Electrical_Engineering_Music_Concentration_BSEE', 'Electrical_Engineering_Physics_BSEE',
          'Biomedical_Engineering_Minor', 'Computational_Data_Analytics_Minor', 'Computer_Engineering_Minor',
          'Electrical_Engineering_Minor', 'Robotics_Minor', 'BSIE',
          'Industrial_Engineering_Business_Administration_BSIE', 'Industrial_Engineering_Computer_Science_BSIE', 'BSME',
          'Mechanical_Engineering_Bioengineering_BSME 2', 'Mechanical_Engineering_Computer_Science_BSME',
          'Mechanical_Engineering_Design_BSME', 'Mechanical_Engineering_History_BSME',
          'Mechanical_Engineering_Physics_BSME', 'Aerospace_Minor', 'Biomechanical_Engineering_Minor',
          'Healthcare_System_Operations_Minor', 'Industrial_Engineering_Minor', 'Mechanical_Engineering_Minor',
          'Robotics_Minor 2', 'Design_Innovation_Engineering_Minor', 'Entrepreneurial_Engineering_Minor',
          'Global_Perspectives_Engineering_Minor', 'Materials_Science_Engineering_Minor',
          'Sustainable_Energy_Systems_Minor', 'Accelerated Bachelor/Graduate Degree Programs Engineering',
          'College_of_Science', 'Biology', 'Chemistry_and_Chemical_Biology', 'Marine_and_Environmental_Sciences',
          'Mathematics', 'Physics', 'Psychology', 'Interdisciplinary_Programs', 'Accelerated_Programs', 'Biology_BS',
          'Cell_and_Molecular_Biology_BS', 'Biology_English_BS', 'Biology_Mathematics_BS',
          'Biology_Political_Science_BS', 'Computer_Science_Biology_BS', 'Data_Science_Biology_BS', 'Biology_Minor',
          'Cell_and_Molecular_Biology_Minor', 'Science_Writing_Minor', 'Chemistry_BS', 'Data_Science_Chemistry_BS',
          'Environmental_Sustainability_Chemistry_BS', 'Chemistry_Minor', 'Environmental_Chemistry_Minor 2',
          'marine_environmental_ecology_evolutionary_biology_bs',
          'marine_environmental_environmental_sustainability_sciences_bs',
          'marine_environmental_environmental_studies_ba', 'marine_environmental_marine_biology_bs',
          'marine_environmental_marine_biology_three_seas',
          'marine_environmental_computer_science_environmental_sustainability_sciences_bs',
          'marine_environmental_data_science_ecology_evolutionary_biology_bs',
          'marine_environmental_data_science_environmental_sustainability_sciences_bs',
          'marine_environmental_environmental_sustainability_sciences_chemistry_bs',
          'marine_environmental_environmental_sustainability_sciences_economics_bs',
          'marine_environmental_environmental_sustainability_sciences_journalism_bs',
          'marine_environmental_environmental_sustainability_sciences_landscape_architecture_bs',
          'marine_environmental_environmental_studies_history_ba',
          'marine_environmental_environmental_studies_international_affairs_ba',
          'marine_environmental_environmental_studies_philosophy_ba',
          'marine_environmental_environmental_studies_political_science_ba',
          'marine_environmental_sociology_environmental_studies_ba',
          'marine_environmental_ecology_evolutionary_biology_minor',
          'marine_environmental_environmental_sustainability_sciences_minor',
          'marine_environmental_environmental_studies_minor', 'marine_environmental_geosciences_minor',
          'marine_environmental_marine_sciences_minor', 'mathematics_ba', 'mathematics_bs', 'biology_mathematics_bs',
          'computer_science_mathematics_bs', 'data_science_mathematics_bs', 'design_mathematics_bs',
          'economics_mathematics_bs', 'mathematics_business_administration_bs', 'mathematics_philosophy_bs',
          'mathematics_physics_bs 2', 'mathematics_political_science_bs', 'mathematics_psychology_bs',
          'mathematics_sociology_bs', 'mathematics_minor', 'physics_bs', 'applied_physics_bs', 'biomedical_physics_bs',
          'computer_science_physics_bs', 'data_science_physics_bs', 'mathematics_physics_bs', 'physics_music_bs',
          'physics_philosophy_bs', 'chemical_engineering_physics_bsche', 'computer_engineering_physics_bscompe',
          'electrical_engineering_physics_bsee', 'mechanical_engineering_physics_bsme', 'astrophysics_minor',
          'physics_minor', 'psychology_bs', 'american_sign_language_psychology_bs',
          'business_administration_psychology_bs', 'computer_science_cognitive_psychology_bs',
          'criminal_justice_psychology_bs', 'data_science_psychology_bs', 'economics_psychology_bs',
          'health_science_psychology_bs', 'human_services_psychology_bs', 'linguistics_psychology_bs',
          'mathematics_psychology_bs 2', 'psychology_design_bs', 'psychology_music_bs', 'psychology_theatre_bs',
          'psychology_minor', 'american_sign_language_linguistics_bs', 'behavioral_neuroscience_bs',
          'behavioral_neuroscience_design_bs', 'behavioral_neuroscience_philosophy_bs', 'biochemistry_bs',
          'bioengineering_biochemistry_bsbioe', 'chemical_engineering_biochemistry_bs',
          'computer_science_behavioral_neuroscience_bs', 'computer_science_linguistics_bs',
          'data_science_behavioral_neuroscience_bs', 'data_science_biochemistry_bs', 'data_science_linguistics_bs',
          'interdisciplinary_studies_bs', 'linguistics_bs', 'linguistics_communication_studies_ba',
          'linguistics_cultural_anthropology_bs', 'linguistics_english_ba', 'linguistics_psychology_bs 2',
          'linguistics_speech_language_pathology_bs', 'spanish_linguistics_ba',
          'speech_language_pathology_behavioral_neuroscience_bs', 'behavioral_neuroscience_minor', 'biochemistry_minor',
          'environmental_chemistry_minor', 'linguistics_minor', 'network_science_minor',
          'accelerated_bachelor_graduate_degree_programs', 'academic_policies_procedures', 'interdisciplinary ',
          'clinical_rehabilitation_sciences', 'community_health_behavioral_sciences', 'nursing', 'pharmacy',
          'code_conduct_caep', 'code_conduct_slpa', 'code_conduct_msci', 'code_conduct_pt', 'code_conduct_nurs',
          'code_conduct_sopps', 'background_checks', 'health_certification', 'liability_insurance',
          'practicum_internship_policies', 'health_science_law_bs', 'interdisciplinary_studies_bs 2',
          'public_health_law_ba', 'business_administration_public_health_bs',
          'communication_studies_speech_language_pathology_bs',
          'computer_science_speech_language_pathology_audiology_bs', 'data_science_health_science_bs',
          'data_science_public_health_bs', 'data_science_speech_language_pathology_audiology_bs',
          'environmental_engineering_health_sciences_bsenve', 'health_humanities_health_science',
          'health_humanities_public_health', 'health_science_business_administration_bs',
          'health_science_communication_studies_bs', 'health_science_psychology_bs 2', 'health_science_sociology_bs',
          'health_science_spanish_bs', 'linguistics_speech_language_pathology_bs w',
          'public_health_communication_studies_ba', 'public_health_cultural_anthropology_ba',
          'public_health_journalism_ba', 'public_health_sociology_ba', 'spanish_public_health_ba',
          'speech_language_pathology_behavioral_neuroscience_bs 2', 'speech_language_pathology_human_services_bs',
          'communication_sciences_disorders_minor', 'early_intervention_minor', 'exercise_science_minor',
          'global_health_minor', 'health_psychology_minor', 'health_sciences_entrepreneurship_minor',
          'health_humanities_society_minor', 'healthcare_system_operations_minor', 'human_movement_science_minor',
          'mindfulness_minor', 'nutrition_minor', 'pharmaceutical_sciences_minor', 'public_health_minor',
          'speech_language_pathology_audiology_minor', 'wellness_minor', 'speech_language_pathology_audiology_bs',
          'communication_studies_speech_language_pathology_bs 2',
          'computer_science_speech_language_pathology_audiology_bs 2',
          'data_science_speech_language_pathology_audiology_bs 2', 'linguistics_speech_language_pathology_bs 2',
          'speech_language_pathology_behavioral_neuroscience_bs 3', 'speech_language_pathology_human_services_bs 2',
          'communication_sciences_disorders_minor 2', 'health_sciences_entrepreneurship_minor 2',
          'human_movement_science_minor 2', 'speech_language_pathology_audiology_minor 2', 'applied_psychology_ba',
          'early_intervention_minor 2', 'health_psychology_minor 2', 'mindfulness_minor 2', 'public_health_ba',
          'public_health_law_ba 2', 'health_science_bs', 'health_science_law_bs 2', 'interdisciplinary_studies_bs 3',
          'business_administration_public_health_bs 2', 'data_science_health_science_bs 2',
          'environmental_engineering_health_sciences_bsenve 2', 'health_humanities_health_science 2',
          'health_science_business_administration_bs 2', 'health_science_communication_studies_bs 2',
          'health_science_psychology_bs 3', 'health_science_sociology_bs 2', 'health_science_spanish_bs 2',
          'health_humanities_public_health 2', 'public_health_and_communication_studies_ba 2',
          'public_health_cultural_anthropology_ba 2', 'public_health_journalism_ba 2', 'public_health_sociology_ba 2',
          'spanish_public_health_ba 2', 'exercise_science_minor 2', 'global_health_minor 2',
          'health_humanities_society_minor 2', 'healthcare_system_operations_minor 2', 'nutrition_minor 2',
          'public_health_minor 2', 'nursing_bsn', 'accelerated_second_degree_bsn', 'nursing_bsn_transfer_track',
          'wellness_minor 2', 'pharmaceutical_sciences_bs', 'pharmacy_pharmd', 'pharmaceutical_sciences_minor 2',
          'accelerated_bachelor_graduate_programs', 'social_sciences_interdisciplinary', 'criminology_criminal_justice',
          'cultures_societies_global_studies', 'economics', 'english', 'history', 'international_affairs',
          'philosophy_religion', 'political_science', 'sociology_anthropology',
          'computer_science_politics_philosophy_economics', 'global_asian_studies',
          'health_humanities_health_science 3', 'health_humanities_public_health 3', 'history_asian_studies',
          'history_culture_law', 'human_services_ba', 'human_services_bs', 'human_services_communications',
          'human_services_criminal_justice', 'human_services_international_affairs', 'human_services_sociology_ba',
          'human_services_sociology_bs', 'jewish_studies_religion', 'politics_philosophy_economics_business',
          'politics_philosophy_economics', 'speech_language_pathology_human_services',
          'computational_social_sciences_minor', 'digital_methods_in_the_humanities_minor',
          'food_systems_sustainability_health_equity_minor', 'global_asian_studies_minor',
          'health_humanities_society_minor 3', 'human_services_minor', 'jewish_studies_minor',
          'law_public_policy_minor', 'urban_studies_minor', 'womens_gender_sexuality_studies_minor',
          'criminology_criminal_justice 2', 'english_criminal_justice', 'history_criminal_justice',
          'international_affairs_criminal_justice', 'business_administration_criminal_justice',
          'criminal_justice_journalism', 'criminal_justice_philosophy', 'criminal_justice_political_science',
          'criminal_justice_psychology', 'criminal_justice_sociology', 'cybersecurity_criminal_justice',
          'data_science_criminal_justice', 'human_services_criminal_justice 2', 'criminal_justice_minor',
          'africana_studies', 'africana_studies_english', 'africana_studies_human_services',
          'africana_studies_journalism', 'africana_studies_media_and_screen_studies',
          'africana_studies_political_science', 'history_culture_law 2', 'religious_studies_africana_studies',
          'spanish', 'spanish_international_affairs', 'spanish_linguistics', 'spanish_public_health',
          'american_sign_language_english_interpreting', 'american_sign_language_human_services',
          'american_sign_language_linguistics', 'american_sign_language_psychology', 'american_sign_language_theatre',
          'health_science_spanish', 'african_american_studies_minor', 'africana_studies_minor',
          'american_sign_language_minor', 'arabic_minor', 'black_feminist_studies_minor', 'chinese_minor',
          'french_minor', 'german_minor', 'italian_minor', 'japanese_minor',
          'latinx_latin_american_caribbean_studies_minor', 'portuguese_minor', 'russian_minor', 'spanish_minor',
          'spanish_healthcare_minor', 'economics_ba', 'history_economics_ba', 'international_affairs_economics_ba',
          'political_science_economics_ba', 'economics_bs', 'computer_science_economics_bs',
          'cybersecurity_economics_bs', 'data_science_economics_bs', 'economics_business_administration_bs',
          'economics_human_services_bs', 'economics_international_business_bs', 'economics_journalism_bs',
          'economics_mathematics_bs 2', 'economics_philosophy_bs', 'economics_psychology_bs 2',
          'environmental_sustainability_sciences_economics_bs', 'history_economics_bs',
          'political_science_economics_bs', 'economics_minor', 'english_ba', 'africana_studies_english_ba',
          'english_communication_studies_ba', 'english_criminal_justice_ba', 'english_cultural_anthropology_ba',
          'english_design_ba', 'english_philosophy_ba', 'english_political_science_ba', 'english_theatre_ba',
          'history_english_ba', 'journalism_english_ba', 'linguistics_english_ba 2', 'media_screen_studies_english_ba',
          'architecture_english_bs 2', 'biology_english_bs', 'computer_science_english_bs', 'english_minor',
          'rhetoric_minor', 'writing_minor', 'history_ba', 'history_asian_studies_ba', 'history_criminal_justice_ba',
          'history_cultural_anthropology_ba', 'history_english_ba 2', 'history_economics_ba 2', 'history_philosophy_ba',
          'history_political_science_ba', 'history_religious_studies_ba', 'environmental_studies_history_ba',
          'international_affairs_history_ba', 'media_screen_studies_history_ba', 'history_bs',
          'computer_science_history_bs', 'history_economics_bs 2', 'history_minor', 'international_affairs_ba',
          'environmental_studies_international_affairs_ba', 'human_services_international_affairs_ba',
          'international_affairs_criminal_justice_ba', 'cultural_anthropology_ba', 'economics_ba 2',
          'international_affairs_history_ba 2', 'religious_studies_ba', 'journalism_international_affairs_ba',
          'political_science_international_affairs_ba', 'sociology_international_affairs_ba',
          'spanish_international_affairs_ba', 'data_science_international_affairs_bs',
          'international_affairs_international_business_bs', 'international_affairs_minor', 'middle_east_studies_minor',
          'philosophy_ba', 'religious_studies_ba 2', 'cultural_anthropology_philosophy_ba',
          'cultural_anthropology_religious_studies_ba', 'english_philosophy_ba 2',
          'environmental_studies_philosophy_ba', 'history_philosophy_ba 2', 'history_religious_studies_ba 2',
          'jewish_studies_religion_ba', 'media_screen_studies_philosophy_ba', 'political_science_philosophy_ba',
          'religious_studies_africana_studies_ba', 'sociology_philosophy_ba', 'sociology_religious_studies_ba',
          'philosophy_bs', 'behavioral_neuroscience_philosophy_bs 2', 'computer_science_philosophy_bs',
          'criminal_justice_philosophy_bs', 'data_science_philosophy_bs', 'economics_philosophy_bs 2',
          'mathematics_philosophy_bs 2', 'physics_philosophy_bs 2', 'political_science_philosophy_bs', 'ethics_minor',
          'information_ethics_minor', 'philosophy_minor', 'religious_studies_minor', 'political_science_ba',
          'africana_studies_political_science_ba', 'english_political_science_ba 2',
          'environmental_studies_political_science_ba', 'history_political_science_ba 2',
          'journalism_political_science_ba', 'media_screen_studies_political_science_ba',
          'political_science_communication_studies_ba', 'political_science_economics_ba 2',
          'political_science_human_services_ba 2', 'political_science_international_affairs_ba 2',
          'political_science_philosophy_ba 2', 'sociology_political_science_ba', 'political_science_bs',
          'biology_political_science_bs', 'computer_science_political_science_bs',
          'computer_science_politics_philosophy_economics_bs', 'criminal_justice_political_science_bs',
          'mathematics_political_science_bs 2', 'political_science_business_administration_bs',
          'political_science_communication_studies_bs', 'political_science_economics_bs 2',
          'political_science_human_services_bs', 'political_science_philosophy_bs 2',
          'politics_philosophy_economics_bs', 'political_science_minor', 'american_political_institutions_minor',
          'international_security_studies_minor', 'sociology_ba', 'cultural_anthropology_ba 2',
          'communication_studies_sociology_ba', 'cultural_anthropology_philosophy_ba 2',
          'cultural_anthropology_religious_studies_ba 2', 'cultural_anthropology_theatre_ba 2',
          'english_cultural_anthropology_ba 2', 'history_cultural_anthropology_ba 2', 'human_services_sociology_ba 2',
          'cultural_anthropology_minor', 'science_technology_studies_minor', 'sociology_minor',
          'college_of_engineering_overview', 'first_year_engineering', 'bioengineering', 'chemical_engineering',
          'civil_and_environmental_engineering', 'electrical_and_computer_engineering',
          'mechanical_and_industrial_engineering', 'interdisciplinary_minors',
          'accelerated_bachelor_graduate_programs 3', 'college_of_arts_media_and_design_overview', 'architecture',
          'art_and_design', 'communication_studies', 'music', 'journalism', 'theatre', 'interdisciplinary 2',
          'accelerated_bachelor_graduate_programs 2'])

    ]

    # Process each scraper batch sequentially
    for scraper_class, tasks in scraping_batches:
        run_scraper_batch(scraper_class, tasks, config, logger)


if __name__ == "__main__":
    main()
