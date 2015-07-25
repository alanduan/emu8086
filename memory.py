import ctypes
import struct

class Memory:

    def __init__(self):
        self.bank = bytearray(2**20)
        #self.memory = ctypes.create_string_buffer(2**20)

    def set_value(self, address, value, size=1):
        if value < 0:
            fmts = [None, '<b', '<h', None, '<i', None, None, None, '<q']
        else:
            fmts = [None, '<B', '<H', None, '<I', None, None, None, '<Q']
        fmt = fmts[size]
        if fmt:
            struct.pack_into(fmt, self.bank, address, value)
        else:
            raise ValueError('Invalid data size: %d bytes' % size)

    def get_value(self, address, signed=False, size=1):
        if signed:
            fmts = [None, '<b', '<h', None, '<i', None, None, None, '<q']
        else:
            fmts = [None, '<B', '<H', None, '<I', None, None, None, '<Q']
        fmt = fmts[size]
        if fmt:
            return struct.unpack_from(fmt, self.bank, address)[0]
        else:
            raise ValueError('Invalid data size: %d bytes' % size)

if __name__ == '__main__':
    mem = Memory()
