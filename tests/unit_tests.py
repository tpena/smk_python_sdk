import types
import unittest

from contextlib import contextmanager
from itertools import chain, product
from mock import Mock, patch, sentinel
from nose.tools import eq_

import smarkets.eto.piqi_pb2 as eto
import smarkets.seto.piqi_pb2 as seto
import smarkets.uuid as uuid

from smarkets.clients import Callback, Smarkets
from smarkets.exceptions import InvalidCallbackError
from smarkets.orders import OrderCreate, OrderCancel, BUY


class CallbackTestCase(unittest.TestCase):

    "Test the `smarkets.Callback` class"

    def setUp(self):
        "Set up the tests"
        self.callback = Callback()

    def tearDown(self):
        "Tear down the test requirements"
        self.callback = None

    def test_simple_fire(self):
        "Test the simple case where the handler fires"
        handler = Mock()
        self.callback += handler
        self.assertFalse(handler.called)
        self.assertEquals(1, len(self.callback))
        self.callback(sentinel.message)
        handler.assert_called_once_with(sentinel.message)
        self.assertEquals(1, len(self.callback))

    def test_unhandle(self):
        "Test the case where a handler is removed"
        handler = Mock()
        self.callback += handler
        self.assertFalse(handler.called)
        self.assertEquals(1, len(self.callback))
        self.callback -= handler
        self.assertEquals(0, len(self.callback))
        self.callback(sentinel.message)
        self.assertFalse(handler.called)

    def test_2_handlers(self):
        "Test 2 handlers both get called"
        handler1 = Mock()
        handler2 = Mock()
        self.callback += handler1
        self.callback += handler2
        self.assertFalse(handler1.called)
        self.assertFalse(handler2.called)
        self.assertEquals(2, len(self.callback))
        self.callback(sentinel.message)
        handler1.assert_called_once_with(sentinel.message)
        handler2.assert_called_once_with(sentinel.message)
        self.assertEquals(2, len(self.callback))

    def test_many_handlers(self):
        "General version of `test_2_handlers`"
        handlers = [Mock() for _ in xrange(1, 100)]
        for handler in handlers:
            self.callback += handler
        self.assertEquals(len(handlers), len(self.callback))
        for handler in handlers:
            self.assertFalse(handler.called)
        self.callback(sentinel.message)
        for handler in handlers:
            handler.assert_called_once_with(sentinel.message)
        self.assertEquals(len(handlers), len(self.callback))

    def test_many_unhandle(self):
        "Unhandle many"
        real_handlers = [Mock() for _ in xrange(1, 100)]
        to_unhandle = [Mock() for _ in xrange(1, 20)]
        for handler in chain(real_handlers, to_unhandle):
            self.callback += handler
        self.assertEquals(
            len(real_handlers) + len(to_unhandle), len(self.callback))
        for handler in to_unhandle:
            self.callback -= handler
        self.assertEquals(len(real_handlers), len(self.callback))
        self.callback(sentinel.message)
        for handler in to_unhandle:
            self.assertFalse(handler.called)
        for handler in real_handlers:
            handler.assert_called_once_with(sentinel.message)

    def test_handle_exception(self):
        "Test that an exception is raised by the callback method"
        handler = Mock(side_effect=self._always_raise)
        self.callback += handler
        self.assertRaises(Exception, self.callback, sentinel.message)

    def test_2_handle_exception(self):
        "Test that an exception is raised by the callback method"
        handler1 = Mock(side_effect=self._always_raise)
        handler2 = Mock()
        self.callback += handler1
        self.callback += handler2
        self.assertRaises(Exception, self.callback, sentinel.message)
        # Because the collection of handlers in the `Callback` is a
        # `set` the 'firing' order is undefined. However, if handler2
        # is called, we assert that it is called correctly here.
        if handler2.called:
            handler2.assert_called_once_with(sentinel.message)

    @staticmethod
    def _always_raise(*args, **kwargs):
        "Always raise `Exception` with no arguments"
        raise Exception()


class Handler(object):
    call_count = 0

    def __call__(self, *args, **kwargs):
        self.call_count += 1


