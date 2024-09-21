
def neighbour_strings(x):
    n = []
    for pos in range(len(x)):
        c = ord(x[pos])
        if c < 127:
            n += [x[:pos] + chr(c + 1) + x[pos + 1:]]
        if c > 20:
            n += [x[:pos] + chr(c - 1) + x[pos + 1:]]
    return n

if __name__ == "__main__":
    print(neighbour_strings("Hello"))
