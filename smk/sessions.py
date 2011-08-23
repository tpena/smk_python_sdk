"Smarkets TCP-based session management"
import logging
import Queue
import socket

from google.protobuf import text_format

import eto.piqi_pb2 as eto
import seto.piqi_pb2 as seto

from smk.exceptions import ConnectionError, SocketDisconnected


class Session(object):
    "Manages TCP communication via Smarkets streaming API"
    logger = logging.getLogger('smk.session')

    def __init__(self, username, password, host='localhost', port=3701,
                 session=None, inseq=1, outseq=1, socket_timeout=30):
        self.username = username
        self.password = password
        self.socket = SessionSocket(host, port, socket_timeout)
        self.session = session
        self.inseq = inseq
        # Outgoing socket sequence number
        self.outseq = outseq
        # Outgoing buffer sequence number
        self.buf_outseq = outseq
        self.in_payload = seto.Payload()
        self.out_payload = seto.Payload()
        self.send_buffer = Queue.Queue()

    @property
    def connected(self):
        "Returns True if the socket is currently connected"
        return self.socket.connected

    def connect(self):
        "Connects to the API and logs in if not already connected"
        if self.socket.connect():
            # Clear the outgoing send buffer
            self.send_buffer = Queue.Queue()
            # Reset separate outgoing buffer sequence number
            self.buf_outseq = self.outseq
            login = self.out_payload
            login.Clear()
            # pylint: disable-msg=E1101
            login.type = seto.PAYLOAD_LOGIN
            login.eto_payload.type = eto.PAYLOAD_LOGIN
            login.login.username = self.username
            login.login.password = self.password
            self.logger.info("sending login payload")
            if self.session is not None:
                self.logger.info(
                    "attempting to resume session %s", self.session)
                login.eto_payload.login.session = self.session
            # Always flush outgoing login message
            self.send(True)

    def disconnect(self):
        "Disconnects from the API"
        self.socket.disconnect()

    def send(self, flush=False):
        "Serialise, sequence, add header, and send payload"
        self.logger.debug(
            "buffering payload with outgoing sequence %d: %s",
            self.outseq, text_format.MessageToString(self.out_payload))
        # pylint: disable-msg=E1101
        self.out_payload.eto_payload.seq = self.buf_outseq
        self.send_buffer.put_nowait(self.out_payload.SerializeToString())
        self.buf_outseq += 1
        if flush:
            self.flush()

    def flush(self):
        "Flush payloads to the socket"
        self.logger.debug("flushing %d payloads", self.send_buffer.qsize())
        while not self.send_buffer.empty():
            try:
                msg_bytes = self.send_buffer.get_nowait()
                self.socket.send(msg_bytes)
                self.outseq += 1
            except Queue.Empty:
                break

    def next_frame(self):
        "Get the next frame and increment inseq"
        msg_bytes = self.socket.recv()
        self.in_payload.Clear()
        self.in_payload.ParseFromString(msg_bytes)
        self._handle_in_payload()
        # pylint: disable-msg=E1101
        if self.in_payload.eto_payload.seq == self.inseq:
            # Go ahead
            self.logger.debug("received sequence %d", self.inseq)
            self.inseq += 1
            return self.in_payload
        elif self.in_payload.eto_payload.type == eto.PAYLOAD_REPLAY:
            # Just a replay message, sequence not important
            seq = self.in_payload.eto_payload.replay.seq
            self.logger.debug(
                "received a replay message with sequence %d", seq)
            return None
        elif self.in_payload.eto_payload.seq > self.inseq:
            # Need a replay
            self.logger.info(
                "received incoming sequence %d, expected %d, need replay",
                self.in_payload.eto_payload.seq,
                self.inseq)
            replay = self.out_payload
            replay.Clear()
            # pylint: disable-msg=E1101
            replay.type = seto.PAYLOAD_ETO
            replay.eto_payload.type = eto.PAYLOAD_REPLAY
            replay.eto_payload.replay.seq = self.inseq
            # Do not auto-flush replay because we may be in another
            # thread
            self.send()
            return None
        else:
            return None

    def _handle_in_payload(self):
        "Pre-consume the login response message"
        # pylint: disable-msg=E1101
        msg = self.in_payload
        self.logger.debug(
            "received message to dispatch: %s",
            text_format.MessageToString(msg))
        if msg.eto_payload.type == eto.PAYLOAD_LOGIN_RESPONSE:
            self.session = msg.eto_payload.login_response.session
            self.outseq = msg.eto_payload.login_response.reset
            self.buf_outseq = self.outseq
            self.send_buffer = Queue.Queue()
            self.logger.info(
                "received login_response with session %s and reset %d",
                self.session,
                self.outseq)
        elif msg.eto_payload.type == eto.PAYLOAD_HEARTBEAT:
            self.logger.debug("received heartbeat message, responding...")
            heartbeat = self.out_payload
            heartbeat.Clear()
            heartbeat.type = seto.PAYLOAD_ETO
            heartbeat.eto_payload.type = eto.PAYLOAD_HEARTBEAT
            # Do not immediately flush heartbeat response because we
            # may be in another thread
            self.send()
        return msg


