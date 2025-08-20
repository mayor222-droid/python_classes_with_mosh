import random
import re

# lets create a board object to represent the minesweeper game
# this is so that we can just say"create a new board object", or
# "dig here", or "render this game for this object"
class Board:
    def _init_(self, dim_size, num_bombs):
       # let's keep track of these parameters. they'll helpful later
       self.dim_size  = dim_size
       self.num_bombs = num_bombs

       # let's create the board
       # helper function!
       self.board = self.make_new_board() # plant the bombs
       self.assign_new_values_to_board()
       
    
       # initialize a set to keep track of which location we've uncovered
       # we'll save (row, col) tuplesinto this set
       self.dug = set() # if we dig at 0, 0, then self. dug = {(0,0)}

    def make_new_board(self):
        # construct a new board based on the dim size and num bombs
        # we should construct the list of lists here (or whatever representation you prefer
        # but since we have a 2-D board, list of lists is most natural)
        
        # generate a new board
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]

        # plant the bombs
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size**2 -1)
            row = loc // self.dim_size
            col = loc % self.dim_size

            if board[row][col] == '*':
                # this means we've actually planted a bomb there already so keep going
                continue

            board[row][col] = '*' # planted the bomb
            bombs_planted += 1

        return board    

    def assign_new_values_to_board(self):


        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    # if this is already a bomb, we don't want to calculate anything
                    continue
                self.board[r][c] = self.get_num_neighboring_bombs(r, c)
                
    def get_num_neighboring_bombs(self, row, col):

        num_neighboring_bombs = 0
        for r in range(max(0, row-1),min(self.dim_size-1, (row+1))+1):
            for c in  range(max(0,col-1), min(self.dim_size-1, col+1)+1):
                if r == row and c == col:
                    # our original location, don't check
                    continue
                if self.board[r][c] == '*':
                    num_neighboring_bombs += 1

        return num_neighboring_bombs   

    def dig(self, row, col):        # dig at that location
    
        # return true if sucessful dig, false if bomb dug
        
        # a few scenarios:for r in range(max(0,row-1), min(sel
        # hit a bomb -> game over
        # dig at location with neighboring bombs -> recursively dig neighboring!

        self.dug.add((row, col))

        if self.board[row][col]  == '*':
            return False
        elif self.board[row][col] > 0:
            return True
        
        # self.board[row][col] == 0
        for r in range(max(0, row-1),min(self.dim_size-1, (row+1))+1):
            for c in  range(max(0,col-1), min(self.dim_size-1, col+1)+1):
                if (r, c) in self.dug:
                    continue # don't dig where you've already dug
                self.dig(r, c)

        # if our initial dig didn't hit a bomb, we shouldn't hit a bomb here
        return True          

def _str_(self):
         # this is a magic functio where if you call print on this object
         # it'll print out what this function returns
         # return a string that shows the board to the player


         # first let's create a new array that represents what thw user would see
         visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
         for row in range(self.dim_size):
             for col in range(self.dim_size):
                 if (row,col) in self.dug:
                     visible_board[row][col] = str(self.board[row][col])
                 else:
                    visible_board[row][col] = ''

         # put this together in a string

# play the game
def play(dim_size=10, num_bombs=10):
    # step 1: create the board and plant the bombs
    board = Board(dim_size, num_bombs)
    # step 2: show the user the board and ask for where they want to dig
    # step 3a: if location is not a bomb, dig recursively until each square is at least
    #           next to a bomb
    # step 4: repeat steps 2 and 3a/b until there are no more places to dig -> VICTORY
    safe = True

    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        print(board)
        # 0,0 or 0,0 or 0,   0
        user_input = re.split(',(\\s)*', input("where would you like to dig? input as row, col:")) # 0, 3
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= board.dim_size or col < 0 or col >= dim_size:
            print("invalid location, try again.")
            continue

        # if it's valid, we dig
        safe = board.dig(row,col)
        if not safe:
            # dug a bomb ahhhhhhh
            break # (game over rip)

    # 2 ways to end loop, let's check which one 
    if safe:
        print("congratulations!!!! YOU ARE VICTORIOUS!")
    else:
        print("SORRY GAME OVER :(")
        # let's reveal the whole board!
        board.dug = [(r,c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)

if __name__=='_main_': # good practice :
    play()        
 