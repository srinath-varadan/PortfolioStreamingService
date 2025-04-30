import asyncio
import random
from datetime import datetime
from app.logger import logger
import httpx
import time

MOCK_SYMBOLS = ["AAPL", "GOOGL", "AMZN", "MSFT", "TSLA"]

stock_streaming_active_event = asyncio.Event()
stock_streaming_active_event.set()

loki_streaming_active_event = asyncio.Event()
loki_streaming_active_event.set()

async def stock_data_generator():
    try:
        while stock_streaming_active_event.is_set():
            symbol = random.choice(MOCK_SYMBOLS)
            price = round(random.uniform(100, 1500), 2)
            timestamp = datetime.utcnow().isoformat()

            data = {"symbol": symbol, "price": price, "timestamp": timestamp}
            logger.info(f"Generated stock data: {data}")
            yield data

            await asyncio.sleep(1)
    except asyncio.CancelledError:
        logger.info("Stock data generator stopped due to client disconnection.")
        raise
    except Exception as e:
        logger.exception(f"Unexpected error in stock_data_generator: {e}")
        raise

async def loki_log_stream(job_name="logaggregator-ai-analysis", loki_url="https://logs-prod-028.grafana.net", username=None, password=None):
    auth = (username, password) if username and password else None
    try:
        async with httpx.AsyncClient(timeout=None, auth=auth) as client:
            label_url = f"{loki_url}/loki/api/v1/label/job/values"
            label_resp = await client.get(label_url)
            if label_resp.status_code == 200:
                jobs = label_resp.json()
                logger.info(f"Available Loki job labels: {jobs.get('data')}")
                if job_name not in jobs.get("data", []):
                    warning = f"Job '{job_name}' not found in available labels: {jobs.get('data')}"
                    logger.warning(warning)
                    yield {"log": warning}
                    return
            else:
                logger.warning(f"Failed to fetch job labels: {label_resp.status_code}")

            query = f'{{job="{job_name}"}}'
            url = f"{loki_url}/loki/api/v1/query_range"
            start_ns = int((time.time() - 2 * 86400) * 1_000_000_000)  # Start from 48 hours ago

            logger.info(f"Starting Loki log polling for query: {query}")
            while loki_streaming_active_event.is_set():
                params = {
                    "query": query,
                    "start": str(start_ns),
                    "limit": 100,
                    "direction": "forward"
                }
                response = await client.get(url, params=params)
                if response.status_code != 200:
                    error_text = response.text
                    logger.error(f"Loki returned {response.status_code}: {error_text}")
                    yield {"log": f"Loki error {response.status_code}: {error_text}"}
                    return

                logs = response.json().get("data", {}).get("result", [])
                for stream in logs:
                    for entry in stream.get("values", []):
                        ts, log_line = entry
                        logger.info(f"Loki log line: {log_line}")
                        yield {"log": log_line}
                        start_ns = max(start_ns, int(ts) + 1)

                await asyncio.sleep(3)  # poll every 3 seconds
    except asyncio.CancelledError:
        logger.info("Loki log stream cancelled by client.")
        raise
    except Exception as e:
        logger.exception(f"Error streaming from Loki: {e}")
        raise