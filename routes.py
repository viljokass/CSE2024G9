from flask import Flask
from flask_restful import reqparse, Api, Resource
from db_handler import DbHandler
from models.order import Order

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
            return {"message": "Price too low - must be within 10% of the last traded price."}, 406
        if (unit_price > 1.10 * last_traded_price):
            return {"message": "Price too high - must be within 10% of the last traded price."}, 406

        # Create a data object
        try:
            order = Order(type=order_type, price=unit_price, quantity=quantity)
        except ValueError as e:
            return {"message": str(e)}, 406

        # Add order to the database
        self.db_handler.record_order(order)

        # Return a proper response to the sender
        return {"message": "Order received and recorded"}, 201

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