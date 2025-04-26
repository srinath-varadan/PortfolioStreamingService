import logging

logger = logging.getLogger("stock_logger")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("logs/stock_stream.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
