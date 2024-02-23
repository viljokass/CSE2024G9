from flask import Flask
from flask_restful import reqparse, Api, Resource

# Create the parser object to be used in the order end point
parser = reqparse.RequestParser()

# Add arguments to the parser object
#
# Order type: A string. Has to be validated later
parser.add_argument("order_type", type=str, required=True)
# Unit price: Converts the argument to float. Raises an error if the value can not be parsed
parser.add_argument("unit_price", type=float, required=True)
# Quantity: Converts the argument to integer. Raises an error if the value can not be parsed
parser.add_argument("quantity", type=int, required=True)

# Endpoint for posting an order
class OrderEndPoint(Resource):
    
    def post(self):
        # Parse the arguments from the data
        arguments = parser.parse_args()

        # get the data from arguments
        order_type  = arguments["order_type"]
        unit_price  = arguments["unit_price"]
        quantity    = arguments["quantity"]

        # If order type is not Offer or Bid, return an error
        if (order_type not in ["Offer", "Bid"]):
            return {"message": "Undefined order type - Order type must be either Offer or Bid."}, 400
        
        # TODO - Check data validity using AAPL trade price
        # TODO - Add order to the database

        # Return a proper response to the sender
        return {"message": "Order received and processed."}, 201

# Endpoint for getting trades
class TradeEndPoint(Resource):

    def get(self):
        # TODO - fetch the trade information from the database
        return {"message": "Here's some trades for you!"}, 200

def create_app():
    app = Flask(__name__)
    api = Api(app)
    # Add the endpoints to the API
    api.add_resource(OrderEndPoint, '/v1/orders')
    api.add_resource(TradeEndPoint, '/v1/trades')
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)