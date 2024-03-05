import dotenv
from dotenv import dotenv_values
from pymongo import MongoClient
from bson.json_util import dumps

import os

from models.order import Order
from models.trade import Trade


class DbHandler:

    def __init__(self, client=None):
        """
        Initialize the database connection
        :param client: The client to use for the database connection
        """

        if client is None:
            # If the environment variable is not set for the test database, set it to the value in the .env file
            dotenv.load_dotenv()
            self.db = MongoClient(os.getenv('MONGODB_URI'))[os.getenv('DB_NAME')]
        else:
            self.db = client

    def record_trade(self, trade: Trade):
        """Record a trade in the database"""
        try:
            return self.db.trades.insert_one(trade.json())
        except Exception as e:
            return str(e)

    def get_trades(self) -> str:
        """Get all trades from the database"""
        try:
            cursor = list(self.db.trades.find())
            return dumps(cursor)
        except Exception as e:
            return str(e)

    def delete_trade(self, trade_id: str):
        """Delete a trade from the database by its id"""
        try:
            return self.db.trades.delete_one({'_id': trade_id})
        except Exception as e:
            return str(e)

    def delete_trades(self):
        """Delete all trades from the database"""
        try:
            return self.db.trades.delete_many({})
        except Exception as e:
            return str(e)

    def record_order(self, order: Order):
        """Record an order in the database"""
        try:
            return self.db.orders.insert_one(order.json())
        except Exception as e:
            return str(e)

    def delete_order(self, order_id: str):
        """Delete an order from the database by its id"""
        try:
            return self.db.orders.delete_one({'_id': order_id})
        except Exception as e:
            return str(e)

    def delete_orders(self):
        """Delete all orders from the database"""
        try:
            return self.db.orders.delete_many({})
        except Exception as e:
            return str(e)

    def update_order(self, order_id: str, quantity: int):
        """Update the quantity of an order"""
        try:
            return self.db.orders.update_one({'_id': order_id}, {'$set': {'quantity': quantity, }})
        except Exception as e:
            return str(e)

    def get_orders(self):
        """Get all orders from the database"""
        try:
            cursor = list(self.db.orders.find())
            return dumps(cursor)
        except Exception as e:
            return str(e)

    def record_last_traded_price(self, price: float):
        """Record the last traded price in the database"""
        try:
            return self.db.last_trade.update_one({'_id': 'last_trade'}, {'$set': {'price': price}}, upsert=True)
        except Exception as e:
            return str(e)

    def get_last_traded_price(self):
        """Get the last traded price from the database"""
        try:
            cursor = self.db.last_trade.find_one({'_id': 'last_trade'})
            return cursor['price']
        except Exception as e:
            return str(e)
