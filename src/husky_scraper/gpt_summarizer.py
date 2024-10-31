from utils import load_from_file
from logging_util import LoggerFactory
import os
import json
from openai import OpenAI
from pydantic import BaseModel, ValidationError
import ast
import time
import traceback


# Define Pydantic model for structured output
class PolicyResponseModel(BaseModel):
    prompt: str
    completion: str


# Function to generate structured output from JSON data
def generate_response_from_data(data):
    # Construct the prompt with structured formatting
    # Function to generate structured output from JSON data
    # Construct the prompt with structured formatting
    prompt = f'''
    You are a helpful university advisor. Based on the following JSON data containing university policies, procedures, contact information, and other relevant details, generate a structured JSON output in the following format:
    1. Analyze the provided JSON structure.
    2. Convert the information into clear, natural language.
    3. Organize the content logically with appropriate sections.
    4. Include all relevant:
       - Steps and procedures
       - Contact information
       - URLs/links
       - Deadlines and important dates
       - Special requirements or conditions
       - Summary of key points

    Format your response in a user-friendly way using:
    - Clear headings
    - Bullet points where appropriate
    - Numbered steps for processes
    - Tables if needed
    - Clear distinction between main content and supplementary information

    You should maintain:
    - A professional but approachable tone
    - Accuracy to the source material
    - Clear organization
    - An easy-to-follow structure
    - All relevant details from the original JSON


    Please ensure the output is valid JSON and includes all relevant details from the input data.

    Input JSON data:
    {json.dumps(data, indent=2)}
    I need maximum information to be covered as this data will be used for fine tuning a LLM.
    Understand the information and add what promts and completion based on what questions a student can have about it.
    output format:
    {{
      "dataset": [
        {{
          "prompt": "What is [Question about policy,plan of study, courses to choose, benefits of the course, steps and  procedure, course description, course duration, course requirements,contact information,  or specific detail]?",
          "completion": "[Detailed, clear, summarized and concise response based on the provided data. add any relevant contact information, hyperlinks]"
        }}
      ]
    Read the prompt carefully and answer and try to generate at least 10 prompts. if enough data is not there it is ok to have less prompts
    }}
    '''
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",  # You can use "gpt-4" if you have access
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=16382,
        response_format={
            'type': 'json_schema',
            'json_schema':
                {
                    "name": "whocares",
                    "schema": PolicyResponseModel.model_json_schema()
                }}
    )
    # Return content directly as JSON
    try:
        content = response.choices[0].message.content
        return ast.literal_eval(content)
    except json.JSONDecodeError:
        print("Failed to decode the response as JSON.")
        return None


def main():
    """
    Main function to orchestrate the scraping process by loading the config
    and executing the appropriate scrapers concurrently.
    """
    logger = LoggerFactory.get_logger("JsonFormatter")
    logger.info("Starting the scraping process...")

    # Load scraping tasks from scraper_config.json
    config = load_from_file('../../configs/data_fine_tune_config.json', logger)

    # Log the loaded config for debugging
    logger.info(f"Config loaded: {config}")

    if config is None:
        logger.error("Failed to load the configuration file.")
        return

    data_directory = config['input_directory']
    output_directory = config['output_directory']
    api_key = config['api_key']
    os.environ["OPENAI_API_KEY"] = api_key

    # Loop through each JSON file, process, and create a corresponding JSONL file
    if output_directory and not os.path.exists(output_directory):
        os.makedirs(output_directory)
        logger.info(f"Created directory: {output_directory}")
    error_files = []
    for root, dirs, files in os.walk(data_directory):
        for filename in files:
            if filename.endswith('.json'):
                filepath = os.path.join(root, filename)
                print(filename)
                refined_output_path = filepath.replace('raw', 'refined').replace('.json', '.jsonl')
                os.makedirs(os.path.dirname(refined_output_path), exist_ok=True)
                with open(filepath, 'r') as f:
                    data = json.load(f)

                # Generate response from JSON data

                try:
                    response_text = generate_response_from_data(data)
                except Exception as e:
                    response_text = []
                    error_files.append(filepath)
                    logger.error(f"Error occurred during fetching data from api {filepath}: {str(e)} - {traceback.format_exc()} ")

                time.sleep(30)
                if response_text:
                    # Create structured data using the Pydantic model
                    try:
                        # Write structured response to a .jsonl file with the same name as the input file
                        with open(refined_output_path, 'w') as jsonl_file:
                            jsonl_file.write(json.dumps(response_text, indent=4))

                        print(f"Processed and wrote output to {refined_output_path}")

                    except ValidationError as e:
                        print(f"Validation error for {filename}: {e}")

    logger.info(f"error file = {error_files}")


main()
