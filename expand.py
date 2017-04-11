#!/usr/bin/python

inp = [[0, 1], [2, 3, 4], [5, 6 ]]

outp = [0, 0, 0]
def expand(index):
    global outp
    if index >= len(inp):
        print outp
        return
    for i in range(len(inp[index])):
        outp[index] = inp[index][i]
        expand(index+1)

expand(0)
