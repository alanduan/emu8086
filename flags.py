#===========================================================================
# FLAGS
#===========================================================================
flag_position = {
    'of':11,
    'df':10,
    'if':9,
    'tf':8,
    'sf':7,
    'zf':6,
    'af':4,
    'pf':2,
    'cf':0}
flag_names = flag_position.keys()

class Flags:
    def __init__(self):
        self.__dict__['_internals'] = dict(map(lambda x: (x, 0), flag_names))
        self._internals['value'] = 2

    def __getattr__(self, name):
        name = name.lower()
        if name in ['_internals']:
            return self.__dict__[name]
        if name == 'value':
            return self._internals['value']
        if name in flag_names:
            return (self.value >> flag_position[name]) & 1
        raise AttributeError('%r has no attribute %r' % (
            self.__class__.__name__, name))

    def __setattr__(self, name, value):
        name = name.lower()
        if name == 'value':
            self._internals['value'] = (value & 0b111111010111) | 0b10
        elif name in flag_names:
            if value & 1 != 0:
                self.value |= (1 << flag_position[name])
            else:
                self.value &= ~(1 << flag_position[name])
        else:
            raise AttributeError('%r rejects attribute %r' % (
                self.__class__.__name__, name))

    def __str__(self):
        return '%(of)s %(df)s %(if)s %(sf)s %(zf)s %(af)s %(pf)s %(cf)s' % {
            'of': 'OV' if self.OF else 'NV',
            'df': 'DN' if self.DF else 'UP',
            'if': 'EI' if self.IF else 'DI',
            'tf': '' if self.TF else '',
            'sf': 'NG' if self.SF else 'PL',
            'zf': 'ZR' if self.ZF else 'NZ',
            'af': 'AC' if self.AF else 'NA',
            'pf': 'PE' if self.PF else 'PO',
            'cf': 'CY' if self.CF else 'NC'}


if __name__ == '__main__':
    flags = Flags()
    print(flags)
