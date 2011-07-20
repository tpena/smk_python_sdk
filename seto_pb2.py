# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message as gmessage
from google.protobuf import reflection
from google.protobuf import service
from google.protobuf import service_reflection
from google.protobuf import descriptor_pb2
_ORDER_REJECTED_REASON = descriptor.EnumDescriptor(
  name='order_rejected_reason',
  full_name='order_rejected_reason',
  filename='order_rejected_reason',
  values=[
    descriptor.EnumValueDescriptor(
      name='insufficient_funds', index=0, number=1,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='limit_exceeded', index=1, number=2,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='market_not_open', index=2, number=3,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='market_settled', index=3, number=4,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='market_halted', index=4, number=5,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='crossed_self', index=5, number=6,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='error', index=6, number=7,
      options=None,
      type=None),
  ],
  options=None,
)


_ORDER_CANCELLED_REASON = descriptor.EnumDescriptor(
  name='order_cancelled_reason',
  full_name='order_cancelled_reason',
  filename='order_cancelled_reason',
  values=[
    descriptor.EnumValueDescriptor(
      name='member_requested', index=0, number=1,
      options=None,
      type=None),
  ],
  options=None,
)


_SIDE = descriptor.EnumDescriptor(
  name='side',
  full_name='side',
  filename='side',
  values=[
    descriptor.EnumValueDescriptor(
      name='buy', index=0, number=1,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='sell', index=1, number=2,
      options=None,
      type=None),
  ],
  options=None,
)


insufficient_funds = 1
limit_exceeded = 2
market_not_open = 3
market_settled = 4
market_halted = 5
crossed_self = 6
error = 7
member_requested = 1
buy = 1
sell = 2



_MESSAGE = descriptor.Descriptor(
  name='message',
  full_name='message',
  filename='seto.proto',
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='seq', full_name='message.seq', index=0,
      number=1, type=17, cpp_type=1, label=2,
      default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='payload', full_name='message.payload', index=1,
      number=2, type=11, cpp_type=10, label=2,
      default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='replay', full_name='message.replay', index=2,
      number=3, type=8, cpp_type=7, label=1,
      default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],  # TODO(robinson): Implement.
  enum_types=[
  ],
  options=None)


_REPLAY_PAYLOAD = descriptor.Descriptor(
  name='replay_payload',
  full_name='replay_payload',
  filename='seto.proto',
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='seq', full_name='replay_payload.seq', index=0,
      number=1, type=17, cpp_type=1, label=2,
      default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],  # TODO(robinson): Implement.
  enum_types=[
  ],
  options=None)


_LOGIN_RESPONSE_PAYLOAD = descriptor.Descriptor(
  name='login_response_payload',
  full_name='login_response_payload',
  filename='seto.proto',
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='session', full_name='login_response_payload.session', index=0,
      number=1, type=12, cpp_type=9, label=2,
      default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],  # TODO(robinson): Implement.
  enum_types=[
  ],
  options=None)


_RANGE_PAYLOAD = descriptor.Descriptor(
  name='range_payload',
  full_name='range_payload',
  filename='seto.proto',
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='from', full_name='range_payload.from', index=0,
      number=1, type=17, cpp_type=1, label=2,
      default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='to', full_name='range_payload.to', index=1,
      number=2, type=17, cpp_type=1, label=2,
      default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],  # TODO(robinson): Implement.
  enum_types=[
  ],
  options=None)


_ORDER_PAYLOAD = descriptor.Descriptor(
  name='order_payload',
  full_name='order_payload',
  filename='seto.proto',
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='quantity', full_name='order_payload.quantity', index=0,
      number=1, type=17, cpp_type=1, label=2,
      default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='price', full_name='order_payload.price', index=1,
      number=2, type=12, cpp_type=9, label=2,
      default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='side', full_name='order_payload.side', index=2,
      number=3, type=14, cpp_type=8, label=2,
      default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='group', full_name='order_payload.group', index=3,
      number=4, type=12, cpp_type=9, label=2,
      default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='contract', full_name='order_payload.contract', index=4,
      number=5, type=12, cpp_type=9, label=2,
      default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],  # TODO(robinson): Implement.
  enum_types=[
  ],
  options=None)


