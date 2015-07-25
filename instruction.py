
class Instruction:
    def __init__(self):
        pass

def is_valid_opcode(opcode):
    if 0xd8 <= opcode <= 0xdf:
        # x87
        return False
    if 0x60 <= opcode <= 0x6f:
        return False
    if  opcode in [0x26, 0x2e, 0x36, 0x3e]:
        return False
    if opcode in [0xc0, 0xc1, 0xc8, 0xc9, 0xd6, 0xf1]:
        return False
    if opcode == 0x0f:
        # two-byte instruction not supported yet
        return False
    if opcode == 0x82:
        # remove the alias for now
        return False
    return True

def requires_modrm_byte(opcode):
    if opcode in [
        0x00, 0x01, 0x02, 0x03, # add 
        0x08, 0x09, 0x0a, 0x0b, # or
        0x10, 0x11, 0x12, 0x13, # adc
        0x18, 0x19, 0x1a, 0x1b, # ssb
        0x20, 0x21, 0x22, 0x23, # and
        0x28, 0x29, 0x2a, 0x2b, # sub
        0x30, 0x31, 0x32, 0x33, # xor
        0x38, 0x39, 0x3a, 0x3b, # cmp
        0x80, 0x81, 0x82, 0x83, # EA<-IMM
        0x84, 0x85, 0x86, 0x87, # test, xchg
        0x88, 0x89, 0x8a, 0x8b, # mov
        0x8c, 0x8d, 0x8e, 0x8f, # mov, lea, pop
        0xc4, 0xc5, 0xc6, 0xc7, # les, lds, mov
        0xd0, 0xd1, 0xd2, 0xd3, # shl/shr/sal/sar/rol/ror/rcl/rcr
        0xf6, 0xf7, 0xfe, 0xff, # jmp, call, push, inc/dec
        ]:
        return True
    return False

def requires_immediate_data(opcode, modrm_byte):
    if opcode in [0xf6, 0xf7] and parse_modrm_byte(modrm_byte)[1] == 0b000:
        return True
    if opcode in [
        0x04, 0x05, # add
        0x0c, 0x0d, # or
        0x14, 0x15, # adc
        0x1c, 0x1d, # ssb
        0x24, 0x25, # and
        0x2c, 0x2d, # sub
        0x34, 0x35, # xor
        0x3c, 0x3d, # cmp
        0x80, 0x81, 0x82, 0x83, # arithmetic, logic EA<-IMM
        0x9a, # call
        0xa0, 0xa1, 0xa2, 0xa3, # mov
        0xa8, 0xa9, # test
        0xc2, # ret n
        0xc6, 0xc7, # mov EA, IMM
        0xca, # retf n
        0xcd, # int n
        0xe0, 0xe1, 0xe2, 0xe3, # loopnz/loopz/loop/jcxz
        0xe4, 0xe5, # in AL/AX, port
        0xe6, 0xe7, # out port, AL/AX
        0xe8, # call DISP16
        0xe9, 0xea, 0xeb, # jmp direct
        ]:
        return True
    if 0x70 <= opcode <= 0x7f:
        return True
    if 0xb0 <= opcode <= 0xbf:
        # mov REG8, IMM8
        # mov REG16, IMM16
        return True
    if opcode in [0xd4, 0xd5]:
        return True
    return False
    
def get_immediate_size(opcode, modrm_byte=0):
    if opcode in [0xf6, 0xf7] and parse_modrm_byte(modrm_byte)[1] == 0b000:
        return 2**(opcode & 1)
    if opcode in [
        0x04, 0x05, # add
        0x0c, 0x0d, # or
        0x14, 0x15, # adc
        0x1c, 0x1d, # ssb
        0x24, 0x25, # and
        0x2c, 0x2d, # sub
        0x34, 0x35, # xor
        0x3c, 0x3d, # cmp
        0x80, 0x81, 0x82, # arithmetic, logic EA<-IMM
        0xa8, 0xa9, # test
        0xc6, 0xc7, # mov EA, IMM
        ]:
        return 2**(opcode & 1)
    if opcode in [
        0xa0, 0xa1, 0xa2, 0xa3,# mov
        0xc2, 0xca, # ret n; retf n
        0xe8, # call DISP16
        0xe9, # jmp DISP16 
        ]:
        return 2
    if 0x70 <= opcode <= 0x7f:
        return 1
    if 0xb0 <= opcode <= 0xb7:
        return 1
    if 0xb8 <= opcode <= 0xbf:
        return 2
    if opcode in [
        0x83,
        0xcd, # int n
        0xe0, 0xe1, 0xe2, 0xe3, # loopnz/loopz/loop/jcxz
        0xe4, 0xe5, # in AL/AX, port
        0xe6, 0xe7, # out port, AL/AX
        0xeb, # jmp short disp8
        ]:
        return 1
    if opcode in [
        0x9a, # call seg16:offset16
        0xea, # jmp far seg16:offset16
        ]:
        return 4
    if opcode in [0xd4, 0xd5]:
        return 1
    return 0

