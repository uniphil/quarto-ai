from functools import reduce


init_board = (
    None, None, None, None,
    None, None, None, None,
    None, None, None, None,
    None, None, None, None,
)

rows = (
    (0, 1, 2, 3),
    (4, 5, 6, 7),
    (8, 9, 10, 11),
    (12, 13, 14, 15),
)

cols = (
    (0, 4, 8, 12),
    (1, 5, 9, 13),
    (2, 6, 10, 14),
    (3, 7, 11, 15),
)

diags = {
    '-1': (0, 5, 10, 15),
    '1': (12, 9, 6, 3),
}

traps = (
    (rows[0], cols[0], diags['-1']),
    (rows[0], cols[1]),
    (rows[0], cols[2]),
    (rows[0], cols[3], diags['1']),

    (rows[1], cols[0]),
    (rows[1], cols[1], diags['-1']),
    (rows[1], cols[2], diags['1']),
    (rows[1], cols[3]),

    (rows[2], cols[0]),
    (rows[2], cols[1], diags['1']),
    (rows[2], cols[2], diags['-1']),
    (rows[2], cols[3]),

    (rows[3], cols[0], diags['1']),
    (rows[3], cols[1]),
    (rows[3], cols[2]),
    (rows[3], cols[3], diags['-1']),
)

init_pieces = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)


quatro = lambda a, b, c, d:\
    a is not None and\
    b is not None and\
    c is not None and\
    d is not None and\
    bool(0b1111 &
        (a & b & c & d |
            ~a & ~b & ~c & ~d))


check = lambda board, spot:\
    any(quatro(*(board[p] for p in trap))
        for trap in traps[spot])


def place(board, piece, spot):
    next_board = list(board)
    next_board[spot] = piece
    return tuple(next_board)


empties = lambda board:\
    (spot for spot, board_piece in enumerate(board) if board_piece is None)


piece_wins = lambda board, piece:\
    any(check(place(board, piece, spot), spot) for spot in empties(board))


def place_win(board, piece):
    for spot in empties(board):
        maybe = place(board, piece, spot)
        if check(maybe, spot):
            return maybe


def place_piece(board, piece):
    if piece_wins(board, piece):
        return where_piece_wins(), True
    else:
        return place(board, piece, empties(board).send(None))


turn_wins = lambda board, pieces:\
    any(piece_wins(board, piece) for piece in pieces)


def get_nonwinning(board, pieces):
    for piece in pieces:
        if not turn_wins(board, pieces):
            return piece


def get_from(hint, cast, choices):
    while True:
        value = input(hint)
        try:
            value = cast(value)
        except ValueError:
            print('could not understand "{}" :( available options: {}'.format(
                value, ', '.join(map(str, choices))))
            continue
        if value in choices:
            return value
        else:
            print('could not find "{}" from available options: {}'.format(
                value, ', '.join(map(str, choices))))


parse_piece = lambda piece:\
    int(piece.replace('.', '0').replace('*', '1'), 2)


def parse_spot(s):
    nums = s.split(',')
    if len(nums) != 2:
        raise ValueError
    return reduce(lambda a, b: a + b*4, map(int, nums))


def player_move(board, pieces):
    piece = get_from('your piece: ', parse_piece, pieces)
    pieces_left = tuple(filter(lambda p: p!= piece, pieces))

    spot = get_from('your spot: ', parse_spot, tuple(empties(board)))
    new_board = place(board, piece, spot)
    return new_board, pieces_left, check(new_board, spot)


ppiece = lambda piece:\
    '{:04b}'.format(piece).replace('0', '.').replace('1', '*')


ppieces = lambda pieces:\
    ' '.join(map(ppiece, pieces))


pcell = lambda c, i=None:\
    '    ' if c is None else ppiece(c)


pboard = lambda board:\
    '+0---+1---+2---+3---+\n' +\
    '|\n+    +    +    +    +\n'.join(
        ('{}{}'.format(n, r) for n, r in enumerate(
            map(lambda r: ' '.join(
                map(pcell, r)),
                zip(*[board[i::4] for i in range(4)])))))+\
    '|\n+----+----+----+----+'


board = init_board
pieces = init_pieces
while True:
    print(pboard(board))
    print('remaining pieces:', ppieces(pieces))
    board, pieces, won = player_move(board, pieces)
    if won:
        print(pboard(board))
        print('you won!')
        break

