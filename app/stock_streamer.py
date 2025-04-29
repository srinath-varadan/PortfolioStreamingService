import asyncio
import random
from datetime import datetime
from app.logger import logger

sample_stocks = [
    {"symbol": "AAPL", "color": "#FF5733"},
    {"symbol": "GOOGL", "color": "#33FF57"},
    {"symbol": "AMZN", "color": "#3357FF"},
    {"symbol": "MSFT", "color": "#FF33A1"},
    {"symbol": "TSLA", "color": "#A133FF"},
    {"symbol": "META", "color": "#33FFF3"},
    {"symbol": "NFLX", "color": "#FF8C33"},
    {"symbol": "NVDA", "color": "#8CFF33"},
    {"symbol": "BABA", "color": "#338CFF"},
    {"symbol": "DIS", "color": "#FF3333"},
]

# GLOBAL event to control streaming
streaming_active_event = asyncio.Event()
streaming_active_event.set()  # Initially streaming is allowed

async def stock_data_generator():
    while streaming_active_event.is_set():
        symbol = random.choice(sample_stocks)
        price = round(random.uniform(100, 1500), 2)
        timestamp = datetime.utcnow().isoformat()

        data = {"symbol": symbol["symbol"], "price": price, "timestamp": timestamp,"color": symbol["color"]}
        logger.info(f"Generated stock data: {data}")
        yield data

        await asyncio.sleep(1)