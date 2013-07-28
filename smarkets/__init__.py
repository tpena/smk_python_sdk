"Smarkets API package"
# Copyright (C) 2011 Smarkets Limited <support@smarkets.com>
#
# This module is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php
import inspect
import os

if 'READTHEDOCS' in os.environ:
    from mock import Mock
    import sys

    eto = seto = \
        sys.modules['smarkets.eto'] = sys.modules['smarkets.eto.piqi_pb2'] = \
        sys.modules['smarkets.seto'] = sys.modules['smarkets.seto.piqi_pb2'] = Mock()

from smarkets.clients import Smarkets
from smarkets.events import (
    EventsRequest,
    Politics,
    CurrentAffairs,
    TvAndEntertainment,
    SportByDate,
    FootballByDate,
    HorseRacingByDate,
    TennisByDate,
    BasketballByDate,
    AmericanFootballByDate,
    BaseballByDate,
    CricketByDate,
    HandballByDate,
    RugbyByDate,
    RugbyLeagueByDate,
    VolleyballByDate,
    SportOther,
)
from smarkets.exceptions import (
    Error,
    ConnectionError,
    DecodeError,
    ParseError,
    SocketDisconnected,
    InvalidCallbackError,
    )
from smarkets.orders import Order, FillOrKillOrder
from smarkets.orders import OrderCreate

from smarkets.sessions import Session, SessionSettings


__version__ = '0.4.8'

__all__ = sorted(name for name, obj in locals().items()
                 if not (name.startswith('_') or inspect.ismodule(obj)))

VERSION = tuple((int(x) for x in __version__.split('.')))
