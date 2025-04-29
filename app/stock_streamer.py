import asyncio
import random
from datetime import datetime
from app.logger import logger

MOCK_SYMBOLS = ["AAPL", "GOOGL", "AMZN", "MSFT", "TSLA"]

# GLOBAL event to control streaming
streaming_active_event = asyncio.Event()
streaming_active_event.set()  # Initially streaming is allowed

async def stock_data_generator():
    while streaming_active_event.is_set():
        symbol = random.choice(MOCK_SYMBOLS)
        price = round(random.uniform(100, 1500), 2)
        timestamp = datetime.utcnow().isoformat()

        data = {"symbol": symbol, "price": price, "timestamp": timestamp}
        logger.info(f"Generated stock data: {data}")
        yield data

        await asyncio.sleep(1)