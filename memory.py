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
    address = 2
    value = -1
    mem.set_value(address, value, size=1)
    print mem.get_value(address, signed=True, size=1)
    print mem.get_value(address, signed=True, size=2)
    print map(hex, list(mem.bank[:8]))
    print hex(mem.get_value(address-2, size=4))
    # we can output using the xxd way!!!
    mem.bank[:4] = [0x12, 0x34, 0x56, 0x78]
    print map(hex, list(mem.bank[:8]))
    mem.bank[:4] = [0xff, 0xfe, 0xfd, 1]
    print mem.get_value(address, signed=True, size=1)
    print mem.get_value(address, signed=True, size=2)
