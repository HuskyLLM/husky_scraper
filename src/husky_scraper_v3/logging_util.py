import logging
import sys

class LoggerFactory:
    """
    A factory class for setting up and providing a logging instance.
    Ensures consistent logging configuration across the application.
    """

    @staticmethod
    def get_logger(logger_name: str) -> logging.Logger:
        """
        Sets up and returns a logger instance.

        Args:
            logger_name (str): The name of the logger.

        Returns:
            logging.Logger: The configured logger instance.
        """
        logger = logging.getLogger(logger_name)

        # Check if the logger has already been configured
        if not logger.hasHandlers():
            logger.setLevel(logging.INFO)

            # Create a console handler
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(logging.INFO)

            # Create a formatter and set it to the handler
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)

            # Add the handler to the logger
            logger.addHandler(handler)

        return logger
