from flags import Flags

#===========================================================================
# CPU
#===========================================================================
output_format = '''\
AX=%(ax)04X  BX=%(bx)04X  CX=%(cx)04X  DX=%(dx)04X  SP=%(sp)04X  BP=%(bp)04X  SI=%(si)04X  DI=%(di)04X
DS=%(ds)04X  ES=%(es)04X  SS=%(ss)04X  CS=%(cs)04X  IP=%(ip)04X   %(flags)s
%(cs)04X:%(ip)04X'''

class CPU:
    '''8086 cpu emulator'''
    def __init__(self):
        self.__dict__['_internals'] = dict(
            ax = 0, cx = 0, dx = 0, bx = 0, sp = 0, bp = 0, si = 0, di = 0,
            cs = 0, ds = 0, ss = 0, es = 0, ip = 0,
            flags = Flags())

    def __str__(self):
        return output_format % self._internals

    def __getattr__(self, name):
        name = name.lower()
        if name == '_internals':
            return self.__dict__[name]
        if name in ['ah', 'bh','ch','dh']:
            # assume the internal values are always set properly as unsigned
            return (self._internals[name[0]+'x'] >> 8) & 0xff
        if name in ['al', 'bl','cl','dl']:
            return self._internals[name[0]+'x'] & 0xff
        if name in [
            'ax', 'cx', 'dx', 'bx', 'sp', 'bp', 'si', 'di',
            'es', 'cs', 'ss', 'ds', 'ip']:
            return self._internals[name]
        if name == 'flags':
            return self._internals[name].value
        if name in ['of', 'df', 'if', 'tf', 'sf', 'zf', 'af', 'pf', 'cf']:
            return getattr(self._internals['flags'], name)
        raise AttributeError('%r has no attribute %r' % (
            self.__class__.__name__, name))

    def __setattr__(self, name, value):
        name = name.lower()
        if name in [
            'ax', 'cx', 'dx', 'bx', 'sp', 'bp', 'si', 'di',
            'es', 'cs', 'ss', 'ds', 'ip'
            ]:
            self._internals[name] = value & 0xffff
        elif name in ['al', 'cl', 'dl', 'bl']:
            v = self._internals[name[0]+'x']
            self._internals[name[0]+'x'] = (v & 0xff00) | (value & 0xff)
        elif name in ['ah', 'ch', 'dh', 'bh']:
            v = self._internals[name[0]+'x']
            self._internals[name[0]+'x'] = (v & 0x00ff) | ((value & 0xff) << 8)
        elif name == 'flags':
            self._internals[name].value = (0b111111010111 & value) | 0b10
        elif name in ['of', 'df', 'if', 'tf', 'sf', 'zf', 'af', 'pf', 'cf']:
            setattr(self._internals['flags'], name, value & 1)
        else:
            raise AttributeError('%r rejects attribute %r' % (
                self.__class__.__name__, name))

if __name__ == '__main__':
    cpu = CPU()
    print(cpu)
    cpu.ax = -1
    cpu.bl = 0xffff
    cpu.flags = 0xff
    print(cpu.OF)
    print(cpu)

