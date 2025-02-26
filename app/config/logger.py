import logging
import os
from datetime import datetime

class Logger:
    def __init__(self, log_file: str = "app.log", log_level=logging.INFO):
        """Initializes the logger with a log file and logging level."""
        self.logger = logging.getLogger("CentralizedLogger")
        self.logger.setLevel(log_level)

        # Create log directory if it doesn't exist
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Set up file handler
        log_file_path = os.path.join(log_dir, log_file)
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(log_level)

        # Set up console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)

        # Define log format
        log_format = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(module)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        file_handler.setFormatter(log_format)
        console_handler.setFormatter(log_format)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        """Returns the configured logger instance."""
        return self.logger



logger = Logger().get_logger()