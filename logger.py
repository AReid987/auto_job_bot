import logging
from coloredlogs import ColoredFormatter

# Create a custom logger class
class Logger:
    def __init__(self, name, log_file, level=logging.DEBUG):
        # Create a logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Create handlers
        self.file_handler = logging.FileHandler(log_file)
        self.file_handler.setLevel(level)

        self.console_handler = logging.StreamHandler()
        self.console_handler.setLevel(level)

        # Create formatters
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_formatter = ColoredFormatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        self.file_handler.setFormatter(file_formatter)
        self.console_handler.setFormatter(console_formatter)

        # Add handlers to the logger
        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.console_handler)

    def get_logger(self):
        return self.logger
