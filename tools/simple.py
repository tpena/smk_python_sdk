# -*- coding: utf-8 -*-

import logging
logging.basicConfig(level=logging.DEBUG)

from smarkets.streaming_api.session import Session, SessionSettings
from smarkets.streaming_api.client import StreamingAPIClient
from smarkets.streaming_api.orders import OrderCreate

import smarkets.streaming_api.seto as seto

from google.protobuf import text_format

def _border(name):
    return "########################### %s ###############################" % name

def create_client():
    username = 'tito+euro@betacular.com'
    password = 'Gq7dbfq6DetHwn8y'
    settings = SessionSettings(username, password)
    settings.host = 'api.smarkets.com'
    settings.port = 3801
    settings.ssl = True
    session = Session(settings)
    client = StreamingAPIClient(session)
    client.login()

    return client

def place_fill_or_kill_order():
    _place_order('000000000000000000000020d3ccc024', '00000000000000000000005c677ecccc', True)

def place_order():
    _place_order('000000000000000000000020d3ccc024', '00000000000000000000005c677ecccc', False)

def _place_order(market, contract, is_fok):
    if is_fok:
        title = "FILL OR KILL ORDER"
    else:
        title = "ORDER"

    logging.info(_border(title))
    client = create_client()

    order = OrderCreate()
    order.quantity = 2000
    order.min_accepted_quantity = 2000
    order.time_in_force = seto.IMMEDIATE_OR_CANCEL
    order.price = 5000
    order.side = smarkets.Order.BUY
    order.market = client.str_to_uuid128(market)
    order.contract = client.str_to_uuid128(contract)

    if is_fok:
        order.min_accepted_quantity = order.quantity
        order.time_in_force = seto.IMMEDIATE_OR_CANCEL

    client.order(order)
    client.flush()
    client.read(3)

    client.logout()
    logging.info(_border(title))

def simple_login_logout():
    logging.info("########################### SIMPLE LOGIN ###############################")
    client = create_client()
    client.logout()
    client.flush()
    logging.info("########################### SIMPLE LOGIN ###############################")

def market_quotes():
    logging.info("########################### MARKET_QUOTES ###############################")
    client = create_client()
    market = client.str_to_uuid128('00000000000000000000001f2515c024')
    client.market_quotes(market)
    client.flush()
    client.read(5)
    client.logout()
    client.flush()
    logging.info("########################### MARKET_QUOTES ###############################")


def market_subscribe():
    logging.info("########################### SUBSCRIBE ###############################")
    client = create_client()
    market = client.str_to_uuid128('00000000000000000000001f2515c024')
    client.subscribe(market)
    client.flush()
    client.read(5)
    client.logout()
    client.flush()
    logging.info("########################### SUBSCRIBE ###############################")

def orders_for_account():
    logging.info("########################### ORDERS_FOR_ACCOUNT ###############################")
    client = create_client()
    client.add_handler('seto.orders_for_account', orders_for_account_handler)
    client.request_orders_for_account()
    client.flush()
    client.read(2)
    client.logout()
    client.flush()
    logging.info("########################### ORDERS_FOR_ACCOUNT ###############################")

def orders_for_account_handler(payload):
    text_format.MessageToString(payload)


if __name__ == '__main__':
    import smarkets.uuid
    print smarkets.uuid.int_to_uuid(5815765, 'Contract')
    simple_login_logout()
    #orders_for_account()

