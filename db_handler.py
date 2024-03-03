from dotenv import dotenv_values
from pymongo import MongoClient
from bson.json_util import dumps

import os

from models.order import Order
from models.trade import Trade


class DbHandler:

    def __init__(self):
        """Initialize the database connection"""

        # If the environment variable is not set for test database, set it to the value in the .env file
        if os.getenv('db') is None:
            os.environ['db'] = dotenv_values(".env").get('DB_NAME')

        self.db = MongoClient(os.getenv('mongodb_uri'))[os.getenv('db')]

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
