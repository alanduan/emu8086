from cpu import CPU
from memory import Memory
from isa import ISA

lookup_table = [
    lambda: 'hello',
    ]

def handle_code_00():
    print('handle 0x00')

opcodes = {
    0x00: handle_code_00,
}

class Emulator:

    def __init__(self):
        self.cpu = CPU()
        self.memory = Memory()
        self.isa = ISA(self)

    def get_instruction(self):
        address = (self.cpu.cs << 4) | self.cpu.ip
        aByte = self.memory.get_value(address)
        if aByte in self.isa.opcodes:
            self.isa.opcodes[aByte]()

        prefix = []
        opcode = []

    def run(self):
        instruction = self.get_instruction()

if __name__ == '__main__':
    emulator = Emulator()
    emulator.run()
