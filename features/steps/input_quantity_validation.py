import json
from behave import *


@given('current market last trade price is "200" as M2')
def get_last_traded_price(context):
    price = 200.00
    context.db_handler.record_last_traded_price(price)
    context.last_traded_price = context.db_handler.get_last_traded_price()
    assert context.last_traded_price == price


@when('I submit "{order}" with price of "200" and quantity of "{quantity}"')
def submit_order(context, order, quantity):
    context.order_type = order
    context.order_price = 200
    context.order_quantity = quantity
    context.response = context.client.post("/v1/orders", json={
        "type": context.order_type,
        "price": context.order_price,
        "quantity": context.order_quantity
    })
    assert context.response