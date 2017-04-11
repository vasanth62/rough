board = [-1]*144
idx = 0
for i in xrange(12):
    if i > 1 and i < 10:
        for j in xrange(12):
            if j > 1 and j < 10:
                board[i*12+j] = idx
                idx += 1

next_vals = [None] * 64
offsets = [10, -10, 14, -14, 23, -23, 25, -25]
def get_next(x):
    # For a square return a set of all possible next squares
    if next_vals[x]:
        return next_vals[x]

    i = ((x/8)+2) * 12 + (x%8) + 2
    n = set()
    for offset in offsets:
        n.add(board[i+offset])
    n.discard(-1)
    next_vals[x] = n
    return n

def bfs(start, dest):
    count = 0 
    visited, queue = set([-1]), [start, -1]
    while queue:
        vertex = queue.pop(0)
        if vertex == -1:
            count += 1
            queue.append(-1)
        if vertex == dest:
            return count
        if vertex not in visited:
            visited.add(vertex)
            n = get_next(vertex)
            queue.extend(n)
    assert(0)


def answer(src, dest):
    if src < 0 or src >= 64:
        return 0
    if dest < 0 or dest >= 64:
        return 0
    return bfs(src, dest)


print board
print answer(19,36)
print answer(0,1)
print answer(0,63)

