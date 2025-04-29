import asyncio
import random
from datetime import datetime, timedelta
from app.logger import logger

MOCK_SYMBOLS = [
    {"symbol": "AAPL", "color": "#FF0000"},
    {"symbol": "GOOGL", "color": "#00FF00"},
    {"symbol": "AMZN", "color": "#0000FF"},
    {"symbol": "MSFT", "color": "#FFA500"},
    {"symbol": "TSLA", "color": "#800080"}
]

# GLOBAL event to control streaming
streaming_active_event = asyncio.Event()
streaming_active_event.set()  # Initially streaming is allowed

async def stock_data_generator():
    start_date = datetime.utcnow()

    current_date = start_date
    while streaming_active_event.is_set():
        for entry in MOCK_SYMBOLS:
            symbol = entry["symbol"]
            color = entry["color"]
            price = round(random.uniform(100, 1500), 2)
            timestamp = current_date.isoformat()

            data = {
                "symbol": symbol,
                "price": price,
                "timestamp": timestamp,
                "color": color
            }
            logger.info(f"Generated stock data: {data}")
            yield data

        current_date += timedelta(seconds=2)  # 2-second interval simulation
        await asyncio.sleep(0)  # Yield control to event loop