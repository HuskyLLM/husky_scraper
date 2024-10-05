import logging
import json


def setup_logging(log_file_path='../../logs/scraper.log'):
    """
    Sets up logging configuration with the specified log file.

    :param log_file_path: Path to the log file where logs will be written.
    :return: Configured logger object.
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Create handlers (if no handlers are attached)
    if not logger.hasHandlers():
        # File handler for logging to a file
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(logging.DEBUG)

        # Console handler for printing to console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Formatter for log message format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


def load_json_file(file_path, logger):
    """
    Loads a JSON file from the given file path.

    :param file_path: Path to the JSON file to be loaded.
    :return: Parsed JSON data as a dictionary.
    """
    try:
        with open(file_path, 'r') as file:
            logger.info(f"Loading JSON file from {file_path}")
            return json.load(file)
    except FileNotFoundError:
        logger.error(f"JSON file {file_path} not found.")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse the JSON file {file_path}: {e}")
        raise


def save_results(result, filename, logger):
    """
    Saves results to a JSON file.

    :param result: Data to be saved.
    :param filename: Path where the JSON data will be saved.
    """
    try:
        with open(filename, 'w') as file:
            json.dump(result, file, indent=4)
            logger.info(f"Results saved successfully to {filename}")
    except Exception as e:
        logger.error(f"Failed to save results to {filename}: {e}")
        raise
