# -*- coding: utf-8 -*-
"""
Created on Fri May 17 13:09:52 2019

@author: ACER
"""

tile_sprites = {
0xa652: (0x0, 'White Square'),
0xa65A: (0x2, 'Red Triangle'),
0xa662: (0x4, 'Gold Triangle'),
0xa66A: (0x6, 'Green Square'),
0xa672: (0x8, 'Blue Circle'),
0xa67A: (0xA, 'Orange Diamond'),
0xa682: (0xC, 'Pink Cross')
}

tile_id = {
0x0: 'White Square',
0x2: 'Red Triangle',
0x4: 'Yellow Triangle',
0x6: 'Green Square',
0x8: 'Blue Circle',
0xA: 'Orange Diamond',
0xC: 'Pink Cross'
}


def lower_half(hex_number):
    return (hex_number % 16**4)

def upper_half(hex_number):
    return (int((hex_number-int(lower_half(hex_number))) / 16**4))

def store_lower_half(source_value, target_value):
    # store_lower_half(0x8C81AC0A, 0x6115E4FA) -> 0x6115AC0A
    return upper_half(target_value) * 16**4 + lower_half(source_value)

def swap(source_value):
    return lower_half(source_value) * 16**4 + upper_half(source_value)

def eraser_rng_original(rng_seed):
    if rng_seed == 0:
        rng_seed = 0x2A6D365A

    d1 = rng_seed
    d0 = d1
    d1 = (d1 * 2**2) % 16**8
    d1 = (d1+d0) % 16**8
    d1 = (d1 * 2**3) % 16**8
    d1 = (d1+d0) % 16**8
    d0 = store_lower_half(d1, d0)
    d1 = swap(d1)
    d0 = store_lower_half(d0+d1, d0)
    d1 = store_lower_half(d0, d1)
    d1 = swap(d1)
    return d0, d1
    # d0 is the RNG value
    # d1 is the RNG seed


def eraser_rng_simplified(rng_seed):
    if rng_seed == 0:
        rng_seed = 0x2A6D365A

    d1 = rng_seed
    d0 = d1
    d1 = (41*rng_seed) % 16**8


    d0 = store_lower_half(d1, d0)
    d1 = swap(d1)
    d0 = store_lower_half(d0+d1, d0)
    d1 = store_lower_half(d0, d1)
    d1 = swap(d1)
    return d0, d1
    # d0 is the RNG value
    # d1 is the RNG seed


def eraser_rng(rng_seed):
    return eraser_rng_original(rng_seed)

def rng_cycle():
    rng_seeds_so_far = set()
    seed = 0
    while seed not in rng_seeds_so_far:
        rng_seeds_so_far.add(seed)
        value, seed = eraser_rng(seed)
        if len(rng_seeds_so_far) % 1000 == 0:
            print(len(rng_seeds_so_far))
    return seed, rng_seeds_so_far

class Piece():
    def __init__(self, colors):
        self.colors = [tile_id[i][0].lower() for i in colors]
        self.table = [[" ", " ", " ", " "],
                     [" ", " ", " ", " "]]

    def __eq__(self, other):
        return self.table == other.table

    def __repr__(self):
        return "\n"+" ".join(self.table[0]) + "\n" + " ".join(self.table[1]) + "\n         "

    def shape_is(self, *shapes):
        return self.name in set(shapes)

    def shape_isnt(self, *shapes):
        return self.name not in set(shapes)

    def colors_has(self, *colors):
        return set(colors).issubset(self.colors)

    def colors_hasnt(self, *colors):
        return not set(colors).intersection(self.colors)

    def colors_right_can(self, base_color, *colors):
        raise NotImplementedError

    def colors_right_cant(self, base_color, *colors):
        return not self.colors_right_can(base_color, *colors)

    def colors_left_can(self, base_color, *colors):
        raise NotImplementedError

    def colors_left_cant(self, base_color, *colors):
        return not self.colors_right_can(base_color, *colors)

    def colors_up_can(self, base_color, *colors):
        raise NotImplementedError

    def colors_up_cant(self, base_color, *colors):
        return not self.colors_up_can(base_color, *colors)

    def colors_down_can(self, base_color, *colors):
        raise NotImplementedError

    def colors_down_cant(self, base_color, *colors):
        return not self.colors_down_can(base_color, *colors)

    def colors_never_touch(self, base_color, *colors):
        raise NotImplementedError

class O_Piece(Piece):
    def __init__(self, colors):
        super().__init__(colors)
        self.name = 'O'
        self.table[1][0] = self.colors[0]
        self.table[1][1] = self.colors[1]
        self.table[0][1] = self.colors[2]
        self.table[0][0] = self.colors[3]

    # For O-pieces, these are all equivalent
    def colors_right_can(self, base_color, *colors):
        index = self.colors.index(base_color)
        return self.colors[index-3] in set(colors) or self.colors[index-1] in set(colors)

    def colors_left_can(self, base_color, *colors):
        return self.colors_right_can(base_color, *colors)

    def colors_up_can(self, base_color, *colors):
        return self.colors_right_can(base_color, *colors)

    def colors_down_can(self, base_color, *colors):
        return self.colors_right_can(base_color, *colors)

    # Except this one
    def colors_never_touch(self, base_color, *colors):
        index = self.colors.index(base_color)
        return self.colors[index-2] in set(colors)

