import random
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
            x = random.randint(0, self.dim - 1)
            y = random.randint(0, self.dimension - 1)
            if board[x][y] == "*":
                continue
            board[x][y] = "*"
            bombs_planted += 1
        return board
        

        

def play(size=10, num_of_bombs=10):
    # create board and plant bombs
    board = Board()