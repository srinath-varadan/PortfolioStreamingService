from pydantic import BaseModel

class StockData(BaseModel):
    symbol: str
    price: float
    timestamp: str