_ORDER_ACCEPTED_PAYLOAD = descriptor.Descriptor(
  name='order_accepted_payload',
  full_name='order_accepted_payload',
  filename='seto.proto',
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='seq', full_name='order_accepted_payload.seq', index=0,
      number=1, type=17, cpp_type=1, label=2,
      default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='order', full_name='order_accepted_payload.order', index=1,
      number=2, type=12, cpp_type=9, label=2,
      default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],  # TODO(robinson): Implement.
  enum_types=[
  ],
  options=None)


_ORDER_REJECTED_PAYLOAD = descriptor.Descriptor(
  name='order_rejected_payload',
  full_name='order_rejected_payload',
  filename='seto.proto',
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='seq', full_name='order_rejected_payload.seq', index=0,
      number=1, type=17, cpp_type=1, label=2,
      default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='reason', full_name='order_rejected_payload.reason', index=1,
      number=2, type=14, cpp_type=8, label=2,
      default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],  # TODO(robinson): Implement.
  enum_types=[
  ],
  options=None)


_ORDER_EXECUTED_PAYLOAD = descriptor.Descriptor(
  name='order_executed_payload',
  full_name='order_executed_payload',
  filename='seto.proto',
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='order', full_name='order_executed_payload.order', index=0,
      number=1, type=12, cpp_type=9, label=2,
      default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='price', full_name='order_executed_payload.price', index=1,
      number=2, type=12, cpp_type=9, label=2,
      default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='quantity', full_name='order_executed_payload.quantity', index=2,
      number=3, type=17, cpp_type=1, label=2,
      default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],  # TODO(robinson): Implement.
  enum_types=[
  ],
  options=None)


_ORDER_CANCEL_PAYLOAD = descriptor.Descriptor(
  name='order_cancel_payload',
  full_name='order_cancel_payload',
  filename='seto.proto',
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='order', full_name='order_cancel_payload.order', index=0,
      number=1, type=12, cpp_type=9, label=2,
      default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],  # TODO(robinson): Implement.
  enum_types=[
  ],
  options=None)


_ORDER_CANCELLED_PAYLOAD = descriptor.Descriptor(
  name='order_cancelled_payload',
  full_name='order_cancelled_payload',
  filename='seto.proto',
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='order', full_name='order_cancelled_payload.order', index=0,
      number=1, type=12, cpp_type=9, label=2,
      default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='reason', full_name='order_cancelled_payload.reason', index=1,
      number=2, type=14, cpp_type=8, label=1,
      default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],  # TODO(robinson): Implement.
  enum_types=[
  ],
  options=None)


_PP = descriptor.Descriptor(
  name='pp',
  full_name='pp',
  filename='seto.proto',
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='contract', full_name='pp.contract', index=0,
      number=1, type=12, cpp_type=9, label=2,
      default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='group', full_name='pp.group', index=1,
      number=2, type=12, cpp_type=9, label=2,
      default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='price', full_name='pp.price', index=2,
      number=3, type=12, cpp_type=9, label=2,
      default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='side', full_name='pp.side', index=3,
      number=4, type=14, cpp_type=8, label=2,
      default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='quantity', full_name='pp.quantity', index=4,
      number=5, type=17, cpp_type=1, label=2,
      default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='ts', full_name='pp.ts', index=5,
      number=6, type=1, cpp_type=5, label=2,
      default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],  # TODO(robinson): Implement.
  enum_types=[
  ],
  options=None)


_LOGIN_PAYLOAD = descriptor.Descriptor(
  name='login_payload',
  full_name='login_payload',
  filename='seto.proto',
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='session', full_name='login_payload.session', index=0,
      number=1, type=12, cpp_type=9, label=1,
      default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='username', full_name='login_payload.username', index=1,
      number=2, type=12, cpp_type=9, label=2,
      default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='password', full_name='login_payload.password', index=2,
      number=3, type=12, cpp_type=9, label=2,
      default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],  # TODO(robinson): Implement.
  enum_types=[
  ],
  options=None)


