import sys

HALT = 0
PRINT_TIM = 1
PRINT = 2
PRINT_NUM = 3
PRINT_SUM = 4
SAVE = 5
ADD = 6

# memory = [
# 	PRINT_TIM,
# 	PRINT_NUM,
# 	45,
# 	PRINT_SUM,
# 	10, 
# 	32,
# 	SAVE,
# 	2,
# 	99,
# 	PRINT,
# 	2,
# 	SAVE,
# 	3,
# 	1,
# 	PRINT,
# 	3,
# 	ADD,
# 	2,
# 	3,
# 	PRINT,
# 	2,
# 	HALT
# ]

ram = [0] * 256
registers = [0] * 8

PC = 0
running = True

def load_memory():
  address = 0
  
  try: 
    with open(sys.argv[1]) as file:
      for line in file:
        comment_split = line.split('#')
        possible_number = comment_split[0]
          
        if possible_number == '':
          continue
      
        first_bit = possible_number[0]

        if first_bit == '0' or first_bit == '1':
          instruction = int(possible_number[0:8], base = 2)
          ram[address] = instruction
          address += 1
          print('{:08b}, {:d}'.format(instruction, instruction))
  except IOError: # FileNotFoundError
    print('I cannot file that file, check the name')
    sys.exit(1)
  except IndexError:
    print('Please provide a filename.')
    sys.exit(2)

load_memory()

while running:
  command = ram[PC]
	
  if command == PRINT_TIM:
	  print('Tim!')
	  PC += 1
  elif command == PRINT:
	  index = ram[PC + 1]
	  print(registers[index])
	  PC += 2
  elif command == PRINT_NUM:
	  num = ram[PC + 1]
	  print(num)
	  PC += 2
  elif command == PRINT_SUM:
	  first_num = ram[PC + 1]
	  second_num = ram[PC + 2]
	  print(first_num + second_num)
	  PC += 3
  elif command == SAVE:
    first_num = ram[PC + 1]
    second_num = ram[PC + 2]
    registers[first_num] = second_num
    PC += 3
  elif command == ADD:
  	first_num = ram[PC + 1]
  	second_num = ram[PC + 2]
  	registers[first_num] += registers[second_num]
  	PC += 3
  elif command == HALT:
  	running = False
  else:
  	print('command not recognized: {}'.format(command))
  	running = False