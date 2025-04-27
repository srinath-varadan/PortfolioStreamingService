from fastapi import FastAPI
from fastapi.responses import StreamingResponse, FileResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from app.stock_streamer import stock_data_generator, streaming_active_event
from app.logger import logger
import asyncio
import json
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST


from app.stock_streamer import stock_data_generator

LOG_COUNT = Counter('python_log_entries_total', 'Total log entries received')

app = FastAPI(
    title="Stock Stream Service",
    description="Streaming mock stock data and logs",
    version="1.0.0"
)

origins = [
    "https://srinath-varadan.github.io",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/stream/stocks", summary="Stream stock data in real-time")
async def stream_stock_data():
    async def event_generator():
        async for stock in stock_data_generator():
            yield f"data: {json.dumps(stock)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.post("/stop", summary="Stop streaming stock data")
async def stop_streaming():
    streaming_active_event.clear()  # ✅ This will stop all existing generators
    logger.info("Streaming manually stopped by API call")
    return {"message": "Streaming stopped"}

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/logs", summary="Fetch current .log file")
async def fetch_logs():
    LOG_COUNT.inc()
    return FileResponse("logs/stock_stream.log", media_type="text/plain")