class SmarketsTestCase(unittest.TestCase):

    "Tests for the `smarkets.Smarkets` client object"

    def setUp(self):
        "Patch the `Session` object for mock use"
        self.session_patcher = patch('smarkets.sessions.Session')
        self.mock_session_cls = self.session_patcher.start()
        self.mock_session = self.mock_session_cls.return_value
        self.client = Smarkets(self.mock_session)

    def tearDown(self):
        "Stop the patcher"
        self.session_patcher.stop()
        self.mock_session_cls = None
        self.mock_session = None
        self.client = None

    def test_login(self):
        "Test the `Smarkets.login` method"
        payload = self._login_response()
        self.mock_session.next_frame.return_value = payload
        response = Mock()
        self.client.add_handler('eto.login_response', response)
        self.client.login()
        self.assertEquals(
            self.mock_session.method_calls,
            [('connect', (), {}), ('next_frame', (), {})])
        response.assert_called_once_with(payload)

    def test_login_norecv(self):
        "Test the `Smarkets.login` method"
        payload = self._login_response()
        self.mock_session.next_frame.return_value = payload
        response = Mock()
        self.client.add_handler('eto.login_response', response)
        self.client.login(False)
        self.assertEquals(
            self.mock_session.method_calls,
            [('connect', (), {})])
        self.assertFalse(response.called)
        self.mock_session.reset_mock()
        self.client.read()
        self.assertEquals(
            self.mock_session.method_calls,
            [('next_frame', (), {})])
        response.assert_called_once_with(payload)

    def test_logout(self):
        "Test the `Smarkets.logout` method"
        self.client.logout()
        self.assertEquals(
            self.mock_session.method_calls,
            [('logout', (), {}),
             ('next_frame', (), {}),
             ('disconnect', (), {})])

    def test_logout_norecv(self):
        "Test the `Smarkets.logout` method"
        self.client.logout(False)
        self.assertEquals(
            self.mock_session.method_calls,
            [('logout', (), {}),
             ('disconnect', (), {})])

    def test_each_instance_has_separate_callbacks(self):
        client_a, client_b = (Smarkets('_') for i in range(2))
        handler = Handler()
        client_a.add_handler('seto.http_found', handler)
        eq_(handler.call_count, 0)

        client_a.callbacks['seto.http_found']('irrelevant')
        eq_(handler.call_count, 1)

        client_b.callbacks['seto.http_found']('also irrelevant')
        eq_(handler.call_count, 1)

    def test_flush(self):
        "Test the `Smarkets.flush` method"
        self.client.flush()
        self.assertEquals(
            self.mock_session.method_calls,
            [('flush', (), {})])

    def test_order(self):
        "Test the `Smarkets.order` method"
        market_id = self.client.str_to_uuid128('1c024')
        contract_id = self.client.str_to_uuid128('1cccc')
        with self._clear_send():
            order = OrderCreate()
            order.price = 2500
            order.quantity = 10000
            order.side = BUY
            order.market = market_id
            order.contract = contract_id
            order.validate_new()
            self.client.send(order)

    def test_order_cancel(self):
        "Test the `Smarkets.order_cancel` method"
        order_id = self.client.str_to_uuid128('1fff0')
        with self._clear_send():
            self.client.send(OrderCancel(order_id))

    def test_ping(self):
        "Test the `Smarkets.ping` method"
        with self._clear_send():
            self.client.ping()

    def test_subscribe(self):
        "Test the `Smarkets.subscribe` method"
        market_id = self.client.str_to_uuid128('1c024')
        with self._clear_send():
            self.client.subscribe(market_id)

    def test_unsubscribe(self):
        "Test the `Smarkets.unsubscribe` method"
        market_id = self.client.str_to_uuid128('1c024')
        with self._clear_send():
            self.client.unsubscribe(market_id)

    def test_request_events(self):
        "Test the `Smarkets.request_events` method"
        with patch('smarkets.events.Politics') as mock_politics:
            request = mock_politics.return_value
            with self._clear_send():
                self.client.request_events(request)
            request.copy_to.assert_called_once_with(
                self.mock_session.out_payload)

    def test_fetch_http_found(self):
        "Test the `Smarkets.fetch_http_found` method"
        mock_fetch = Mock()
        self.client.fetch = mock_fetch
        expected = seto.Events()
        payload_bytes = expected.SerializeToString()
        mock_fetch.return_value = ('application/x-protobuf', payload_bytes)
        payload = seto.Payload()
        payload.type = seto.PAYLOAD_HTTP_FOUND
        payload.http_found.url = 'http://domain.invalid/url'
        payload.http_found.seq = 2
        self.assertEqual(expected, self.client.fetch_http_found(payload))
        mock_fetch.assert_called_once_with(payload.http_found.url)

    def test_add_bad_handler(self):
        "Test trying to add a bad handler either as a global or normal"
        for bad_handler in (
                50, 'foo', False, True, u'foo', 1.2, 1L):
            self.assertRaises(
                ValueError, self.client.add_handler, 'eto.pong', bad_handler)
            self.assertRaises(
                ValueError, self.client.add_global_handler, bad_handler)

    def test_add_unknown_handler(self):
        "Test trying to add a handler for an unknown callback name"
        handler = lambda: None
        self.assertRaises(
            InvalidCallbackError, self.client.add_handler, 'foo', handler)
        self.assertRaises(
            InvalidCallbackError, self.client.del_handler, 'foo', handler)

    @contextmanager
    def _clear_send(self):
        """
        Shortcut for asserting that the outgoing payload is cleared
        and sent via the session
        """
        self.mock_session.out_payload.Clear = Mock()
        yield
        self.mock_session.send.assert_called_once_with(True)
        self.assertEquals(1, self.mock_session.out_payload.Clear.call_count)

    @staticmethod
    def _login_response():
        "Create a dummy login response payload"
        payload = seto.Payload()
        payload.eto_payload.seq = 1
        payload.eto_payload.type = eto.PAYLOAD_LOGIN_RESPONSE
        payload.eto_payload.login_response.session = 'session'
        payload.eto_payload.login_response.reset = 2
        return payload


