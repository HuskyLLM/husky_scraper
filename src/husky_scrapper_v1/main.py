from preprocessing.utils import get_terms, declare_term, get_courses, get_subjects, create_session
from preprocessing.clean_data import clean_course_data
import json
import os


def main():
    session = create_session()
    terms = get_terms(session)
    all_courses = []

    for term in terms:
        term_code = term['code']
        declare_term(session, term_code)
        subjects = get_subjects(session, term_code)
        for subject in subjects:
            subject_code = subject.get('code')
            if subject_code:
                print(f"Processing subject {subject_code} for term {term_code}")
                courses = get_courses(session, term_code, subject_code)
                all_courses.extend(courses)

    # Save raw data
    os.makedirs('data/raw', exist_ok=True)
    with open('data/raw/all_courses.json', 'w') as f:
        json.dump(all_courses, f, indent=4)
        print("All course data saved to data/raw/all_courses.json")

    # Preprocess data
    cleaned_courses = [clean_course_data(course) for course in all_courses]

    # Save processed data
    os.makedirs('data/processed', exist_ok=True)
    with open('data/processed/processed_courses.json', 'w') as f:
        json.dump(cleaned_courses, f, indent=4)
        print("Processed course data saved to data/processed/processed_courses.json")


if __name__ == "__main__":
    main()
