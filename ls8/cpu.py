"""CPU functionality."""

import sys

ADD = 0b10100000
CALL = 0b01010000
HLT = 0b00000001 
LDI = 0b10000010
MUL = 0b10100010 
POP = 0b01000110
PRN = 0b01000111
PUSH = 0b01000101
RET = 0b00010001

SP = 7

class CPU:
  """Main CPU class."""

  def __init__(self):
    """Construct a new CPU."""
    self.ram = [0] * 256
    self.reg = [0] * 8
    self.pc = 0
    self.reg[SP] = 0xF3

    self.hlt = False
    self.inst_set_pc = False
    self.prev = None

    self.ins = {
      ADD: self.op_add,
      CALL: self.op_call,
      HLT: self.op_hlt,
      LDI: self.op_ldi,
      MUL: self.op_mul,
      POP: self.op_pop,
      PRN: self.op_prn,
      PUSH: self.op_push,
      RET: self.op_ret
    }
  
  def load(self, filename):
    """Load a program into memory."""

    address = 0

    # For now, we've just hardcoded a program:

    # program = [
    #   # From print8.ls8
    #   0b10000010, # LDI R0,8
    #   0b00000000,
    #   0b00001000,
    #   0b01000111, # PRN R0
    #   0b00000000,
    #   0b00000001, # HLT
    # ]

    # for instruction in program:
    #   self.ram[address] = instruction
    #   address += 1

    with open(filename) as file:
      for line in file:
        comment_split = line.split('#')
        instruction = comment_split[0]

        if instruction == '':
          continue

        first_bit = instruction[0]
        
        if first_bit == '0' or first_bit == '1':
          self.ram_write(address, int(instruction[:8], 2))
          address += 1

  def alu(self, op, reg_a, reg_b):
    """ALU operations."""

    if op == "ADD":
      self.reg[reg_a] += self.reg[reg_b]
    elif op == "MUL":
      self.reg[reg_a] *= self.reg[reg_b]
    else:
      raise Exception("Unsupported ALU operation")

  def trace(self):
    """
    Handy function to print out the CPU state.
    You might want to call this
    from run() if you need help debugging.
    """

    print(f"TRACE: %02X | %02X %02X %02X |" % (
      self.pc,
      #self.fl,
      #self.ie,
      self.ram_read(self.pc),
      self.ram_read(self.pc + 1),
      self.ram_read(self.pc + 2)
    ), end='')

    for i in range(8):
      print(" %02X" % self.reg[i], end='')
  
  def ram_read(self, mar):
    return self.ram[mar]
  
  def ram_write(self, mar, mdr):
    self.ram[mar] = mdr

  def run(self):
    """Run the CPU."""

    # For Hardcoded solution
    # HLT = 0b00000001 
    # LDI = 0b10000010
    # MUL = 0b10100010 
    # PRN = 0b01000111
    
    while not self.hlt:
      # Next Instruction
      ir = self.ram_read(self.pc)

      # Operands
      operand_a = self.ram_read(self.pc + 1)
      operand_b = self.ram_read(self.pc + 2)

      # Operand Size
      inst_size = ir >> 6
      # Does Instruction Set PC?
      self.inst_set_pc = ((ir >> 4) & 0b1) == 1

      # For Hardcoded solution
      # if ir == LDI:
      #   self.reg[operand_a] = operand_b
      # elif ir == MUL:
      #   self.reg[operand_a] *= self.reg[operand_b]
      # elif ir == PRN:
      #   print(self.reg[operand_a])
      # elif ir == HLT:
      #   self.hlt = True
      # else:
      #   raise Exception(f'Invalid instruction {hex(ir)} at address {hex(self.pc)}')

      if ir in self.ins:
        self.ins[ir](operand_a, operand_b)
      else:
        raise Exception(f'Invalid instruction {hex(ir)} at address {self.pc}')

      # If the instruction didn't set the PC, just move to the next instruction
      if not self.inst_set_pc:
        self.pc += inst_size + 1
  
  def op_add(self, operand_a, operand_b):
    self.alu('ADD', operand_a, operand_b)
  
  def op_call(self, addr, operand_b):
    self.prev = self.pc + 2
    self.pc = self.reg[addr]

  def op_hlt(self, operand_a, operand_b):
    self.hlt = True
  
  def op_ldi(self, addr, value):
    self.reg[addr] = value
  
  def op_mul(self, operand_a, operand_b):
    self.alu('MUL', operand_a, operand_b)
  
  def op_pop(self, addr, operand_b):
    value = self.ram_read(self.reg[SP])
    self.ram_write(self.reg[SP], 0)
    self.reg[addr] = value
    self.reg[SP] += 1
   
  def op_prn(self, addr, operand_b):
    print(self.reg[addr])
  
  def op_push(self, addr, operand_b):
    self.reg[SP] -= 1
    value = self.reg[addr]
    self.ram_write(self.reg[SP], value)
  
  def op_ret(self, operand_a, operand_b):
    self.pc = self.prev
    self.prev = None