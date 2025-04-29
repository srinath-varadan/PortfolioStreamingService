from fastapi import FastAPI
from fastapi.responses import StreamingResponse, FileResponse, Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from app.stock_streamer import stock_data_generator, streaming_active_event
from app.logger import logger
import asyncio
import json
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import traceback
import os


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
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    if request.method == "POST":
        body = await request.body()
        logger.info(f"Payload: {body.decode('utf-8')}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response
import os

@app.on_event("startup")
async def clear_logs_on_startup():
    log_file_path = "logs/stock_stream.log"
    if os.path.exists(log_file_path):
        with open(log_file_path, "w") as log_file:
            log_file.truncate(0)  # Clear the contents of the log file
    logger.info("Log file cleared on application startup")

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    tb = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
    logger.error(f"Unhandled Exception: {exc}\nTraceback:\n{tb}")
    return JSONResponse(
        status_code=500,
        content={"error": "An unexpected error occurred. Please try again later."}
    )

@app.get("/stream/stocks", summary="Stream stock data in real-time")
async def stream_stock_data():
    try:
        async def event_generator():
            async for stock in stock_data_generator():
                yield f"data: {json.dumps(stock)}\n\n"
        logger.info("Streaming started")
        return StreamingResponse(event_generator(), media_type="text/event-stream")
    except Exception as e:
        logger.exception(f"Error during streaming: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": "An error occurred during streaming."}
        )

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
