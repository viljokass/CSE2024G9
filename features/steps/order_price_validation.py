import json
from behave import *
from scheduler import fetch_last_traded_price


@given('current market last trade price is "{market_price}" as M1')
def get_last_traded_price(context, market_price):
    price = float(market_price)
    context.db_handler.record_last_traded_price(price)
    context.last_traded_price = context.db_handler.get_last_traded_price()
    assert context.last_traded_price == price


@when('I submit "{order}" with price of M1 x "{multiplier}" with quantity of "{quantity}"')
def submit_order(context, order, multiplier, quantity):
    price = context.last_traded_price * float(multiplier)
    context.order_type = order
    context.order_price = price
    context.order_quantity = int(quantity)
    context.response = context.client.post("/v1/orders", json = {
        "type": context.order_type,
        "price": context.order_price,
        "quantity": context.order_quantity
    })
    assert context.response


@then('order is accepted')
def validate_response(context):
    assert context.response.status_code == 201

    # verify order is in db, but no trades have happened
    orders_json = context.db_handler.get_orders()
    orders = json.loads(orders_json)
    assert orders[0]['type'] == context.order_type
    assert orders[0]['price'] == context.order_price
    assert orders[0]['quantity'] == context.order_quantity

    trades_json = context.db_handler.get_trades()
    trades = json.loads(trades_json)
    assert len(trades) == 0


@then('order is rejected')
def validate_response(context):
    assert context.response.status_code == 406 or context.response.status_code == 400
    
    # verify order is not in db, and no trades have happened
    orders_json = context.db_handler.get_orders()
    orders = json.loads(orders_json)
    assert len(orders) == 0

    trades_json = context.db_handler.get_trades()
    trades = json.loads(trades_json)
    assert len(trades) == 0
