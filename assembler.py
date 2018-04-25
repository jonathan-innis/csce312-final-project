from string import ascii_lowercase
from sys import stdin

REGISTERS = 7
WIDTH = 16

ops = ['rmmov', 'mrmov', 'rrmov', 'irmov', 'add', 'sub', 'cmp', 'mult', 'jmp']
regs = ['rtmp'] + ['r' + c for c in ascii_lowercase[:REGISTERS]] 
flags = ['ao', 'lz', 'le', 'eq', 'ge', 'gz']

op_codes = {s:i for i, s in enumerate(ops)}
reg_codes = {s:i for i, s in enumerate(regs)}
flag_codes = {s:i for i, s in enumerate(flags)}
mark_codes = {}

op_codes['halt'] = 0x10

def to_byte(x):
    return hex(x)[2:].zfill(2)

def const_to_tmp(x):
    return '03 00 ' + to_byte(int(x)) + ' '

def decode_instr(instr):
    global instr_count
    spl = instr.lower().split()
    if instr[0] == '#' or not spl:
        return

    if spl[0][-1] == ':':
        markers[spl[0][:-1]] = 3*instr_count
        spl = spl[1:]

    op = spl[0]
    op_code = op_codes[op]
    args = [s.strip() for s in ''.join(spl[1:]).split(',')]

    args_out = [0, 0, 0]
    dummy = ''
    if op in ('cmp', 'rmmov', 'mrmov', 'rrmov', 'add', 'sub', 'mul'):
        if args[0] in reg_codes:
            args_out[0] = reg_codes[args[0]]
        else:
            assert op in ('mrmov', 'rrmov'), 'bad register name'
            dummy = const_to_tmp(args[0])
            args_out[0] = 0
        if op != 'cmp':
            assert op == 'rmmov', 'bad register name'
            dummy = const_to_tmp(args[1])
            args_out[1] = reg_codes[args[1]]
    elif op == 'jmp':
        args_out[0] = flag_codes[args[0]]
        args_out[2] = mark_codes[args[1]]

    if dummy:
        instr_count += 2
    else:
        instr_count += 1
        
    out_codes = [op_code, args_out[0]<<4 + args_out[1], args_out[2]]
    return dummy + ' '.join(map(to_byte, out_codes))

def main():
    k = 0
    bytes = (' '.join(filter(None, map(decode_instr, stdin)))).split()
    while len(bytes) % WIDTH:
        bytes.append('00')
    for i in range(len(bytes) // WIDTH):
        print(*bytes[i:i+WIDTH])

main()
