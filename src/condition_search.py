import rng

def search(conditions):
    seed = 0
    i = 0
    while True:
        if i % 1000 == 0:
            print(i)
        i += 1
        _, seed = rng.eraser_rng(seed)
        case_seed = seed

        for j in range(len(conditions)):
            piece, case_seed = rng.next_piece(case_seed)
            if not conditions[j](piece):
                break
        else:
            pieces = rng.get_pieces(seed, n=4)
            print(i, hex(seed), pieces)
            if input("Continue searching? [y/n]: ") == "y":
                continue
            return i, hex(seed), pieces

        if i == 32768:
            raise ValueError('Reached loop point.')

def all_combos():
    d = dict()
    seed = 0
    for i in range(32768):
        if i % 1000 == 0:
            print(i)
        _, seed = rng.eraser_rng(seed)
        pieces = rng.get_pieces(seed, n=5)
        d[i] = pieces
    print('---')

    for i in range(32768, 32768*2):
        if i % 1000 == 0:
            print(i)
        _, seed = rng.eraser_rng(seed)
        pieces = rng.get_pieces(seed, n=5)
        if d[i % 32768] != pieces:
            raise ValueError(i)

    return d
