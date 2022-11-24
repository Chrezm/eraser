from src import rng

_LOOP_POINT = 32768

def search(conditions, i=0, seed=0):
    while i < _LOOP_POINT:
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
            return i, seed, pieces

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

def main(conditions):
    i, seed, pieces = search(conditions, i=0, seed=0)
    return i, hex(seed), pieces

def io_main(conditions):
    i = 0
    seed = 0
    while True:
        try:
            i, seed, pieces = search(conditions, i=i, seed=seed)
            print(i, hex(seed), pieces)
            user_response = ''
            while user_response not in ['y', 'n']:
                user_response = input("Continue searching? [y/n]: ")
                if user_response == "y":
                    break
                if user_response == 'n':
                    return
        except ValueError:
            return
