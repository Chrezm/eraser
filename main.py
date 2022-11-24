# -*- coding: utf-8 -*-

from src import seed_inspect
from src import condition_search

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

conditions = [condition1, condition2, condition3, condition4]

if __name__ == '__main__':
    seed_inspect.io_main()
    #condition_search.io_main(conditions)
