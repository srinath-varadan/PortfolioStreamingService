import asyncio
import random
from datetime import datetime
from app.logger import logger

MOCK_SYMBOLS = ["AAPL", "GOOGL", "AMZN", "MSFT", "TSLA"]

# GLOBAL event to control streaming
streaming_active_event = asyncio.Event()
streaming_active_event.set()  # Initially streaming is allowed

async def stock_data_generator():
    try:
        while True:
            if not streaming_active_event.is_set():
                await asyncio.sleep(1)
                continue

            symbol = random.choice(MOCK_SYMBOLS)
            price = round(random.uniform(100, 1500), 2)
            timestamp = datetime.utcnow().isoformat()

            data = {"symbol": symbol, "price": price, "timestamp": timestamp}
            yield data

            await asyncio.sleep(1)
    except asyncio.CancelledError:
        logger.info("Stock data generator task was cancelled.")
    except Exception as e:
        logger.exception(f"Unexpected error in stock_data_generator: {e}")