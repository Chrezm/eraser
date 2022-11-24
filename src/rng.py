import piece

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

form_to_piece = {
    ((1, 2), (0, 2), (0, 1), (0, 0)): piece.J_Piece,
    ((1, 0), (1, 1), (0, 1), (0, 0)): piece.O_Piece,
    ((1, 1), (0, 2), (0, 1), (0, 0)): piece.T_Piece,
    ((0, 2), (0, 1), (0, 0), (0, 3)): piece.I_Piece,
    ((1, 0), (0, 2), (0, 1), (0, 0)): piece.L_Piece
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
