MAX = 1000
MIN = -MAX

def neighbours(x, y):
    return [(x + dx, y + dy) for dx in [-1, 0, 1]
            for dy in [-1, 0, 1]
            if (dx != 0 or dy != 0)
            and ((MIN <= x + dx <= MAX)
                 and (MIN <= y + dy <= MAX))]

if __name__ == "__main__":
    print(neighbours(10, 10))