_MESSAGE_PAYLOAD = descriptor.Descriptor(
  name='message_payload',
  full_name='message_payload',
  filename='seto.proto',
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='ping', full_name='message_payload.ping', index=0,
      number=1, type=8, cpp_type=7, label=1,
      default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='pong', full_name='message_payload.pong', index=1,
      number=2, type=8, cpp_type=7, label=1,
      default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='gapfill', full_name='message_payload.gapfill', index=2,
      number=3, type=8, cpp_type=7, label=1,
      default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='replay', full_name='message_payload.replay', index=3,
      number=4, type=11, cpp_type=10, label=1,
      default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='login', full_name='message_payload.login', index=4,
      number=5, type=11, cpp_type=10, label=1,
      default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='login_response', full_name='message_payload.login_response', index=5,
      number=6, type=11, cpp_type=10, label=1,
      default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='order', full_name='message_payload.order', index=6,
      number=7, type=11, cpp_type=10, label=1,
      default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='order_rejected', full_name='message_payload.order_rejected', index=7,
      number=8, type=11, cpp_type=10, label=1,
      default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='order_accepted', full_name='message_payload.order_accepted', index=8,
      number=9, type=11, cpp_type=10, label=1,
      default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='order_executed', full_name='message_payload.order_executed', index=9,
      number=10, type=11, cpp_type=10, label=1,
      default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='order_cancel', full_name='message_payload.order_cancel', index=10,
      number=11, type=11, cpp_type=10, label=1,
      default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='order_cancelled', full_name='message_payload.order_cancelled', index=11,
      number=12, type=11, cpp_type=10, label=1,
      default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],  # TODO(robinson): Implement.
  enum_types=[
  ],
  options=None)


_MESSAGE.fields_by_name['payload'].message_type = _MESSAGE_PAYLOAD
_ORDER_PAYLOAD.fields_by_name['side'].enum_type = _SIDE
_ORDER_REJECTED_PAYLOAD.fields_by_name['reason'].enum_type = _ORDER_REJECTED_REASON
_ORDER_CANCELLED_PAYLOAD.fields_by_name['reason'].enum_type = _ORDER_CANCELLED_REASON
_PP.fields_by_name['side'].enum_type = _SIDE
_MESSAGE_PAYLOAD.fields_by_name['replay'].message_type = _REPLAY_PAYLOAD
_MESSAGE_PAYLOAD.fields_by_name['login'].message_type = _LOGIN_PAYLOAD
_MESSAGE_PAYLOAD.fields_by_name['login_response'].message_type = _LOGIN_RESPONSE_PAYLOAD
_MESSAGE_PAYLOAD.fields_by_name['order'].message_type = _ORDER_PAYLOAD
_MESSAGE_PAYLOAD.fields_by_name['order_rejected'].message_type = _ORDER_REJECTED_PAYLOAD
_MESSAGE_PAYLOAD.fields_by_name['order_accepted'].message_type = _ORDER_ACCEPTED_PAYLOAD
_MESSAGE_PAYLOAD.fields_by_name['order_executed'].message_type = _ORDER_EXECUTED_PAYLOAD
_MESSAGE_PAYLOAD.fields_by_name['order_cancel'].message_type = _ORDER_CANCEL_PAYLOAD
_MESSAGE_PAYLOAD.fields_by_name['order_cancelled'].message_type = _ORDER_CANCELLED_PAYLOAD

class message(gmessage.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _MESSAGE

class replay_payload(gmessage.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _REPLAY_PAYLOAD

class login_response_payload(gmessage.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _LOGIN_RESPONSE_PAYLOAD

class range_payload(gmessage.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _RANGE_PAYLOAD

class order_payload(gmessage.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _ORDER_PAYLOAD

class order_accepted_payload(gmessage.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _ORDER_ACCEPTED_PAYLOAD

class order_rejected_payload(gmessage.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _ORDER_REJECTED_PAYLOAD

class order_executed_payload(gmessage.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _ORDER_EXECUTED_PAYLOAD

class order_cancel_payload(gmessage.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _ORDER_CANCEL_PAYLOAD

class order_cancelled_payload(gmessage.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _ORDER_CANCELLED_PAYLOAD

class pp(gmessage.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _PP

class login_payload(gmessage.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _LOGIN_PAYLOAD

class message_payload(gmessage.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _MESSAGE_PAYLOAD

