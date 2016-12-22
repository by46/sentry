import struct
import six

from .exception import InvalidZabbixDataException
from .exception import InvalidZabbixHeaderException
from .utils import hex_representation

ZBX_HEADER = b'ZBXD'
ZBX_VERSION = 1
ZBX_HEADER_FMT = '<4sBq'

MAX_BUFFER = 1024 * 32

StringIO = six.moves.cStringIO


def receive_data(socket, buffer_size=MAX_BUFFER):
    header_size = struct.calcsize(ZBX_HEADER_FMT)
    buf = socket.recv(header_size)
    if len(buf) < header_size:
        msg = hex_representation(buf)
        raise InvalidZabbixHeaderException(msg)
    zbx_header, zbx_version, data_length = struct.unpack(ZBX_HEADER_FMT, buf)
    assert zbx_header == ZBX_HEADER
    assert zbx_version == ZBX_VERSION
    if data_length < 0:
        raise InvalidZabbixDataException(0, data_length)

    buf = StringIO()
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

    data = buf.getvalue()
    return data


def send_data(data):
    json_byte = len(data)
    header = struct.pack(ZBX_HEADER_FMT, ZBX_HEADER, ZBX_VERSION, json_byte)
    return header + data.encode('utf-8')
