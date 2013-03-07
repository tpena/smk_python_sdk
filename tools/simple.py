# -*- coding: utf-8 -*-

import logging
logging.basicConfig(level=logging.DEBUG)

import smarkets

def create_client():
    username = 'xxx'
    password = 'xxx'
    settings = smarkets.SessionSettings(username, password)
    settings.host = 'api.smarkets.com'
    settings.port = 3701
    settings.ssl = True
    session = smarkets.Session(settings)
    client = smarkets.Smarkets(session)
    client.login()

    return client

def fillOrKillTest():
    logging.info("########################### FILL OR KILL ###############################")
    client = create_client()

    order = smarkets.orders.FillOrKillOrder()
    order.quantity = 2000
    order.price = 5000
    order.side = smarkets.Order.BUY
    order.market = client.str_to_uuid128('00000000000000000000001a6ae9c024')
    #order.contract = client.str_to_uuid128('00000000000000000000004ebfb7cccc')
    order.contract = client.str_to_uuid128('00000000000000000000004ebfbdcccc')
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


if __name__ == '__main__':
    fillOrKillTest()

