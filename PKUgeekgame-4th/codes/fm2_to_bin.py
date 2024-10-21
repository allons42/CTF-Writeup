BUTTONS = ['A', 'B', 'S', 'T', 'U', 'D', 'L', 'R']

def int_to_input(i: int) -> str:
  '''
  Converts a byte to a string of 8 buttons.
  '''
  buttons = ''.join(BUTTONS[b] if (i & (1 << b)) else '.'
                    for b in range(7, -1, -1))
  return f'|0|{buttons}|........||\n'

def bin_to_fm2(bin: bytes) -> str:
  '''
  Converts the given binary data of per-frame input to an FM2 file.
  '''
  fm2 = ""
  for b in bin:
    fm2 += int_to_input(b)
  return fm2

def input_to_byte(input: str) -> bytes:
  '''
  Converts a string of 8 buttons to a byte.
  '''
  line = input.split('|')[2]
  x = 0
  for b in range(7, -1, -1):
    if BUTTONS[b] in line:
      x |= 1 << b
  return x.to_bytes(1, 'big')


def fm2_to_bin(fm2, start) -> bytes:
  '''
  Converts the given FM2 file to binary data of per-frame input.
  '''
  bin = b''
  for line in fm2.readlines()[start:]:
    bin += input_to_byte(line)
    
  return bin

if __name__ == "__main__":
  with open("klmz3-smb.fm2", 'r') as f:
    bin = fm2_to_bin(f, 13) # 改为实际的起始行号
  with open("flag1.bin", 'wb') as f:
    f.write(bin)