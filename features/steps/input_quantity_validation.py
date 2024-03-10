import json

from behave import *


@given('current market last trade price is "200" as M2')
def get_last_traded_price(context):
    price = 200.00
    context.db_handler.record_last_traded_price(price)
    context.last_traded_price = context.db_handler.get_last_traded_price()
    assert context.last_traded_price == price


@when('I submit "{order}" with price of "{price}" and quantity of "{quantity}"')
def submit_order(context, order, quantity, price):
    context.order_type = order
    context.order_price = price
    context.order_quantity = quantity
    context.response = context.client.post("/v1/orders", json={
        "type": context.order_type,
        "price": context.order_price,
        "quantity": context.order_quantity
    })
    assert context.response


@then('order is rejected due to invalid quantity')
def validate_response(context):
    assert context.response.status_code == 406
    assert context.response.json['message'] == "Order rejected - Quantity error"

    # verify order is not in db, and no trades have happened
    orders_json = context.db_handler.get_orders()
    orders = json.loads(orders_json)
    assert len(orders) == 0

    trades_json = context.db_handler.get_trades()
    trades = json.loads(trades_json)
    assert len(trades) == 0
