from pydantic import BaseModel
from datetime import datetime

class Kline(BaseModel):
    OpenTime: datetime
    CloseTime: datetime
    Open: float
    High: float
    Low: float
    Close: float
    Volume: float
    QuoteAssetVolume: float
    NumberOfTrades: float
    TakerBuyBaseAssetVolume: float
    TakerBuyQuoteAssetVolume: float
    Ignore: float