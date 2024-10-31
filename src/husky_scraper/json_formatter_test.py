import json
from typing import List, Dict
from pathlib import Path


def load_json_file(file_path: str) -> List[Dict]:
    """
    Load data from a JSON file.
    """
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {file_path}: {str(e)}")
        return []


def process_course_data(courses: List[Dict]) -> List[Dict]:
    """
    Process course catalog data and generate training examples.
    """
    training_examples = []

    for course in courses:
        # Example 1: Course description query
        training_examples.append(
            {"prompt": f"What is the description of {course['Course Title']}?",
             "completion": course['Description']}
        )

        # Example 2: Prerequisites query
        training_examples.append(
            {"prompt": f"What are the prerequisites for {course['Course Title']}?",
             "completion": course['Prerequisites']}
        )

        # Example 3: Complete course information query
        training_examples.append(
            {"prompt": f"Tell me everything about {course['Course Title']}.",
             "completion": f"This is a {course['Hours']} credit hour course. {course['Description']} Prerequisites: {course['Prerequisites']}"}
        )

        # Example 4: Credit hours query
        training_examples.append(
            {"prompt": f"How many credit hours is {course['Course Title']}?",
             "completion": f"This course is {course['Hours']} credit hours."}
        )

    return training_examples


def process_program_data(programs: List[Dict]) -> List[Dict]:
    """
    Process academic program data and generate training examples.
    """
    training_examples = []

    for program in programs:
        # Extract program code and name
        program_parts = program['Academic Program'].split(': ', 1)
        program_code = program_parts[0]
        program_name = program_parts[1] if len(program_parts) > 1 else program_parts[0]

        # Example 1: General program information query
        training_examples.append(
            {"prompt": f"What is the {program_code} program?",
             "completion": f"The {program_code} program is {program_name}. It appears on transcripts as '{program['Major Transcript Title']}' and has a CIP code of {program['Major Cip Code']}."}
        )

        # Example 2: Program code to full name mapping
        training_examples.append(
            {"prompt": f"What does the program code {program_code} stand for?",
             "completion": f"{program_code} stands for {program_name}."}
        )

        # Example 3: Transcript title query
        training_examples.append(
            {"prompt": f"How does {program_name} appear on the transcript?",
             "completion": f"The program appears on transcripts as '{program['Major Transcript Title']}'."}
        )

        # Example 4: CIP code query
        training_examples.append(
            {"prompt": f"What is the CIP code for {program_name}?",
             "completion": f"The CIP code for this program is {program['Major Cip Code']}."}
        )

        # Example 5: Online program identification
        if "-O:" in program['Academic Program']:
            training_examples.append(
                {"prompt": f"Is {program_name} available online?",
                 "completion": "Yes, this program is available as an online program."}
            )

        # Example 6: Degree type identification
        degree_type = ""
        if "CERTG-" in program_code:
            degree_type = "Graduate Certificate"
        elif "P-CERTG-" in program_code:
            degree_type = "Professional Graduate Certificate"

        if degree_type:
            training_examples.append(
                {"prompt": f"What type of degree or certificate is {program_name}?",
                 "completion": f"This is a {degree_type} program."}
            )

    return training_examples


def save_dataset(dataset: List[Dict], output_file: str):
    """
    Save the dataset in the specified JSON format.
    """
    # Structure the dataset as specified
    output_data = {"dataset": dataset}

    # Save to file
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=4)

    print(f"Dataset saved to: {output_file}")


def main():
    # Check if courses.json exists and process it
    courses_file = "/Users/aadarsh/PycharmProjects/husky_scraper/results/raw/general_information/northeastern_course_descriptions.json"
    if Path(courses_file).exists():
        courses = load_json_file(courses_file)
        if courses:
            course_dataset = process_course_data(courses)
            save_dataset(course_dataset, "/Users/aadarsh/PycharmProjects/husky_scraper/results/refined/general_information/northeastern_course_descriptions.jsonl")

    # Check if programs.json exists and process it
    programs_file = "/Users/aadarsh/PycharmProjects/husky_scraper/results/raw/general_information/major_cip_codes.json"
    if Path(programs_file).exists():
        programs = load_json_file(programs_file)
        if programs:
            program_dataset = process_program_data(programs)
            save_dataset(program_dataset, "/Users/aadarsh/PycharmProjects/husky_scraper/results/refined/general_information/major_cip_codes.jsonl")


if __name__ == "__main__":
    main()
