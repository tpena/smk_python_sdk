"Smarkets API package"
# Copyright (C) 2011 Smarkets Limited support@smarkets.com
#
# This module is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php
import inspect

from smk.clients import Smarkets
from smk.events import (
    EventsRequest,
    Politics,
    CurrentAffairs,
    TvAndEntertainment,
    SportByDate,
    FootballByDate,
    HorseRacingByDate,
    TennisByDate,
    SportOther,
    )
from smk.exceptions import (
    Error,
    ConnectionError,
    DecodeError,
    ParseError,
    SocketDisconnected,
    InvalidCallbackError,
    )
from smk.sessions import Session


__version__ = '0.1.0'

__all__ = sorted(name for name, obj in locals().items()
                 if not (name.startswith('_') or inspect.ismodule(obj)))

VERSION = tuple((int(x) for x in __version__.split('.')))
