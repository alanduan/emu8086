'''
This instruction set is implemented according to:
    Intel 8086 datasheet
'''

class Foo:

    def __init__(self):
        self.instruction_bytes = []

    def fetch_opcode(self):
        self.instruction_bytes = []
        opcode = self.next_data()
        if opcodes[opcode]:
            instruction_bytes.append(opcode)
        else:
            raise Exception('unsupported opcode')
        
        
def parse_modrm(self):
    byte = self.next_data()
    mod = byte & 0b11000000 >> 6
    reg_opcode = byte & 0b00111000 >> 3
    rm = byte & 0b00000111
    base = 0
    index = 0
    disp = 0
    if mod in [0b00, 0b01, 0b10]:
        if mod == 0b01: disp = self.next_data()
        elif mod == 0b10: disp = self.next_data(size=2)
        if rm == 0b000:
            base = self.cpu.bx
            index = self.cpu.si
        elif rm == 0b001:
            base = self.cpu.bx
            index = self.cpu.di
        elif rm == 0b010:
            base = self.cpu.bp
            index = self.cpu.si
        elif rm == 0b011:
            base = self.cpu.bp
            index = self.cpu.di
        elif rm == 0b100:
            index = self.cpu.si
        elif rm == 0b101:
            index = self.cpu.di
        elif rm == 0b110:
            if mod == 0b00:
                disp = self.next_data(size=2)
            else:
                # mod in [0b01, 0b10]
                base = self.cpu.bp
        elif rm == 0b111:
            base = self.cpu.bx
    else:
        # mod == 0b11
        if self.w:
            reg = [
                self.cpu.ax, self.cpu.cx, self.cpu.dx, self.cpu.bx,
                self.cpu.sp, self.cpu.bp, self.cpu.si, self.cpu.di][rm]
        else:
            # self.w = 0
            reg = [
                self.cpu.al, self.cpu.cl, self.cpu.dl, self.cpu.bl,
                self.cpu.ah, self.cpu.ch, self.cpu.dh, self.cpu.bh][rm]

                

def handle_00():
    modrm_byte = self.next_data()
    mod, reg_opcode, rm = self.parse_modrm(modrm_byte)