class I_Piece(Piece):
    def __init__(self, colors):
        super().__init__(colors)
        self.name = 'I'
        self.table[0][2] = self.colors[0]
        self.table[0][1] = self.colors[1]
        self.table[0][0] = self.colors[2]
        self.table[0][3] = self.colors[3]

    def colors_right_can(self, base_color, *colors):
        index = self.colors.index(base_color)
        return self.colors[index-1] in set(colors)

    def colors_left_can(self, base_color, *colors):
        index = self.colors.index(base_color)
        return self.colors[index-3] in set(colors)

    def colors_up_can(self, base_color, *colors):
        return False

    def colors_down_can(self, base_color, *colors):
        return False

    def colors_never_touch(self, base_color, *colors):
        index = self.colors.index(base_color)
        return self.colors[index-2] in set(colors)


class T_Piece(Piece):
    def __init__(self, colors):
        super().__init__(colors)
        self.name = 'T'
        self.table[1][1] = self.colors[0]
        self.table[0][2] = self.colors[1]
        self.table[0][1] = self.colors[2]
        self.table[0][0] = self.colors[3]

    def colors_right_can(self, base_color, *colors):
        index = self.colors.index(base_color)
        return self.colors[index-1] in set(colors)

    def colors_left_can(self, base_color, *colors):
        index = self.colors.index(base_color)
        return self.colors[index-3] in set(colors)

    def colors_up_can(self, base_color, *colors):
        index = self.colors.index(base_color)
        return self.colors[index-2] in set(colors)

    def colors_down_can(self, base_color, *colors):
        return self.colors_up_can(base_color, *colors)

    def colors_never_touch(self, base_color, *colors):
        False


class L_Piece(Piece):
    def __init__(self, colors):
        super().__init__(colors)
        self.name = 'L'
        self.table[1][0] = self.colors[0]
        self.table[0][2] = self.colors[1]
        self.table[0][1] = self.colors[2]
        self.table[0][0] = self.colors[3]

    def colors_right_can(self, base_color, *colors):
        index = self.colors.index(base_color)
        return self.colors[index-1] in set(colors)

    def colors_up_can(self, base_color, *colors):
        return self.colors_right_can(base_color, *colors)

    def colors_left_can(self, base_color, *colors):
        index = self.colors.index(base_color)
        return self.colors[index-3] in set(colors)

    def colors_down_can(self, base_color, *colors):
        return self.colors_left_can(base_color, *colors)

    def colors_never_touch(self, base_color, *colors):
        index = self.colors.index(base_color)
        return self.colors[index-2] in set(colors)


class J_Piece(Piece):
    def __init__(self, colors):
        super().__init__(colors)
        self.name = 'J'
        self.table[1][2] = self.colors[0]
        self.table[0][2] = self.colors[1]
        self.table[0][1] = self.colors[2]
        self.table[0][0] = self.colors[3]

    def colors_right_can(self, base_color, *colors):
        index = self.colors.index(base_color)
        return self.colors[index-1] in set(colors)

    def colors_down_can(self, base_color, *colors):
        return self.colors_right_can(base_color, *colors)

    def colors_left_can(self, base_color, *colors):
        index = self.colors.index(base_color)
        return self.colors[index-3] in set(colors)

    def colors_up_can(self, base_color, *colors):
        return self.colors_left_can(base_color, *colors)

    def colors_never_touch(self, base_color, *colors):
        index = self.colors.index(base_color)
        return self.colors[index-2] in set(colors)

form_to_piece = {
    ((1, 2), (0, 2), (0, 1), (0, 0)): J_Piece,
    ((1, 0), (1, 1), (0, 1), (0, 0)): O_Piece,
    ((1, 1), (0, 2), (0, 1), (0, 0)): T_Piece,
    ((0, 2), (0, 1), (0, 0), (0, 3)): I_Piece,
    ((1, 0), (0, 2), (0, 1), (0, 0)): L_Piece
    }

