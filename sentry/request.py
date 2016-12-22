import json
import struct

import six
from werkzeug.utils import cached_property

from .exception import InvalidZabbixDataException
from .exception import InvalidZabbixHeaderException
from .utils import hex_representation

BytesIO = six.BytesIO


class Request(object):
    protocol_header = b'ZBXD'
    protocol_version = 1
    max_buffer = 1024 * 32

    def __init__(self, socket, address):
        self.socket = socket
        self.address = address
        self.header = None
        self.version = None
        self.payload = self.process_payload(self.process())

    @cached_property
    def header_fmt(self):
        return self.make_header_fmt()

    def make_header_fmt(self):
        return '<4sBq'

    def process(self):
        socket = self.socket
        header_fmt = self.header_fmt
        buffer_size = self.max_buffer
        header_size = struct.calcsize(header_fmt)
        buf = socket.recv(header_size)
        if len(buf) < header_size:
            msg = hex_representation(buf)
            raise InvalidZabbixHeaderException(msg)
        header, version, data_length = struct.unpack(header_fmt, buf)
        assert header == self.protocol_header
        assert version == self.protocol_version
        self.header = header
        self.version = version
        if data_length < 0:
            raise InvalidZabbixDataException(0, data_length)

        buf = BytesIO()
        receive_size = 0
        while True:
            data = socket.recv(buffer_size)
            if len(data) <= 0:
                break

            buf.write(data)
            receive_size += len(data)
            if receive_size == data_length:
                break
            elif receive_size > data_length:
                raise InvalidZabbixDataException(data_length, receive_size)
        return buf.getvalue().decode('utf-8')

    @staticmethod
    def process_payload(data):
        return json.loads(data)

    def __repr__(self):
        return repr(self.payload)
