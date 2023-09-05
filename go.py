'''
Go game mechanics and rules are coded in this script.
'''


class Go:
    def __init__(self, size):
        self.size = size
        self.board = self.create_board()
        self.turn = 'black'

    def create_board(self):
        '''
        Creates an empty Go board of size tuples. Each filled with a string, initial '-' stating is not occupied.
        '''
        return [['-' for _ in range(self.size)] for _ in range(self.size)]

    def place_stone(self, x, y, color):
        '''
        Place a stone on the board. x and y are the coordinates, color is either 'black' or 'white'.
        After each stone is placed, check the board for any captured stones and remove them.
        If the placement is valid, switch turn between 'black' and 'white'.
        '''
        if self.board[x][y] == '-' and color == self.turn:
            self.board[x][y] = color
            self.remove_captured(x, y, self.opposite_color(color))
            self.turn = 'white' if self.turn == 'black' else 'black'
            return True
        return False

    def get_board(self):
        return self.board

    # def remove_captured(self, x, y, color):
    #     '''
    #     Check the board for any stones of the opposite color that have
    #     been completely surrounded (captured) after a stone placement and remove them.
    #     '''
    #
    #     for direction in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
    #         nx, ny = x + direction[0], y + direction[1]
    #         visited = set()
    #         if self.valid_position(nx, ny) and self.board[nx][ny] == color and \
    #                 self.group_has_no_liberties(nx, ny, visited):
    #             self.remove_group(nx, ny, visited)
    def remove_captured(self, x, y, color):
        '''
        Check the board for any stones of the opposite color that have
        been completely surrounded (captured) after a stone placement and remove them.
        '''
        checked = set()
        for direction in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nx, ny = x + direction[0], y + direction[1]
            if self.valid_position(nx, ny) and self.board[nx][ny] == color and (nx, ny) not in checked:
                visited = set()
                if self.group_has_no_liberties(nx, ny, visited):
                    for vx, vy in visited:
                        self.board[vx][vy] = '-'
                checked.update(visited)

    def group_has_no_liberties(self, x, y, visited):
        '''
        Check if the group of stones connected to the stone at (x, y) has any liberties (empty adjacent points).
        '''
        for direction in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nx, ny = x + direction[0], y + direction[1]
            if self.valid_position(nx, ny):
                if self.board[nx][ny] == '-':
                    return False
                elif self.board[nx][ny] == self.board[x][y] and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    if not self.group_has_no_liberties(nx, ny, visited):
                        return False
        return True

    def remove_group(self, x, y, visited):
        '''
        Remove all stones in the group connected to the stone at (x, y).
        '''
        self.board[x][y] = '-'
        for direction in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nx, ny = x + direction[0], y + direction[1]
            if self.valid_position(nx, ny) and self.board[nx][ny] == self.board[x][y] and (nx, ny) not in visited:
                visited.add((nx, ny))
                self.remove_group(nx, ny, visited)

    def valid_position(self, x, y):
        # TODO: forbid placing stones in the opponent's eye. (eye = surrounded by opponent's stones)
        # TODO: sometime can be placed in opponent's eye
        return 0 <= x < self.size and 0 <= y < self.size

    def opposite_color(self, color):
        return 'white' if color == 'black' else 'black'

    def calculate_score(self):
        # TODO: calculate score based on real rules
        black_score = 0
        white_score = 0
        for row in self.board:
            for cell in row:
                if cell == 'black':
                    black_score += 1
                elif cell == 'white':
                    white_score += 1
        return black_score, white_score

    def check_end(self):
        for row in self.board:
            for cell in row:
                if cell == '-':
                    return False
        return True

    def find_winner(self):
        black_score, white_score = self.calculate_score()
        if black_score > white_score:
            return 'black'
        elif white_score > black_score:
            return 'white'
        else:
            return 'draw'
