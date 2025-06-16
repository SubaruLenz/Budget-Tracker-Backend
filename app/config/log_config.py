import logging
from rich.logging import RichHandler

def setup_config():
    #Create file handler
    file_handler = logging.FileHandler("Report.log", mode="w")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

    #Create terminal handler
    terminal_handler = RichHandler()
    terminal_handler.setLevel(logging.INFO)
    terminal_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(message)s"))

    logging.basicConfig(
        level=logging.INFO,
        handlers=[file_handler, terminal_handler]
    )