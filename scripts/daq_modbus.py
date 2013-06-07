#!/usr/bin/env python

import time
import struct

from pymodbus.client.sync import ModbusTcpClient as _ModbusTcpClient
from pymodbus.client.sync import ModbusSerialClient as _ModbusSerialClient
from pymodbus.pdu import ExceptionResponse
from pymodbus.exceptions import ConnectionException

from daq.config import cfg
from daq.services.query_engine.client_base import ClientBase
from daq.services.query_engine.query import Query, QueryError

class ModbusClient(ClientBase):

    MINIMUM_QUERY_GAP = 2

    FUNCTION_CODES = {
        3: 'read_holding_registers',
        4: 'read_input_registers'
    }

    @classmethod
    def query_factory(cls, variables):
        queries = []

        for var in sorted(variables, key=lambda v: (v.interval,
                                                    v.interface['address'],
                                                    v.function_code,
                                                    v.registers[0])):
            address = var.interface['address']
            start, end = var.registers

            if len(queries) == 0 or queries[-1].interval != var.interval \
            or queries[-1].address != address \
            or queries[-1].function_code != var.function_code \
            or start - (queries[-1].end + 1) > cls.MINIMUM_QUERY_GAP:

                queries.append(Query(interval=var.interval,
                                     address=address,
                                     function_code=var.function_code,
                                     start=start,
                                     end=end))

            if not hasattr(var, 'byte_order'):
                var.update(byte_order='abcd')

            queries[-1].add_variable(var)
            queries[-1].end = end

        return queries

    def make_query(self, query):
        try:
            resp = self._query_registers(query)
        except ConnectionException as e:
            raise QueryError(e)
        except:
            raise QueryError

        if resp is None or isinstance(resp, ExceptionResponse):
            raise QueryError(resp)

        return resp.registers

    def parser(self, var, regs, query):
        start, end = var.registers
        regs = regs[(start - query.start):(end - query.start + 1)]

        regs = self._order_bytes(var.byte_order, regs)

        formatter = "_format_%s" % var.format_type

        try:
            return getattr(self, formatter)(regs)
        except:
            return None

    def _query_registers(self, query):
        func = getattr(self.client, self.FUNCTION_CODES.get(query.function_code))
        start = query.start
        count = query.end - start + 1

        return func(start, count, unit=query.address)

    def _order_bytes(self, order, regs):
        if order in ('abcd', 'badc'):
            regs.reverse()

        if order in ('badc', 'dcba', 'ba'):
            func = lambda r: struct.unpack('>H', struct.pack('<H', r))[0]
            regs = map(func, regs)

        return regs

    def _format_uint16(self, regs):
        return regs[0]

    def _format_sint16(self, regs):
        return struct.unpack('h', struct.pack('H', *regs))[0]

    def _format_uint32(self, regs):
        return struct.unpack('I', struct.pack('HH', *regs))[0]

    def _format_sint32(self, regs):
        return struct.unpack('i', struct.pack('HH', *regs))[0]

    def _format_float(self, regs):
        return struct.unpack('f', struct.pack('HH', *regs))[0]

    def _format_ascii(self, regs):
        return struct.pack('h' * len(regs), *regs).strip()[::-1]


class ModbusTcpClient(ModbusClient):

    def __init__(self, **kwargs):
        self.host = kwargs.get('host', 'localhost')
        self.port = kwargs.get('port', 502)

        self.sig = 'modbus:tcp:%s:%s' % (self.host, self.port)
        self._client = None

    @property
    def client(self):
        if self._client is None:
            self._client = _ModbusTcpClient(host=self.host, port=self.port)

        return self._client

    def close(self):
        if self._client is not None:
            self._client.close()


class ModbusRtuClient(ModbusClient):

    def __init__(self, **kwargs):
        self.port = cfg.COMM_PORTS.get(kwargs.get('comm_port', 1))
        self.baudrate = kwargs.get('baudrate', 9600)
        self.timeout = kwargs.get('timeout', 1)

        self.sig = 'modbus:rtu:%s' % self.port
        self._client = None

    @property
    def client(self):
        if self._client is None:
            self._client = _ModbusSerialClient(method='rtu', port=self.port,
                baudrate=self.baudrate, timeout=self.timeout)

        return self._client

    def close(self):
        if self._client is not None:
            self._client.close()


def client_factory(**kwargs):
    protocol = kwargs.get('protocol')

    if protocol == 'tcp':
        return ModbusTcpClient(**kwargs)

    elif protocol == 'rtu':
        return ModbusRtuClient(**kwargs)

    return None
