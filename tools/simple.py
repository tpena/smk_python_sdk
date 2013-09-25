# -*- coding: utf-8 -*-

import logging
import smarkets.seto.piqi_pb2 as seto

logging.basicConfig(level=logging.DEBUG)

import smarkets

from google.protobuf import text_format

current_order_id = None

def _on_order_accepted_handler(msg):
    global current_order_id
    current_order_id = msg.order_accepted.order.low
    print "ACCEPTED ORDER: %s" % current_order_id


def create_client():
    username = 'tito+euro@betacular.com'
    password = 'Gq7dbfq6DetHwn8y'
    settings = smarkets.SessionSettings(username, password)
    settings.host = 'api.smarkets.com'
    settings.port = 3801
    settings.ssl = True
    session = smarkets.Session(settings)
    client = smarkets.Smarkets(session)
    client.login()

    return client


# def fillOrKillTest():
#     logging.info("########################### FILL OR KILL ###############################")
#     client = create_client()
#
#     order = smarkets.orders.FillOrKillOrder()
#     order.quantity = 4000
#     order.price = 5000
#     order.side = smarkets.Order.BUY
#     order.market = client.str_to_uuid128('0000000000000000000000002c7ec024')
#     #order.contract = client.str_to_uuid128('0000000000000000000000005c87cccc')
#     #order.contract = client.str_to_uuid128('0000000000000000000000005c89cccc')
#     order.contract = client.str_to_uuid128('0000000000000000000000005c88cccc')
#     client.order(order)
#     client.flush()
#     client.read(5)
#
#     client.logout()
#     logging.info("########################### FILL OR KILL ###############################")


def simpleLoginLogout():
    logging.info("########################### TEST2 ###############################")
    client = create_client()
    client.logout()
    client.flush()
    logging.info("########################### TEST2 ###############################")


def place_order(market_id, contract_id):
    logging.info("########################### ORDER ###############################")

    client = create_client()
    _place_order(client, market_id, contract_id, seto.IMMEDIATE_OR_CANCEL)

    client.logout()
    client.flush()

    logging.info("########################### ORDER ###############################")


def _place_order(client, market_id, contract_id, time_in_force):
    market = client.str_to_uuid128(market_id)

    order = smarkets.orders.OrderCreate()
    order.quantity = 2000
    order.price = 5000
    order.side = smarkets.orders.BUY
    order.market = market
    order.contract = client.str_to_uuid128(contract_id)
    order.time_in_force = time_in_force
    order.validate_new()

    client.send(order)
    client.flush()
    client.read(2)


def cancel_order(market_id, contract_id):
    logging.info("########################### CANCEL ORDER ###############################")

    client = create_client()
    client.add_handler('seto.order_accepted', _on_order_accepted_handler)

    _place_order(client, market_id, contract_id, seto.GOOD_TIL_CANCELLED)

    global current_order_id
    if current_order_id is not None:
        cancel_order = smarkets.orders.OrderCancel()
        cancel_order.uid = smarkets.uuid.int_to_uuid128(current_order_id)
        cancel_order.validate_new()

        client.send(cancel_order)
        client.flush()
        client.read(1)
    else:
        print "ERROR: NO ORDER ID FOUND"

    client.logout()
    client.flush()

    logging.info("########################### CANCEL ORDER ###############################")

# def market_quotes(market_id):
#     logging.info("########################### MARKET_QUOTES ###############################")
#     client = create_client()
#     market = client.str_to_uuid128(market_id)
#     client.market_quotes(market)
#     client.flush()
#     client.read(5)
#     client.logout()
#     client.flush()
#     logging.info("########################### MARKET_QUOTES ###############################")
#
#
# def market_subscribe(market_id):
#     logging.info("########################### SUBSCRIBE ###############################")
#     client = create_client()
#     market = client.str_to_uuid128(market_id)
#     client.subscribe(market)
#     client.flush()
#     client.read(5)
#     client.logout()
#     client.flush()
#     logging.info("########################### SUBSCRIBE ###############################")

# def orders_for_account():
#     logging.info("########################### ORDERS_FOR_ACCOUNT ###############################")
#     client = create_client()
#     client.add_handler('seto.orders_for_account', orders_for_account_handler)
#     client.request_orders_for_account()
#     client.flush()
#     client.read(2)
#     client.logout()
#     client.flush()
#     logging.info("########################### ORDERS_FOR_ACCOUNT ###############################")

# def orders_for_account_handler(payload):
#     text_format.MessageToString(payload)


if __name__ == '__main__':
    simpleLoginLogout()
    #place_order('00000000000000000000002cb3c6c024', '000000000000000000000075f3e8cccc')
    #cancel_order('00000000000000000000002e64f6c024', '0000000000000000000000798fd2cccc')

