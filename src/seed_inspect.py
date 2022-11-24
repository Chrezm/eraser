from src import rng

def main(seed, n):
    return rng.get_pieces(seed, n=n)

def io_main():
    while True:
        try:
            seed = int(input('Seed: '))
            n = int(input('Number of pieces: ' ))
            print("\n PIECES \n")
            print(main(seed, n))
        except KeyboardInterrupt:
            break
