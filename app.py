import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
from bot import BasicBot
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Binance Futures Bot API")

# Initialize bot
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

bot = None
# Check if keys are still placeholders or missing
if api_key and api_secret and "your_testnet" not in api_key:
    try:
        bot = BasicBot(api_key, api_secret)
    except Exception as e:
        print(f"Failed to initialize bot: {e}")
else:
    print("⚠️ WARNING: API Keys are missing or placeholders in .env file.")

class OrderRequest(BaseModel):
    symbol: str
    side: str
    quantity: float
    price: Optional[float] = None
    stop_price: Optional[float] = None
    order_type: str # MARKET, LIMIT, STOP_LIMIT

@app.get("/api/balance")
async def get_balance():
    if not bot:
        raise HTTPException(status_code=400, detail="Bot not initialized. Set API keys in .env")
    try:
        return bot.get_futures_balance()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/order")
async def place_order(order: OrderRequest):
    if not bot:
        raise HTTPException(status_code=400, detail="Bot not initialized")
    try:
        if order.order_type == "MARKET":
            return bot.place_market_order(order.symbol, order.side, order.quantity)
        elif order.order_type == "LIMIT":
            if not order.price:
                raise HTTPException(status_code=400, detail="Price is required for LIMIT order")
            return bot.place_limit_order(order.symbol, order.side, order.quantity, order.price)
        elif order.order_type == "STOP_LIMIT":
            if not order.price or not order.stop_price:
                raise HTTPException(status_code=400, detail="Price and Stop Price are required for STOP_LIMIT order")
            return bot.place_stop_limit_order(order.symbol, order.side, order.quantity, order.price, order.stop_price)
        else:
            raise HTTPException(status_code=400, detail="Unsupported order type")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/orders/{symbol}")
async def get_orders(symbol: str):
    if not bot:
        raise HTTPException(status_code=400, detail="Bot not initialized")
    try:
        return bot.get_open_orders(symbol=symbol if symbol != "all" else None)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount static files
if os.path.exists("static"):
    app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
