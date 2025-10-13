import logging
import os

def setup_logger(log_file: str = "output.log", log_level=logging.INFO) -> logging.Logger:
    """
    Set up and return a configured logger for the AI assistant.
    
    Args:
        log_file (str): The name or path of the log file. Default is 'output.log'.
        log_level (int): Logging level (e.g., logging.INFO, logging.DEBUG).
    
    Returns:
        logging.Logger: Configured logger instance.
    """

    # Ensure log directory exists
    os.makedirs(os.path.dirname(log_file) or ".", exist_ok=True)

    logger = logging.getLogger("StaplrLogger")
    logger.setLevel(log_level)

    # Prevent adding duplicate handlers if logger is reused
    if not logger.handlers:
        file_handler = logging.FileHandler(log_file)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    logger.info("Logger initialized successfully.")
    return logger


# Example usage
if __name__ == "__main__":
    logger = setup_logger()
    logger.info("Staplr assistant logging started.")
