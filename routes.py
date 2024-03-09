import json
from flask import Flask
from flask_restful import reqparse, Api, Resource
from db_handler import DbHandler
from models.order import Order
from models.trade import Trade

# Create the parser object to be used in the order end point
parser = reqparse.RequestParser()

# Add arguments to the parser object
#
# Order type: A string. Has to be validated later
parser.add_argument("type", type=str, required=True)
# Unit price: Converts the argument to float. Raises an error if the value can not be parsed
parser.add_argument("price", type=float, required=True)
# Quantity: Converts the argument to integer. Raises an error if the value can not be parsed
parser.add_argument("quantity", type=int, required=True)

# Endpoint for posting an order
class OrderEndPoint(Resource):

    # Set the database handler object
    def __init__(self, db_handler: DbHandler):
        self.db_handler = db_handler
    
    def post(self):
        # Parse the arguments from the data
        arguments = parser.parse_args()

        # get the data from arguments
        order_type  = arguments["type"].lower()
        unit_price  = round(arguments["price"], 2)
        quantity    = arguments["quantity"]

        # If order type is not Offer or Bid, return an error
        if (order_type not in ["offer", "bid"]):
            return {"message": "Undefined order type - Order type must be either Offer or Bid."}, 400

        # Check data validity using AAPL trade price
        last_traded_price = self.db_handler.get_last_traded_price()
        if (unit_price < 0.90 * last_traded_price):
            return {"message": f"Price too low - must be within 10% of the last traded price, which is {last_traded_price}"}, 406
        if (unit_price > 1.10 * last_traded_price):
            return {"message": f"Price too high - must be within 10% of the last traded price, which is {last_traded_price}"}, 406

        # Create a data object
        order = Order(type=order_type, price=unit_price, quantity=quantity)
        
        self.create_trades(order)
        if order.quantity != 0:
            # Add order to the database
            self.db_handler.record_order(order)

        # Return a proper response to the sender
        return {"message": "Order received and recorded"}, 201
    
    def create_trades(self, order):
        orders_json = self.db_handler.get_orders()
        orders = json.loads(orders_json)

        if len(orders) == 0:
            return
        
        matching_orders = self.get_matching_orders(orders, order.type, order.price)
        
        if len(matching_orders) == 0:
            return
        
        for matched_order in matching_orders:
            if order.quantity == 0:
                return
            self.create_trade(order, matched_order)
        
    def get_matching_orders(self, orders, order_type, order_price):
        # exclude orders of the same type as the new order
        filtered_orders = [order for order in orders if order['type'] != order_type]
        
        matching_orders = []

        if order_type == "bid":
            orders_by_lowest_price = sorted(filtered_orders, key=lambda order: order['price'])
            for order in orders_by_lowest_price:
                if order_price >= order['price']:
                    matching_orders.append(order)

        if order_type == "offer":
            orders_by_highest_price = sorted(filtered_orders, key=lambda order: order['price'], reverse=True)
            for order in orders_by_highest_price:
                if order_price <= order['price']:
                    matching_orders.append(order)
            
        return matching_orders
    
    def create_trade(self, order, matched_order):
        highest_price = max(order.price, matched_order['price'])
        lowest_quantity = min(order.quantity, matched_order['quantity'])
            
        trade = Trade(
            price=highest_price,
            quantity=lowest_quantity)
            
        self.db_handler.record_trade(trade)

        matched_order_id = str(matched_order['_id']['$oid'])
        if lowest_quantity == matched_order['quantity']:
            # TODO deleting order does not work
            self.db_handler.delete_order(matched_order_id)
            order.quantity -= matched_order['quantity']
        else: 
            updated_quantity = matched_order['quantity'] - order.quantity
            # TODO updating order does not work
            self.db_handler.update_order(matched_order_id, updated_quantity)
            order.quantity = 0


        
# Endpoint for getting trades
class TradeEndPoint(Resource):

    # Set the database handler object
    def __init__(self, db_handler: DbHandler):
        self.db_handler = db_handler

    def get(self):
        # Fetch the trade information from the database
        return self.db_handler.get_trades(), 200

# Create app with a database handler
def create_app(db_handler: DbHandler):
    app = Flask(__name__)
    api = Api(app)
    # Add the endpoints and the db_handler to the API
    api.add_resource(OrderEndPoint, '/v1/orders',
                     resource_class_kwargs={'db_handler': db_handler})

    api.add_resource(TradeEndPoint, '/v1/trades',
                     resource_class_kwargs={'db_handler': db_handler})
    return app