d = {0: 0x0120, 2: 0x00AE, 4: 0x0000, 6: 0xFFF0,
 8: 0xFFF0, 10: 0xFFF0, 12: 0xFFE0, 14: 0xFFF0,
 16: 0x0110, 18: 0x00AE, 20: 0x0010, 22: 0xFFF0,
 24: 0x0000, 26: 0xFFF0, 28: 0xFFF0, 30: 0xFFF0,
 32: 0x0100, 34: 0x00AE, 36: 0x0020, 38: 0xFFF0,
 40: 0x0010, 42: 0xFFF0, 44: 0x0000, 46: 0xFFF0,
 48: 0x0100, 50: 0x00AE, 52: 0x0020, 54: 0xFFF0,
 56: 0x0010, 58: 0xFFF0, 60: 0x0000, 62: 0xFFF0,
 64: 0x0100, 66: 0x00AE, 68: 0x0010, 70: 0x0000,
 72: 0x0010, 74: 0xFFF0, 76: 0x0000, 78: 0xFFF0,
 80: 0x0100, 82: 0x00AE, 84: 0x0010, 86: 0x0000,
 88: 0x0010, 90: 0xFFF0, 92: 0x0000, 94: 0xFFF0,
 96: 0x0120, 98: 0x009E, 100: 0xFFF0, 102: 0x0000,
 104: 0xFFE0, 106: 0x0000, 108: 0x0010, 110: 0x0000,
 112: 0x0110, 114: 0x00AE, 116: 0x0010, 118: 0xFFF0,
 120: 0x0000, 122: 0xFFF0, 124: 0xFFF0, 126: 0xFFF0}

def next_piece(seed):
    tile_list = list()
    coords_hex = list()
    coords = list()

    # Generate the first tile
    while True:
        value, seed = eraser_rng(seed)
        value = (value % 8) * 2
        if value not in tile_list and value != 14:
            tile_list.append(value)
            break

    # Generate the piece
    offset = seed
    offset = swap(offset)
    offset = (offset % 8) * 4 * 4

    column_base = d[offset]
    row_base = d[offset+2]

    offset = offset + 4

    coords_hex_off = list()
    coords_hex_off.append([0, 0])
    coords_hex_off.append([d[offset], d[offset+2]])
    coords_hex_off.append([d[offset+4], d[offset+6]])
    coords_hex_off.append([d[offset+8], d[offset+10]])

    for i in range(4):
        current = coords_hex_off[i]
        current[0] = (current[0] + column_base) % 16**4
        current[1] = (current[1] + row_base) % 16**4
        coords_hex.append(current)

    for coord in coords_hex:
        # Eraser treats (column, row); I do (row, column)
        new_coord = ((coord[1]-158)//16, (coord[0]-256)//16)
        coords.append(new_coord)

    # Generate the other three tiles
    while len(tile_list) < 4:
        while True:
            value, seed = eraser_rng(seed)
            value = (value % 8) * 2
            if value not in tile_list and value != 14:
                tile_list.append(value)
                break

    # Generate the piece object
    piece = form_to_piece[tuple(coords)](tile_list)
    return piece, seed

def immediate_next_piece(output):
    return next_piece(int(output[1], 16))

def get_pieces(seed, n=1):
    l = list()
    for i in range(n):
        piece, seed = next_piece(seed)
        l.append(piece)
    return l

def search(conditions):
    seed = 0
    i = 0
    while True:
        if i % 1000 == 0:
            print(i)
        i += 1
        _, seed = eraser_rng(seed)
        case_seed = seed

        for j in range(len(conditions)):
            piece, case_seed = next_piece(case_seed)
            if not conditions[j](piece):
                break
        else:
            pieces = get_pieces(seed, n=4)
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
        _, seed = eraser_rng(seed)
        pieces = get_pieces(seed, n=5)
        d[i] = pieces
    print('---')

    for i in range(32768, 32768*2):
        if i % 1000 == 0:
            print(i)
        _, seed = eraser_rng(seed)
        pieces = get_pieces(seed, n=5)
        if d[i % 32768] != pieces:
            raise ValueError(i)

    return d

def io_main():
    while True:
        try:
            seed = int(input('Seed: '))
            n = int(input('Number of pieces: ' ))
            print("\n PIECES \n")
            print(get_pieces(seed, n))
        except ValueError:
            break

# I piece. Has orange. To the right of orange, there cannot be yellow nor red
condition1 = lambda piece: (
    piece.shape_is('I')
    and piece.colors_has('o')
    and piece.colors_right_cant('o', 'y', 'r')
    )

# Non-J piece. Has red and yellow. On top of yellow, there can be red
condition2 = lambda piece: (
    piece.shape_isnt('J')
    and piece.colors_has('r', 'y')
    and piece.colors_up_can('y', 'r')
    )

# Non-O-or-J piece. Has red.
condition3 = lambda piece: (
    piece.shape_isnt('O', 'J')
    and piece.colors_has('r')
    )

# Non-J piece. Has red and yellow. On top of red, there can be yellow
condition4 = lambda piece: (
    piece.shape_isnt('J')
    and piece.colors_has('r', 'y')
    and piece.colors_up_can('r', 'y')
    )

# L piece. Has yellow and orange. Yellow and orange never touch.
# To the right of orange, there cannot be red.
condition1 = lambda piece: (
    piece.shape_is('L')
    and piece.colors_has('y', 'o')
    and piece.colors_never_touch('y', 'o')
    and piece.colors_right_cant('o', 'r')
)

if __name__ == '__main__':
    #io_main()
    frame, seed, pieces = search([condition1, condition2, condition3, condition4])
    pass
