_TILE_SPRITES = {
0xa652: (0x0, 'White Square'),
0xa65A: (0x2, 'Red Triangle'),
0xa662: (0x4, 'Gold Triangle'),
0xa66A: (0x6, 'Green Square'),
0xa672: (0x8, 'Blue Circle'),
0xa67A: (0xA, 'Orange Diamond'),
0xa682: (0xC, 'Pink Cross')
}

_TILE_ID = {
0x0: 'White Square',
0x2: 'Red Triangle',
0x4: 'Yellow Triangle',
0x6: 'Green Square',
0x8: 'Blue Circle',
0xA: 'Orange Diamond',
0xC: 'Pink Cross'
}

class Piece():
    def __init__(self, colors):
        self.name = ''
        self.colors = [_TILE_ID[i][0].lower() for i in colors]
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
