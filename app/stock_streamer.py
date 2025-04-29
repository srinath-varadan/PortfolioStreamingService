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
        for i, symbol in enumerate(MOCK_SYMBOLS):
            price = round(random.uniform(100 + i * 50, 1500 - i * 100), 2)
            timestamp = datetime.utcnow().isoformat()
            color = f"hsl({(i * 72) % 360}, 70%, 50%)"  # Generate a unique color

            data = {"symbol": symbol, "price": price, "timestamp": timestamp, "color": color}
            logger.info(f"Generated stock data: {data}")
            yield data

        await asyncio.sleep(2)