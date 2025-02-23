import logging
import os
import datetime


# Function to configure the logger for writing logs into a file
def configure_logger(logger_name,log_output_path):
    # Create a logs directory if it doesn't exist
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    if not os.path.exists(log_output_path):
        os.makedirs(log_output_path)

    # Define the log file path for the document
    log_filename = f"{log_output_path}/{logger_name}_{timestamp}_processing.log"

    # Create a logger with the document name
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)  # Set the logging level

    # Create a FileHandler to write logs into a file
    file_handler = logging.FileHandler(log_filename)

    # Create a logging format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the FileHandler to the logger
    if not logger.hasHandlers():  # Prevent duplicate handlers if already set
        logger.addHandler(file_handler)

    return logger