# -*- coding: utf-8 -*-

import logging

logging.basicConfig(level=logging.DEBUG)

import smarkets
import smarkets.uuid

from google.protobuf import text_format

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


def fillOrKillTest():
    logging.info("########################### FILL OR KILL ###############################")
    client = create_client()

    order = smarkets.orders.FillOrKillOrder()
    order.quantity = 4000
    order.price = 5000
    order.side = smarkets.Order.BUY
    order.market = client.str_to_uuid128('0000000000000000000000002c7ec024')
    #order.contract = client.str_to_uuid128('0000000000000000000000005c87cccc')
    #order.contract = client.str_to_uuid128('0000000000000000000000005c89cccc')
    order.contract = client.str_to_uuid128('0000000000000000000000005c88cccc')
    client.order(order)
    client.flush()
    client.read(5)

    client.logout()
    logging.info("########################### FILL OR KILL ###############################")


def simpleLoginLogout():
    logging.info("########################### TEST2 ###############################")
    client = create_client()
    client.logout()
    client.flush()
    logging.info("########################### TEST2 ###############################")


def place_order(market_id, contract_id):
    logging.info("########################### ORDER ###############################")

    client = create_client()

    market = client.str_to_uuid128(market_id)

    order = smarkets.orders.Order()
    order.quantity = 2000
    order.price = 5000
    order.side = smarkets.orders.BUY
    order.market = market
    order.contract = client.str_to_uuid128(contract_id)

    client.order(order)
    client.flush()
    client.read(2)

    client.flush()
    client.read()

    client.logout()
    client.flush()

    logging.info("########################### ORDER ###############################")


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
    print smarkets.uuid.int_to_uuid(5815765, 'Contract')
    place_order('00000000000000000000002cb3c6c024', '000000000000000000000075f3e8cccc')
    #simpleLoginLogout()