opcodes = {
    0x00: lambda: (self.prase_ea() and self.parse_handle_00,#('add byte EA, byte REG'),
    0x01: ('add word EA, word REG'),
    0x02: ('add byte REG, byte EA'),
    0x03: ('add word REG, word EA'),
    0x04: ('add al, 8bit imm'),
    0x05: ('add ax, 16bit imm'),
    0x06: ('push es'),
    0x07: ('pop es'),
    0x08: ('or byte EA, byte REG'),
    0x09: ('or word EA, word REG'),
    0x0a: ('or byte REG, byte EA'),
    0x0b: ('or word REG, word EA'),
    0x0c: ('or al, 8bit imm'),
    0x0d: ('or ax, 16bit imm'),
    0x0e: ('push cs'),
    0x0f: ('pop cs'),
    0x10: ('adc byte ea, reg'),
    0x11: ('adc word ea, reg'),
    0x12: ('adc reg, byte ea'),
    0x13: ('adc reg, word ea'),
    0x14: ('adc'),
    0x15: ('adc'),
    0x16: ('push ss'),
    0x17: ('pop ss'),
    0x18: ('ssb byte EA, byte REG'),
    0x19: ('ssb word EA, word REG'),
    0x1a: ('ssb byte REG, byte EA'),
    0x1b: ('ssb word REG, word EA'),
    0x1c: ('ssb al, 8bit imm'),
    0x1d: ('ssb ax, 16bit imm'),
    0x1e: ('push ds'),
    0x1f: ('pop ds'),
    0x20: ('and byte EA, byte REG'),
    0x21: ('and word EA, word REG'),
    0x22: ('and byte REG, byte EA'),
    0x23: ('and word REG, word EA'),
    0x24: ('and al, 8bit imm'),
    0x25: ('and ax, 16bit imm'),
    0x26: (),
    0x27: ('baa'),
    0x28: ('sub byte EA, byte REG'),
    0x29: ('sub word EA, word REG'),
    0x2a: ('sub byte REG, byte EA'),
    0x2b: ('sub word REG, word EA'),
    0x2c: ('sub al, 8bit imm'),
    0x2d: ('sub ax, 16bit imm'),
    0x2e: (),
    0x2f: ('das'),
    0x30: ('xor byte EA, byte REG'),
    0x31: ('xor word EA, word REG'),
    0x32: ('xor byte REG, byte EA'),
    0x33: ('xor word REG, word EA'),
    0x34: ('xor al, 8bit imm'),
    0x35: ('xor ax, 16bit imm'),
    0x36: (),
    0x37: ('aaa'),
    0x38: ('cmp byte EA, byte REG'),
    0x39: ('cmp word EA, word REG'),
    0x3a: ('cmp byte REG, byte EA'),
    0x3b: ('cmp word REG, word EA'),
    0x3c: ('cmp al, 8bit imm'),
    0x3d: ('cmp ax, 16bit imm'),
    0x3e: (),
    0x3f: ('aas'),
    0x40: ('inc ax'),
    0x41: ('inc cx'),
    0x42: ('inc dx'),
    0x43: ('inc bx'),
    0x44: ('inc sp'),
    0x45: ('inc bp'),
    0x46: ('inc si'),
    0x47: ('inc di'),
    0x48: ('dec ax'),
    0x49: ('dec cx'),
    0x4a: ('dec dx'),
    0x4b: ('dec bx'),
    0x4c: ('dec sp'),
    0x4d: ('dec bp'),
    0x4e: ('dec si'),
    0x4f: ('dec di'),
    0x50: ('push ax'),
    0x51: ('push cx'),
    0x52: ('push dx'),
    0x53: ('push bx'),
    0x54: ('push sp'),
    0x55: ('push bp'),
    0x56: ('push si'),
    0x57: ('push di'),
    0x58: ('pop ax'),
    0x59: ('pop cx'),
    0x5a: ('pop dx'),
    0x5b: ('pop bx'),
    0x5c: ('pop sp'),
    0x5d: ('pop bp'),
    0x5e: ('pop si'),
    0x5f: ('pop di'),
    0x60: (),
    0x61: (),
    0x62: (),
    0x63: (),
    0x64: (),
    0x65: (),
    0x66: (),
    0x67: (),
    0x68: (),
    0x69: (),
    0x6a: (),
    0x6b: (),
    0x6c: (),
    0x6d: (),
    0x6e: (),
    0x6f: (),
    0x70: ('jo'),
    0x71: ('jno'),
    0x72: ('jb/jnae'),
    0x73: ('jnb/jae'),
    0x74: ('je/jz'),
    0x75: ('jne/jnz'),
    0x76: ('jbe/jna'),
    0x77: ('jnbe/ja'),
    0x78: ('js'),
    0x79: ('jns'),
    0x7a: ('jp/jpe'),
    0x7b: ('jnp/jpo'),
    0x7c: ('jl/jnge'),
    0x7d: ('jnl/jge'),
    0x7e: ('jle/jng'),
    0x7f: ('jnle/jg'),
    0x80: ('add byte EA, 8bits imm', 'adc', 'sub', 'ssb', 'and', 'or', 'xor'),
    0x81: ('add word EA, 16bits imm', 'adc', 'sub', 'ssb', 'and', 'or', 'xor'),
    0x82: ('add byte EA, 8bits imm', 'adc', 'sub', 'ssb'),
    0x83: ('add word EA, 8bits sign extended imm', 'adc', 'sub', 'ssb'),
    0x84: ('test ea, reg'),
    0x85: ('test reg, ea'),
    0x86: ('xchg byte EA, reg'),
    0x87: ('xchg word EA, reg'),
    0x88: ('mov byte EA, reg'),
    0x89: ('mov word EA, reg'),
    0x8a: ('mov reg, byte EA'),
    0x8b: ('mov reg, word EA'),
    0x8c: ('mov word EA, seg'),
    0x8d: ('lea reg, EA'),
    0x8e: ('mov seg, word EA'),
    0x8f: ('pop word EA'),
    0x90: ('xchg AX, ax'),
    0x91: ('xchg AX, cx'),
    0x92: ('xchg AX, dx'),
    0x93: ('xchg AX, bx'),
    0x94: ('xchg AX, sp'),
    0x95: ('xchg AX, bp'),
    0x96: ('xchg AX, si'),
    0x97: ('xchg AX, di'),
    0x98: ('cbw'),
    0x99: ('cwd'),
    0x9a: ('call seg:offset'),
    0x9b: ('wait'),
    0x9c: ('pushf'),
    0x9d: ('popf'),
    0x9e: ('sahf'),
    0x9f: ('lahf'),
    0xa0: ('mov al, [16bits address]'),
    0xa1: ('mov ah, [16bits address]'),
    0xa2: ('mov [16bits address], al'),
    0xa3: ('mov [16bits address], ah'),
    0xa4: ('movs'),
    0xa5: ('movs'),
    0xa6: ('cmps'),
    0xa7: ('cmps'),
    0xa8: ('test al, imm'),
    0xa9: ('test ax, imm16'),
    0xaa: ('stos'),
    0xab: ('stos'),
    0xac: ('lods'),
    0xad: ('lods'),
    0xae: ('scas'),
    0xaf: ('scas'),
    0xb0: ('mov al, imm8'),
    0xb1: ('mov cl, imm8'),
    0xb2: ('mov dl, imm8'),
    0xb3: ('mov bl, imm8'),
    0xb4: ('mov ah, imm8'),
    0xb5: ('mov ch, imm8'),
    0xb6: ('mov dh, imm8'),
    0xb7: ('mov bh, imm8'),
    0xb8: ('mov ax, imm16'),
    0xb9: ('mov cx, imm16'),
    0xba: ('mov dx, imm16'),
    0xbb: ('mov bx, imm16'),
    0xbc: ('mov sp, imm16'),
    0xbd: ('mov bp, imm16'),
    0xbe: ('mov si, imm16'),
    0xbf: ('mov di, imm16'),
    0xc0: (),
    0xc1: (),
    0xc2: ('ret n'),
    0xc3: ('ret'),
    0xc4: ('les reg, EA'),
    0xc5: ('lds reg, EA'),
    0xc6: ('mov byte EA, byte imm'),
    0xc7: ('mov word EA, word imm'),
    0xc8: (),
    0xc9: (),
    0xca: ('retf n'),
    0xcb: ('retf'),
    0xcc: ('int3'),
    0xcd: ('int n'),
    0xce: ('into'),
    0xcf: ('iret'),
    0xd0: ('shl/sal/shr/sar/rol/ror/rcl/rcr byte ea, 1'),
    0xd1: ('shl/sal/shr/sar/rol/ror/rcl/rcr word ea, 1'),
    0xd2: ('shl/sal/shr/sar/rol/ror/rcl/rcr byte ea, cl'),
    0xd3: ('shl/sal/shr/sar/rol/ror/rcl/rcr word ea, cl'),
    0xd4: ('aam'),
    0xd5: ('aad'),
    0xd6: (),
    0xd7: ('xlatb'),
    0xd8: ('esc'),
    0xd9: ('esc'),
    0xda: ('esc'),
    0xdb: ('esc'),
    0xdc: ('esc'),
    0xdd: ('esc'),
    0xde: ('esc'),
    0xdf: ('esc'),
    0xe0: ('loopnz/loopne'),
    0xe1: ('loopz/loope'),
    0xe2: ('loop'),
    0xe3: ('jcxz'),
    0xe4: ('in al, port'),
    0xe5: ('in ax, port'),
    0xe6: ('out port, al'),
    0xe7: ('out port, ax'),
    0xe8: ('call disp16'),
    0xe9: ('jmp direct within segment'),
    0xea: ('jmp direct intersegment'),
    0xeb: ('jmp direct within segment short'),
    0xec: ('in al, dx'),
    0xed: ('in ax, dx'),
    0xee: ('out dx, al'),
    0xef: ('out dx, ax'),
    0xf0: ('lock'),
    0xf1: (),
    0xf2: ('repne'),
    0xf3: ('rep'),
    0xf4: ('hlt'),
    0xf5: ('cmc'),
    0xf6: ('neg/mul/imul/div/idiv/not/test byte ea'),
    0xf7: ('neg/mul/imul/div/idiv/not/test word ea'),
    0xf8: ('clc'),
    0xf9: ('stc'),
    0xfa: ('cli'),
    0xfb: ('sti'),
    0xfc: ('cld'),
    0xfd: ('std'),
    0xfe: ('inc/dec byte ea'),
    0xff: ('push word EA', 'inc/dec word ea', 'call/jmp ind inner', 'call/jmp ind inter' ),
}

class Instruction:
    def __init__(self):
        pass

class ISA:

    def __init__(self, emulator):
        self.emulator = emulator
        self.cpu = self.emulator.cpu
        self.memory = self.emulator.memory
        self.opcodes = {
            0x00: self.handle_00
            }
        self.mem_index = 0
        self.op_prefix = 0
        self.ad_prefix = 0

    def next_data(self, size=1):
        address = self.mem_index
        value = self.memory.get_value(address, size=size)
        self.mem_index += size
        return value

    def handle_00(self):
        pass

    def parse_modrm(self):
        modrm_byte = self.next_data(size=1)
        mod = modrm_byte & 0b11000000 >> 6
        reg_bits = modrm_byte & 0b00111000 >> 3
        rm = modrm_byte & 0b00000111
        base = 0
        index = 0
        disp = 0
        if mod in [0b00, 0b01, 0b10]:
            if mod == 0b01: disp = self.next_data(size=1)
            elif mod == 0b10: disp = self.next_data(size=2)
            if rm == 0b000:
                base = self.cpu.bx
                index = self.cpu.si
            elif rm == 0b001:
                base = self.cpu.bx
                index = self.cpu.di
            elif rm == 0b010:
                base = self.cpu.bp
                index = self.cpu.si
            elif rm == 0b011:
                base = self.cpu.bp
                index = self.cpu.di
            elif rm == 0b100:
                index = self.cpu.si
            elif rm == 0b101:
                index = self.cpu.di
            elif rm == 0b110:
                if mod == 0b00:
                    disp = self.next_data(size=2)
                else:
                    # mod in [0b01, 0b10]
                    base = self.cpu.bp
            elif rm == 0b111:
                base = self.cpu.bx
        else:
            # mod == 0b11
            if self.op_prefix:
                reg = [
                    self.cpu.ax, self.cpu.cx, self.cpu.dx, self.cpu.bx,
                    self.cpu.sp, self.cpu.bp, self.cpu.si, self.cpu.di][rm]
            else:
                reg = [
                    self.cpu.al, self.cpu.cl, self.cpu.dl, self.cpu.bl,
                    self.cpu.ah, self.cpu.ch, self.cpu.dh, self.cpu.bh][rm]

                
            
            
        modrm = self.emulator.memory.get_value(self.emulator.cpu.cs << 4 | self.emulator.cpu.ip)
        print(hex(modrm))


if __name__ == '__main__':
    print('test')
