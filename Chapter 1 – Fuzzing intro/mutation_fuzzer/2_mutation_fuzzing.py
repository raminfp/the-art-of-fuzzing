import random

def insert_random_character(s):
    """Returns s with a random character inserted"""
    pos = random.randint(0, len(s))
    random_character = chr(random.randrange(32, 127))
    # print("Inserting", repr(random_character), "at", pos)
    return s[:pos] + random_character + s[pos:]

if __name__ == "__main__":
    seed_input = "A quick brown fox"
    for i in range(10):
        print(repr(insert_random_character(seed_input)))


