from behave import *
from scheduler import fetch_last_traded_price


@given('current market last trade price is M1')
def get_last_traded_price(context):
    context.last_traded_price = fetch_last_traded_price()
    #get last_traded_price in mockdb instead calling the method.


@when('I submit "{order}" with price of M1 x "{multiplier}"')
def submit_order(context, order, multiplier):
    unit_price = context.last_traded_price * float(multiplier)
    context.response = context.client.post("/v1/orders", json = {
        "order_type": order,
        "unit_price": unit_price,
        "quantity": 100
    })
    assert context.response


@then('order is accepted')
def validate_response(context):
    pass
    # TODO after db uncomment:
    # assert context.response.status_code == 201
    # TODO verify order is in db, but no trades have happened


@then('order is rejected')
def validate_response(context):
    pass
    # TODO after db uncomment:
    # assert context.response.status_code == 400
    # TODO verify order is not in db, and no trades have happened
