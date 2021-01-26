import turtle

t = turtle.Turtle()
screen = turtle.Screen()
screen.bgcolor("black")
t.up()
t.ht()
t.speed(0)
t.tracer(1, 3)
t.color("white")


def display(board):
    d = []
    for row in board:
        r = []
        for x in row:
            if x == 0:
                r.append('-')
            elif x == 1:
                r.append('o')
            elif x == -1:
                r.append('X')
            elif x == -2:
                r.append('/')
        d.append(r)
    return d


def draw_rect(l, w):
    t.begin_fill()
    for i in range(2):
        t.forward(l)
        t.left(90)
        t.forward(w)
        t.left(90)
    t.end_fill()


def draw_board(board):
    board = display(board)
    rows = len(board)
    cols = len(board[0])
    gap = 20
    t.forward(gap)
    for i in range(cols):
        t.write(i)
        t.forward(gap)
    t.backward(gap * cols)
    t.backward(gap)
    for i in range(rows):
        t.right(90)
        t.forward(gap)
        t.left(90)

        t.write(i)
        t.forward(gap)
        for j in range(cols):
            n = board[i][j]
            if n == 'X':
                t.color('red')
                t.forward(gap / 4)
                t.write(n, align="center", font=("Arial", 15, "bold"))
                t.color('white')
                t.backward(gap / 4)
            elif n == 'o':
                t.color('dark slate blue')
                draw_rect(gap * 2 / 3, gap * 2 / 3)
                t.color('white')
            elif n == '/':
                t.dot(gap / 3)
            else:
                t.write(n)
            t.forward(gap)
        t.backward(gap * cols)
        t.backward(gap)


def draw_text(text):
    t.write(text, align="center", font=("Arial", 10, "bold"))


def draw(bot, mine):
    t.clear()
    t.goto(0, 180)
    draw_text("Computer")
    t.goto(-80, 150)
    draw_board(bot)
    t.goto(0, 20)
    draw_text("You")
    t.goto(-80, 0)
    draw_board(mine)


from random import randint as rint

HIT = -1
MISS = -2
SHIP = 1


def user_move(secret_bot, display_bot):
    print("Where do you want to attack opponent?")
    row = int(input("Row:"))
    col = int(input("Col:"))
    if secret_bot[row][col] == SHIP:
        print("HIT")
        display_bot[row][col] = HIT
    else:
        print("Miss")
        display_bot[row][col] = MISS
    return display_bot


def bot_move(user):
    print("Where do you want to attack opponent?")
    rows = len(user)
    cols = len(user[0])
    row = rint(0, rows - 1)
    col = rint(0, cols - 1)
    print("Computer attacks the point:", row, ",", col)
    if user[row][col] == SHIP:
        print("HIT")
        user[row][col] = HIT
    else:
        print("Miss")
        user[row][col] = MISS
    return user


def new_board(rows=5, columns=5):
    board = []
    for i in range(rows):
        row = []
        for i in range(columns):
            row.append(0)
        board.append(row)
    return board


def show(board):
    for row in board:
        text = ''
        for x in row:
            if x == 0:
                pt = '-'
            elif x == SHIP:
                pt = 'o'
            elif x == HIT:
                pt = 'X'
            elif x == MISS:
                pt = '/'
            text += ' ' + pt
        print(text)


def check_validity(board, row, col, ship_len, d):
    if d == 'v' and (row + ship_len) <= len(board) and col <= len(board[0]):
        return True
    elif d == 'h' and (col + ship_len) <= len(board[0]) and row <= len(board):
        return True
    else:
        print(row, col, d)
        return False


def place_ship(board, row, col, ship_len, d):
    if check_validity(board, row, col, ship_len, d) == False:
        print("Invalid")
        return False
    for i in range(ship_len):
        board[row][col] = SHIP
        if d == 'v':
            row += 1
        elif d == 'h':
            col += 1
    return True


def place_random_ship(bot, ship_len):
    num_cols = len(bot[0])
    num_rows = len(bot)
    chance = rint(0, 1)
    if chance:
        max_col = num_rows - ship_len - 1
        col = rint(0, max_col)
        row = rint(0, num_rows - 1)
        place_ship(bot, row, col, ship_len, 'h')
    else:
        max_row = num_rows - ship_len - 1
        row = rint(0, max_row)
        col = rint(0, num_cols - 1)
        place_ship(bot, row, col, ship_len, 'v')


def valid_move(board, r, c):
    return r < len(board) and r >= 0 and c < len(board[0]) and c >= 0


def place_user_ship(mine, ship_len):
    print("")
    print("Place your battleship. The ship is {} units long.".format(ship_len))
    while True:
        d = input("Horizontal or vertical? Type 'h' or 'v': ")
        if d == 'h' or d == 'v':
            break
        if d != 'h' or d != 'v':
            print('invalid')
            continue
        print("Now choose starting point of your battleship.")
        row = int(input("Row: "))
        col = int(input("Column: "))
        if not valid_move(mine, row, col):
            continue
        if place_ship(mine, row, col, ship_len, d) == True:
            break


def count_hits(board):
    hits = 0
    for row in board:
        for x in row:
            if x == HIT:
                hits += 1
    return hits


from random import randint

user = new_board()
secret_bot = new_board()
display_bot = new_board()
ship_length = 4
draw(display_bot, user)
place_user_ship(user, ship_length)
place_random_ship(secret_bot, ship_length)
while True:
    user_move(secret_bot, display_bot)
    if count_hits(display_bot) == ship_length:
        draw(display_bot, user)
        print('you win')
        break
    bot_move(user)
    draw(display_bot, user)
    if count_hits(user) == ship_length:
        draw(display_bot, user)
        print('you lose2')
        break
    draw(display_bot, user)