class SessionSocket(object):
    "Wraps a socket with basic framing/deframing"
    logger = logging.getLogger('smk.session.socket')
    wire_logger = logging.getLogger('smk.session.wire')
    # Most message are quite small, so this won't come into
    # effect. For larger messages, it needs some performance testing
    # to determine whether a single large recv() system call is worse
    # than many smaller ones.
    default_read_chunksize = 65536 # 64k

    def __init__(self, host, port, socket_timeout=None, read_chunksize=None):
        self.host = host
        self.port = port
        self.socket_timeout = socket_timeout
        if read_chunksize is None:
            read_chunksize = self.default_read_chunksize
        self.read_chunksize = read_chunksize
        self._buffer = ''
        self._sock = None

    @property
    def connected(self):
        "Returns True if the socket is currently connected"
        return self._sock is not None

    def connect(self):
        """
        Create a TCP socket connection.

        Returns True if the socket needed connecting, False if not
        """
        if self._sock is not None:
            self.logger.debug("connect() called, but already connected")
            return False
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if self.socket_timeout is not None:
                sock.settimeout(self.socket_timeout)
            self.logger.info(
                "connecting with new socket to %s:%s", self.host, self.port)
            sock.connect((self.host, self.port))
        except socket.error as exc:
            raise ConnectionError(self._error_message(exc))

        self._sock = sock
        return True

    def disconnect(self):
        "Close the TCP socket."
        if self._sock is None:
            self.logger.debug("disconnect() called with no socket, ignoring")
            return
        try:
            self.logger.info("shutting down reads")
            self._sock.shutdown(socket.SHUT_RD)
            self.logger.info("shutting down reads/writes")
            self._sock.shutdown(socket.SHUT_RDWR)
            self.logger.info("closing socket")
            self._sock.close()
        except socket.error:
            # Ignore exceptions while disconnecting
            pass
        self._sock = None

    def send(self, msg_bytes):
        "Send a payload"
        if self._sock is None:
            raise SocketDisconnected()
        byte_count = len(msg_bytes)
        # Pad to 4 bytes
        padding = '\x00' * max(0, 3 - byte_count)
        self.logger.debug(
            "payload has %d bytes and needs %d padding",
            byte_count, len(padding))
        frame = _encode_varint(byte_count) + msg_bytes + padding
        try:
            self.wire_logger.debug("sending frame bytes %r", frame)
            self._sock.sendall(frame)
        except socket.error as exc:
            if len(exc.args) == 1:
                _errno, errmsg = 'UNKNOWN', exc.args[0]
            else:
                _errno, errmsg = exc.args
            raise ConnectionError("Error %s while writing to socket. %s." % (
                    _errno, errmsg))

    def recv(self):
        "Read a frame with header"
        # Read a minimum of 4 bytes
        self._fill_buffer()
        result = 0
        shift = 0
        pos = 0
        while 1:
            if pos > len(self._buffer) - 1:
                pos = 0
                # Empty buffer and read another 4 bytes
                self._fill_buffer(4, socket.MSG_WAITALL)
            cbit = ord(self._buffer[pos])
            result |= ((cbit & 0x7f) << shift)
            pos += 1
            if not (cbit & 0x80):
                self._buffer = self._buffer[pos:]
                to_read = max(0, result - len(self._buffer))
                self.logger.debug("next message is %d bytes long", to_read)
                if to_read:
                    # Read the actual message if necessary
                    while to_read > self.read_chunksize:
                        self._fill_buffer(
                            self.read_chunksize + len(self._buffer))
                        to_read -= self.read_chunksize
                    if to_read > 0:
                        self._fill_buffer(to_read + len(self._buffer))
                msg_bytes = self._buffer[:result]
                self.wire_logger.debug("received bytes %r", msg_bytes)
                # Consume the buffer
                self._buffer = self._buffer[result:]
                return msg_bytes
            shift += 7

    def _fill_buffer(self, min_size=4, empty=False):
        "Ensure the buffer has at least 4 bytes"
        if self._sock is None:
            raise SocketDisconnected()
        if empty:
            self._buffer = ''
        while len(self._buffer) < min_size:
            bytes_needed = min_size - len(self._buffer)
            self.logger.debug("receiving %d bytes", bytes_needed)
            inbytes = self._sock.recv(bytes_needed, socket.MSG_WAITALL)
            if len(inbytes) != bytes_needed:
                self.logger.info(
                    "socket disconnected while receiving, got %r", inbytes)
                raise SocketDisconnected()
            self._buffer += inbytes

    def _error_message(self, exception):
        "Stringify a socket exception"
        # args for socket.error can either be (errno, "message")
        # or just "message"
        if len(exception.args) == 1:
            return "Error connecting to %s:%s. %s." % (
                self.host, self.port, exception.args[0])
        else:
            return "Error %s connecting %s:%s. %s." % (
                exception.args[0], self.host, self.port,
                exception.args[1])


def _encode_varint(value):
    """
    Encode an int/long as a ULEB128 number
    """
    bits = value & 0x7f
    value >>= 7
    ret = ''
    while value:
        ret += chr(0x80 | bits)
        bits = value & 0x7f
        value >>= 7
    return ret + chr(bits)