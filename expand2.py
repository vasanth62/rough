#!/usr/bin/python

inp = [range(15), range(16, 31), range(32, 48)]

outp = [[-1] * len(inp) for x in xrange(8)]
def expand(index):
    global outp
    if index >= len(inp):
        print outp
        return
    for i in xrange(0, len(inp[index]), 8):
        for j in xrange(8):
            if i+j >= len(inp[index]):
                outp[j][index] = -1
            else:
                outp[j][index] = inp[index][i+j]
        expand(index+1)

expand(0)
