import os
from dotenv import load_dotenv
from scraper import initialize_model, run_smart_scraper
from utils import load_json_file, save_results, setup_logging

# Load environment variables
load_dotenv()
HUGGINGFACEHUB_API_TOKEN = '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' #os.getenv('HUGGINGFACEHUB_API_TOKEN')

if not HUGGINGFACEHUB_API_TOKEN:
    raise ValueError("Hugging Face API token not found in .env file")

# Set up logging
logger = setup_logging('../../logs/scraper.log')

try:
    # Log the start of the process
    logger.info("Starting the scraping process...")

    # Load configuration and prompts using the generic load function
    logger.info("Loading config and prompts...")
    config = load_json_file("../../configs/config.json", logger)
    prompts = load_json_file("../../configs/prompts.json", logger)

    # Initialize model instances
    logger.info("Initializing model instances...")
    llm_model_instance, _ = initialize_model(config, HUGGINGFACEHUB_API_TOKEN)

    # Loop through tasks in the config file
    for task_key, task_details in config["scraping_tasks"].items():
        url = task_details["url"]
        output_filename = task_details["output_file"]

        # Log task start
        logger.info(f"Starting scraping task: {task_key} for URL: {url}")

        # Retrieve the prompt for the current task
        prompt = prompts.get(task_key)
        if not prompt:
            logger.error(f"No prompt found for task: {task_key}, skipping this task.")
            continue

        # Log that the scraper is running
        logger.info(f"Running scraper for {task_key}...")

        # Run the scraper
        result = run_smart_scraper(url, prompt, llm_model_instance)

        # If result is None, log an error and continue
        if not result:
            logger.error(f"Failed to get results for {task_key}, skipping saving.")
            continue

        # Save the results if successful
        try:
            logger.info(f"Saving results for {task_key} to {output_filename}")
            save_results(result, f"../../results/{output_filename}", logger)
            logger.info(f"Successfully saved results for {task_key} to {output_filename}")
        except Exception as e:
            logger.error(f"Failed to save results for {task_key}: {e}")

except Exception as e:
    # Log any critical errors during the overall process
    logger.critical(f"Critical error during scraping execution: {e}")
