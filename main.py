# -*- coding: utf-8 -*-

from typing import Callable, List

from src import piece
from src import seed_inspect
from src import condition_search

conditions: List[Callable[[piece.Piece,] , bool]] = [
    # I piece. Has orange. To the right of orange, there cannot be yellow nor red
    lambda piece: (
        piece.shape_is('I')
        and piece.colors_has('o')
        and piece.colors_right_cant('o', 'y', 'r')
        ),

    # Non-J piece. Has red and yellow. On top of yellow, there can be red
    lambda piece: (
        piece.shape_isnt('J')
        and piece.colors_has('r', 'y')
        and piece.colors_up_can('y', 'r')
        ),

    # Non-O-or-J piece. Has red.
    lambda piece: (
        piece.shape_isnt('O', 'J')
        and piece.colors_has('r')
        ),

    # Non-J piece. Has red and yellow. On top of red, there can be yellow
    lambda piece: (
        piece.shape_isnt('J')
        and piece.colors_has('r', 'y')
        and piece.colors_up_can('r', 'y')
        ),
]

if __name__ == '__main__':
    # seed_inspect.io_main()
    condition_search.io_main(conditions)
