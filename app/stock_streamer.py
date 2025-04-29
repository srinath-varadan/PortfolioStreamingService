import asyncio
import random
from datetime import datetime
from app.logger import logger
import json

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

streaming_active_event = asyncio.Event()
streaming_active_event.set()  # Allow streaming initially

async def stock_data_generator():
    while streaming_active_event.is_set():
        current_time = datetime.utcnow().isoformat()

        for stock in sample_stocks:
            price = round(random.uniform(100, 1500), 2)
            data = {
                "symbol": stock["symbol"],
                "price": price,
                "timestamp": current_time,
                "color": stock["color"]
            }

            # Send each stock as an individual SSE event
            yield f"data: {json.dumps(data)}\n\n"

            # Optional: small delay between stocks to smooth streaming
            await asyncio.sleep(0.1)

        await asyncio.sleep(1.5)  # After one round of all stocks, small wait before next batch