class UuidTestCase(unittest.TestCase):

    "Unit tests for Uuids"

    def test_int_roundtrip(self):
        "Test converting an integer to a Uuid and back"
        ttype = 'Account'
        for i in chain(xrange(1, 1000), product(xrange(1, 10), repeat=2)):
            u1 = uuid.int_to_uuid(i, ttype)
            u2, test_ttype = uuid.uuid_to_int(u1, return_tag='type', split=isinstance(i, tuple))
            self.assertEquals(i, u2)
            self.assertEquals(test_ttype, ttype)
            u3 = uuid.int_to_slug(i, ttype)
            u4, test_ttype = uuid.slug_to_int(u3, return_tag='type', split=isinstance(i, tuple))
            self.assertEquals(i, u4)
            self.assertEquals(test_ttype, ttype)

    def test_uuid_roundtrip(self):
        "Test converting a hex string to a Uuid and back"
        suffix = 'acc1'
        for i in xrange(1, 1000):
            hex_str = '%x%s' % (i, suffix)
            hex_str = '0' * (32 - len(hex_str)) + hex_str
            u1, ttype = uuid.uuid_to_int(hex_str, return_tag='type')
            self.assertEquals(ttype, 'Account')
            u2 = uuid.int_to_uuid(u1, ttype)
            self.assertEquals(u2, hex_str)
            u3 = uuid.uuid_to_slug(hex_str)
            u4 = uuid.slug_to_uuid(u3)
            self.assertEquals(u4, hex_str)

    def test_uuid_tag(self):
        "Test UuidTag class"
        tag = uuid.Uuid.tags.get('Account')
        self.assertEquals(tag.name, 'Account')
        self.assertEquals(tag.hex_str, 'acc1')
        self.assertEquals(tag.prefix, 'a')
        self.assertEquals(tag.int_tag, 44225)
        tagged_8 = tag.tag_number(8)
        self.assertEquals(tagged_8, int('8acc1', 16))
        self.assertEquals(tag.split_int_tag(tagged_8), (8, tag.int_tag))

    def test_uuid_high_low(self):
        "Test Uuid class support for high/low number"
        tag = uuid.Uuid.tags.get('Account')
        uuid1 = uuid.Uuid(73786976294838235846L, tag)
        self.assertEquals(uuid1.low, 29382)
        self.assertEquals(uuid1.high, 4)
        uuid2 = uuid.Uuid(5, tag)
        self.assertEquals(uuid2.low, 5)
        self.assertEquals(uuid2.high, 0)

    def test_uuid_shorthex(self):
        "Test Uuid class support for short hex values"
        tag = uuid.Uuid.tags.get('Account')
        uuid1 = uuid.Uuid(73786976294838235846L, tag)
        self.assertEquals(uuid1.shorthex, '400000000000072c6')
        uuid2 = uuid.Uuid(5, tag)
        self.assertEquals(uuid2.shorthex, '5')

    def test_bad_base_raises(self):
        "Test that Uuid class raises TypeError when given a bad 'base' value"
        tag = uuid.Uuid.tags.get('Account')
        uuid1 = uuid.Uuid(73786976294838235846L, tag)
        self.assertRaises(TypeError, lambda: uuid1.to_slug(base=90))
        self.assertRaises(TypeError, lambda: uuid1.to_slug(base=1))
        self.assertRaises(TypeError, lambda: uuid1.to_slug(base=-1))
        self.assertRaises(TypeError, lambda: uuid1.to_slug(chars='abc', base=4))

    def test_slug(self):
        "Test that Uuid can be converted to/from slugs"
        tag = uuid.Uuid.tags.get('Account')
        uuid1 = uuid.Uuid(73786976294838235846L, tag)
        slug = 'a-lvgb2h48s4kweqbl'
        self.assertEquals(uuid1.to_slug(), slug)
        self.assertEquals(uuid1.to_slug(base=16)[2:], uuid1.to_hex().lstrip('0'))
        uuid2 = uuid.Uuid.from_slug(slug)
        self.assertEquals(uuid1, uuid2)

    def test_hex(self):
        "Test that Uuid can be converted to/from hex"
        tag = uuid.Uuid.tags.get('Account')
        uuid1 = uuid.Uuid(73786976294838235846L, tag)
        hex_str = '00000000000400000000000072c6acc1'
        self.assertEquals(uuid1.to_hex(), hex_str)
        self.assertEquals(uuid1.shorthex, hex_str.lstrip('0')[:-4])
        self.assertEquals(uuid1.to_hex(pad=0)[:-4], uuid1.shorthex)
        uuid2 = uuid.Uuid.from_hex(hex_str)
        self.assertEquals(uuid1, uuid2)
        self.assertRaises(TypeError, lambda: uuid.Uuid.from_hex(10))
        self.assertRaises(ValueError, lambda: uuid.Uuid.from_hex('aa0000'))

    def test_int(self):
        "Test that Uuid can be converted to/from integer"
        tag = uuid.Uuid.tags.get('Account')
        number = 73786976294838235846L
        low = 29382
        high = 4
        uuid1 = uuid.Uuid(number, tag)
        uuid2 = uuid.Uuid.from_int(number, 'Account')
        self.assertEqual(uuid1, uuid2)
        self.assertEqual(uuid2.number, number)
        self.assertEqual(uuid2.high, high)
        self.assertEqual(uuid2.low, low)
        uuid3 = uuid.Uuid.from_int((high, low), 'Account')
        self.assertEquals(uuid1, uuid3)
        self.assertRaises(TypeError, lambda: uuid.Uuid.from_int('foo', 'Account'))
        self.assertRaises(TypeError, lambda: uuid.Uuid.from_int(-100, 'Account'))
        self.assertRaises(ValueError, lambda: uuid.Uuid.from_int(1, 'invalid-type'))

    def test_uuid_tag_lengths(self):
        "Test that all uuid tags are 4 characters long (zero-padded)"
        for tag in uuid.Uuid.tag_list:
            self.assertTrue(isinstance(tag.hex_str, types.StringTypes))
            self.assertEquals(4, len(tag.hex_str))

    def test_slugs_without_prefix(self):
        "Test that slugs without prefixes are supported"
        slug = 'a-lvgb2h48s4kweqbl'
        slug_no_prefix = 'lvgb2h48s4kweqbl'
        uuid_prefix = uuid.Uuid.from_slug(slug)
        uuid_no_prefix = uuid.Uuid.from_slug(slug_no_prefix)
        self.assertEqual(uuid_prefix, uuid_no_prefix)