def parse_modrm_byte(modrm_byte):
    mod = (modrm_byte & 0b11000000) >> 6
    reg = (modrm_byte & 0b111000) >> 3
    rm = modrm_byte & 0b111
    return (mod, reg, rm)

def get_disp_size(modrm_byte):
    mod, _, rm = parse_modrm_byte(modrm_byte)
    if mod == 0b11 or (mod == 0b00 and rm != 0b110):
        return 0
    if mod == 0b01:
        return 1
    if mod == 0b10 or (mod == 0b00 and rm == 0b110):
        return 2

def get_instruction(buf, start_address):
    instruction_bytes = []
    next_address = start_address
    opcode = buf[next_address]
    next_address += 1
    if not is_valid_opcode(opcode):
        raise Exception('invalid opcode 0x%02x at %d' % (
            opcode, next_address))
    # supported opcode
    instruction_bytes.append(opcode)
    modrm_byte = None
    if requires_modrm_byte(opcode):
        modrm_byte = buf[next_address]
        next_address += 1
        instruction_bytes.append(modrm_byte)
        mod, reg, rm = parse_modrm_byte(modrm_byte)
        if opcode == 0xff and reg == 0b111:
            raise Exception('unsupported instruction')
        if opcode == 0xff and reg == 0b101 and mod == 0b11:
            raise Exception('invalid instruction: mod cannot be 0b11 for indirect jmp within segment')
        if opcode == 0xff and reg == 0b011 and mod == 0b11:
            raise Exception('invalid instruction: mod cannot be 0b11 for indirect call within segment')
        if opcode == 0xfe and reg != 000:
            raise Exception('invalid instruction: reg must be 0b000 for inc byte EA')
        if (opcode == 0xf7 or opcode == 0xf6) and reg == 001:
            raise Exception('invalid instruction: reg cannot be 0b001 for 0xf6 or 0xf7')
        if opcode == 0x82 and reg in [0b001, 0b100, 0b110]:
            raise Exception('s bit does not apply to logic extension')
        if opcode == 0x8d and mod == 0b11:
            raise Exception('lea applies to memory only')
        if (opcode == 0x8c or opcode == 0x8e) and (reg & 0b100 != 0):
            raise Exception('seg should be in [0, 1, 2, 3]')
        if opcode == 0x8f and reg != 0b000:
            raise Exception('reg must be 0b000 for pop EA16')
        if opcode in [0xc4, 0xc5] and mod == 0b11:
            raise Exception('les, lds can only load from memory')
        if opcode in [0xc6, 0xc7] and reg != 000:
            raise Exception('mov EA, imm; reg must be 0b000')
        if opcode in [0xd0, 0xd1, 0xd2, 0xd3] and reg == 0b110:
            raise Exception('invalid exception')
            
        disp_size = get_disp_size(modrm_byte)
        disp_bytes = []
        for i in range(disp_size):
            disp_bytes.append(buf[next_address])
            next_address += 1
        instruction_bytes.extend(disp_bytes)
        #print (disp_bytes)
    if requires_immediate_data(opcode, modrm_byte):
        immediate_size = get_immediate_size(opcode, modrm_byte)
        immediate_bytes = []
        for i in range(immediate_size):
            immediate_bytes.append(buf[next_address])
            next_address += 1
        instruction_bytes.extend(immediate_bytes)
    return instruction_bytes

if __name__ == '__main__':
    import sys
    import binascii
    buf = [0xb0, 0x00, 0xf0, 0xf1, 0xf2, 0xf3]
    instruction = get_instruction(buf, 0)
    print(list(map(hex, instruction)))
    out = open('instruction.dat', 'wb')
    single_byte_instruction = False
    for i in range(256):
        if single_byte_instruction:
            single_byte_instruction = False
        for j in range(256):
            buf = [i, j, 0xf0, 0xf1, 0xf2, 0xf3]
            try:
                instruction = get_instruction(buf, 0)
                for byte in instruction:
                    out.write(chr(byte))
                if len(instruction) == 1:
                    single_byte_instruction = True
                    break
                    
            except:
                continue
    out.close()
