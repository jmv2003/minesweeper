import random
import re
class Board:
    def __init__(self, dimension_size, num_bombs) -> None:
        self.dimension = dimension_size
        self.number_of_bombs = num_bombs
        
        # create the board
        self.board = self.create_board()
        # track locations of uncovered spots
        self.dug = set()
        self.assign_vals_to_board()

    def assign_vals_to_board(self):
        # up, down, right, left, up-right, etc.
        directions = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]]

        # inner function that checks the location for a bomb
        def check_loc(r, c):
            if r not in range(self.dimension) or c not in range(self.dimension) or self.board[r][c] != "*":
                return 0
            return 1
        # for every coordinate check and mark the number of adjacent bombs
        for row in range(self.dimension):
            for col in range(self.dimension):
                if self.board[row][col] == "*":
                    continue
                adj_bombs = 0
                for dr, dc in directions:
                    adj_bombs += check_loc(row + dr, col + dc)
                self.board[row][col] = adj_bombs

    
    def create_board(self):
        # generaten a new board
        board = [[None for _ in range(self.dimension)] for _ in range(self.dimension)]
        # plant bombs
        bombs_planted = 0
        while bombs_planted < self.number_of_bombs:
            x = random.randint(0, self.dimension - 1)
            y = random.randint(0, self.dimension - 1)
            if board[x][y] == "*":
                continue
            board[x][y] = "*"
            bombs_planted += 1
        return board
    
    def dig(self, row, col):
        # dig location
        # return True if no bomb, else False -> game over
        self.dug.add((row, col))
        if self.board[row][col] == "*":
            return False
        elif self.board[row][col] > 0:
            return True
        # No adjacent bombs -> dig around
        for r in range(max(0, row - 1), min(self.dimension - 1, row + 1) + 1):
            for c in range(max(0, col - 1), min(col + 1, self.dimension - 1) + 1):
                if (r, c) in self.dug:
                    continue
                else:
                    self.dig(r, c)
        return True

    # Prints the board with the visible/dug up locations
    def __str__(self) -> str:
        vis_board = [[None for _ in range(self.dimension)] for _ in range(self.dimension)]
        
        for r in range(self.dimension):
            for c in range(self.dimension):
                if (r, c) in self.dug:
                    vis_board[r][c] = str(self.board[r][c])
                else:
                    vis_board[r][c] = ' '
        
        
        # put this together in a string
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.dimension):
            columns = map(lambda x: x[idx], vis_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.dimension)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'
        
        for i in range(len(vis_board)):
            row = vis_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dimension)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep


def play(size=10, num_of_bombs=10):
    # create board and plant bombs
    board = Board(size, num_of_bombs)
    safe_spot = True
    while len(board.dug) < board.dimension**2 - num_of_bombs:
        print(board)
        user_input = re.split(',(\\s)*', input('Where would you like to dig? Input as row,col:'))
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= board.dimension or col < 0 or col >= board.dimension:
            print('Invalid location. Try again!')
            continue
        safe_spot = board.dig(row, col)
        if not safe_spot:
            print("Game Over")
            board.dug =[(r, c) for r in range(board.dimension) for c in range(board.dimension)]
            print(board)
            return None
    print("Congrats!")

if __name__ == '__main__': # Will only run if you enter 'python3 minesweeper.py'
    play()

