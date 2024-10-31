import json
import os

# Directory containing your JSON files
data_directory = '/Users/aadarsh/PycharmProjects/husky_scraper/results/'  # Replace with your directory path


def process_accreditation_file(data):
    dataset = []
    # Since the data is a list of lists, we need to flatten it
    for sublist in data:
        for item in sublist:
            college = item.get('College', 'Unknown College')
            program = item.get('Program', 'Unknown Program')
            agency = item.get('Accrediting Agency', 'Unknown Agency')
            prompt = f"Which accrediting agency has accredited the {program} program at {college}?"
            completion = f"The {program} program at {college} is accredited by {agency}."
            dataset.append({'prompt': prompt, 'completion': completion})
    return dataset


def process_course_file(data):
    dataset = []
    for item in data:
        course_title = item.get('Course Title', 'Unknown Course')
        description = item.get('Description', 'No description available.')
        prerequisites = item.get('Prerequisites', 'No prerequisites listed.')
        hours = item.get('Hours', 'N/A')

        # Course Description
        prompt = f"What is the description of the course '{course_title}'?"
        completion = description
        dataset.append({'prompt': prompt, 'completion': completion})

        # Course Prerequisites
        prompt = f"What are the prerequisites for the course '{course_title}'?"
        completion = prerequisites
        dataset.append({'prompt': prompt, 'completion': completion})

        # Course Hours
        prompt = f"How many credit hours is the course '{course_title}'?"
        completion = f"The course '{course_title}' is {hours} credit hours."
        dataset.append({'prompt': prompt, 'completion': completion})
    return dataset


def process_faculty_file(data):
    dataset = []
    for item in data:
        name = item.get('Name', 'Unknown Name')
        title_department = item.get('Title and Department', 'No title or department available.')
        prompt = f"What is the title and department of {name}?"
        completion = f"{name} is {title_department}."
        dataset.append({'prompt': prompt, 'completion': completion})
    return dataset


# Existing function to extract texts recursively
def extract_texts(data):
    texts = []
    if isinstance(data, str):
        texts.append(data.strip())
    elif isinstance(data, dict):
        text = data.get('text', '')
        if text:
            texts.append(text.strip())
        else:
            for value in data.values():
                texts.extend(extract_texts(value))
    elif isinstance(data, list):
        for item in data:
            texts.extend(extract_texts(item))
    return texts


# Existing function to create prompt-completion pairs
def create_prompt_completion(data):
    dataset = []
    for item in data:
        for title, content in item.items():
            policies = content.get('Content', {})
            url = policies.get('url', '')
            contact_info = content.get('contact_info', {})
            emails = contact_info.get('emails', [])
            phone_numbers = contact_info.get('phone_numbers', [])
            hyperlinks = contact_info.get('hyperlinks', [])

            # Include contact info in prompts and completions
            if emails:
                for email in emails:
                    prompt = f"What is the email address provided in the '{title}' document?"
                    completion = f"The email address is {email}."
                    dataset.append({"prompt": prompt, "completion": completion})

            if phone_numbers:
                for phone in phone_numbers:
                    prompt = f"What is the phone number provided in the '{title}' document?"
                    completion = f"The phone number is {phone}."
                    dataset.append({"prompt": prompt, "completion": completion})

            if hyperlinks:
                for link in hyperlinks:
                    prompt = f"Provide the hyperlink for '{link.get('text', 'the provided link')}' from the '{title}' document."
                    completion = f"The hyperlink is {link.get('url', '')}."
                    dataset.append({"prompt": prompt, "completion": completion})

            for section, section_content in policies.items():
                if section == 'url':
                    continue  # Skip the URL key
                if isinstance(section_content, dict):
                    for subsection, texts in section_content.items():
                        extracted_texts = extract_texts(texts)
                        for text in extracted_texts:
                            prompt = f"Explain the policy section '{subsection}' in the context of '{section}'."
                            completion = text
                            dataset.append({
                                "prompt": prompt,
                                "completion": completion
                            })
                else:
                    extracted_texts = extract_texts(section_content)
                    for text in extracted_texts:
                        prompt = f"Provide information on '{section}' from the university policies."
                        completion = text
                        dataset.append({
                            "prompt": prompt,
                            "completion": completion
                        })
    return dataset


# Initialize lists to hold all data and the final dataset
all_data = []
dataset = []

# Read and process each JSON file in the directory and its subdirectories
for root, dirs, files in os.walk(data_directory):
    for filename in files:
        if filename.endswith('.json'):
            filepath = os.path.join(root, filename)
            with open(filepath, 'r') as f:
                data = json.load(f)
                # Check the filename to determine how to process it
                if filename == 'northeastern_accreditation.json':
                    dataset.extend(process_accreditation_file(data))
                elif filename == 'northeastern_course_descriptions.json':
                    dataset.extend(process_course_file(data))
                elif filename == 'northeastern_faculty_members.json':
                    dataset.extend(process_faculty_file(data))
                else:
                    all_data.extend(data)

# Process the remaining data using the existing function
if all_data:
    dataset.extend(create_prompt_completion(all_data))

# Save to JSONL file
with open('fine_tuning_data.jsonl', 'w') as f:
    for entry in dataset:
        json.dump(entry, f)
        f.write('\n')

print("Dataset has been successfully created and saved to 'fine_tuning_data.jsonl'.")
