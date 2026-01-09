import logging
import os
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv

# Configure logging
if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("TradingBot")

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        self.client = Client(api_key, api_secret, testnet=testnet)
        if testnet:
            # Explicitly set the Futures Testnet URL as per assignment instructions
            self.client.F_API_URL = 'https://testnet.binancefuture.com/fapi'
            self.client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'
            self.client.FUTURES_DATA_URL = 'https://testnet.binancefuture.com/fapi'
        
        logger.info(f"Initialized BasicBot (Testnet={testnet})")

    def get_futures_balance(self, asset="USDT"):
        """Get futures account balance for a specific asset."""
        try:
            logger.info("Fetching futures account balance...")
            balances = self.client.futures_account_balance()
            logger.info(f"Balance response received: {balances}")
            for balance in balances:
                if balance['asset'] == asset:
                    return balance
            return None
        except BinanceAPIException as e:
            logger.error(f"API Error fetching balance: {e.status_code} - {e.message}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error fetching balance: {str(e)}")
            raise

    def place_market_order(self, symbol, side, quantity):
        """Place a market order on Binance Futures."""
        try:
            logger.info(f"Request: MARKET {side} {symbol} Qty:{quantity}")
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type=ORDER_TYPE_MARKET,
                quantity=quantity
            )
            logger.info(f"Response: Order {order['orderId']} successful. Details: {order}")
            return order
        except BinanceAPIException as e:
            logger.error(f"API Error (Market Order): {e.status_code} - {e.message}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise

    def place_limit_order(self, symbol, side, quantity, price):
        """Place a limit order on Binance Futures."""
        try:
            logger.info(f"Request: LIMIT {side} {symbol} Qty:{quantity} @ {price}")
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type=ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=quantity,
                price=str(price)
            )
            logger.info(f"Response: Order {order['orderId']} successful. Details: {order}")
            return order
        except BinanceAPIException as e:
            logger.error(f"API Error (Limit Order): {e.status_code} - {e.message}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise

    def place_stop_limit_order(self, symbol, side, quantity, price, stop_price):
        """Place a stop-limit order on Binance Futures."""
        try:
            logger.info(f"Request: STOP_LIMIT {side} {symbol} Qty:{quantity} @ {price} Stop:{stop_price}")
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type=FUTURE_ORDER_TYPE_STOP,
                quantity=quantity,
                price=str(price),
                stopPrice=str(stop_price)
            )
            logger.info(f"Response: Order {order['orderId']} successful. Details: {order}")
            return order
        except BinanceAPIException as e:
            logger.error(f"API Error (Stop-Limit Order): {e.status_code} - {e.message}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise

    def get_open_orders(self, symbol=None):
        """Fetch open orders."""
        try:
            logger.info(f"Fetching open orders for {symbol if symbol else 'all symbols'}...")
            orders = self.client.futures_get_open_orders(symbol=symbol)
            logger.info(f"Fetched {len(orders)} open orders.")
            return orders
        except Exception as e:
            logger.error(f"Error fetching open orders: {str(e)}")
            raise
