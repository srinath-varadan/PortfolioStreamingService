# Stock Stream Service

## Overview
This service streams mock stock data real-time and captures logs to a `.log` file. It also exposes:
- `/stream/stocks` : Real-time SSE API
- `/logs` : Download log file
- `/docs` : Swagger UI

## Tech
- FastAPI
- Uvicorn
- Python 3.11
- Docker (for Render deployment)

## Deployment
Use `render.yaml` for one-click deploy to Render.com.
