import json
from behave import *

@then('there exists trades')
def validate_response(context):

    trades_json = context.db_handler.get_trades()
    trades = json.loads(trades_json)
    assert len(trades) == len(context.table.rows)
    index = 0
    for excpexted_trade in context.table: 
        assert trades[index]['price'] == float(excpexted_trade.cells[1])
        assert trades[index]['quantity'] == int(excpexted_trade.cells[2])

        index = index + 1