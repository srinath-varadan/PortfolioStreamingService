import asyncio
import random
from datetime import datetime
from app.logger import logger

MOCK_SYMBOLS = ["AAPL", "GOOGL", "AMZN", "MSFT", "TSLA"]

async def stock_data_generator():
    while True:
        symbol = random.choice(MOCK_SYMBOLS)
        price = round(random.uniform(100, 1500), 2)
        timestamp = datetime.utcnow().isoformat()

        data = {"symbol": symbol, "price": price, "timestamp": timestamp}
        logger.info(f"Generated stock data: {data}")
        yield data

        await asyncio.sleep(1)
