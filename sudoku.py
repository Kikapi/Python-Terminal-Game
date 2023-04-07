import random
from copy import deepcopy

class Cell:
    #Every cell will hold the number of the block, row and column that it belongs to
    #It also holds the value (digit from 1 to 9, or " " for empty cell),
    #fixed determines if the value in the cell is part of the initial setting, if True, player can't change its value
    def __init__(self, block, row, col, value=" ", fixed=True):
        self.block = block
        self.row = row
        self.col = col
        self.value = value
        self.fixed = fixed

    def set_value(self, num):
        if not self.fixed:
            self.value = num
    
class Board:
    BLOCKS_TO_CHECK = {
            #[blocks on the same row], [blocks on the same column] for each block
            1 : [[2, 3], [4, 7]],
            2 : [[1, 3], [5, 8]],
            3 : [[1, 2], [6, 9]],
            4 : [[5, 6], [1, 7]],
            5 : [[4, 6], [2, 8]],
            6 : [[4, 5], [3, 9]],
            7 : [[8, 9], [1, 4]],
            8 : [[7, 9], [2, 5]],
            9 : [[7, 8], [3, 6]]
        }
    def __init__(self):
        self.level = 1
        self.cell_count = 81  
        self.moves = []
        
        self.board = {block: [[Cell(block, row, col) for col in range(3)] for row in range(3)] for block in range(1, 10)}          
        
        self.result = {} 
          
        
    def create_new_board(self):
        for block in self.board:
            self.create_block(block)
        
        self.result = deepcopy(self.board)

        #eliminate few cells according with the level chosen
        blocks = [n for n in range(1, 10)]
        blocks_copy = []
        for i in range((5 + self.level)*6):

            while True:
                if not blocks:
                    blocks = blocks_copy.copy()
                block_num = random.choice(blocks)              
                current_cell = self.board[block_num][random.randint(0, 2)][random.randint(0, 2)]
                
                if current_cell.value != " ":                    
                    current_cell.value = " " 
                    current_cell.fixed = False 
                    self.cell_count -= 1 
                    blocks_copy.append(block_num)  
                    blocks.remove(block_num)               
                    break

    def create_block(self, key):
        options = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for row in range(3):
                for col in range(3):
                    copy_options = options.copy()
                    while copy_options:
                        num = random.choice(copy_options)
                        if self.is_possible(self.board[key][row][col], num)[0]:
                            options.remove(num)
                            self.board[key][row][col].value = num
                            break
                        else:
                            copy_options.remove(num)
        
        missing_num = self.block_is_not_complete(key)
        if missing_num:
            self.complete_block(key, missing_num)

    def block_is_not_complete(self, key):
        missing_num = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for row in range(3):
            for col in range(3):
                if self.board[key][row][col].value != " ":
                    missing_num.remove(self.board[key][row][col].value)           
        return missing_num
    
    def complete_block(self, key, list_missing_num):
        list_empty_cell = self.find_empty_cell(key)
        for num in list_missing_num:
            for ec in list_empty_cell:
                for row in range(3):
                    for col in range(3):
                        current_cell = self.board[key][row][col]
                        current_value = current_cell.value
                        current_cell.value = " "
                        new_cell = self.board[key][ec[0]][ec[1]]
                        if self.is_possible(current_cell, num)[0] and self.is_possible(new_cell, current_value)[0]:
                            current_cell.value = num
                            new_cell.value = current_value
                            list_empty_cell.remove(ec)
                            list_missing_num.remove(num)
                        else:
                            current_cell.value = current_value
        if list_empty_cell:
            self.complete_block_adv(key, list_missing_num)

    def complete_block_adv(self, key, list_missing_num):
        for num in list_missing_num:
            list_empty_cell = self.find_empty_cell(key)
            current_cell = self.board[key][list_empty_cell[0][0]][list_empty_cell[0][1]]
            current_cell.value = num
            while not self.is_possible(current_cell, current_cell.value)[0]:
                self.fix_collision(current_cell, self.is_possible(current_cell, current_cell.value)[1])

    def fix_collision(self, cell, coll_cell):
        
        self.board[(coll_cell.block)][coll_cell.row][coll_cell.col].value = " "
        if (coll_cell.block) in self.BLOCKS_TO_CHECK[cell.block][0]:
            #collision same row
            row_options = [0, 1, 2]
            row_options.remove(coll_cell.row)

            #if first row_option doesn't cause new collision swap with first option
            if self.is_possible(self.board[(coll_cell.block)][row_options[0]][coll_cell.col], cell.value)[0]:
                row = row_options[0]

            #other wise swap with second option
            else:
                row = row_options[1]
            current_cell = self.board[(coll_cell.block)][row][coll_cell.col]
            current_value = current_cell.value
            current_cell.value = cell.value
            coll_cell.value = current_value    

            #if swapped cell has collision, fix collision
            
            if not self.is_possible(current_cell, current_cell.value)[0]:
                self.is_possible(current_cell, current_cell.value)[1]

        
        
        if (coll_cell.block) in self.BLOCKS_TO_CHECK[cell.block][1]:
            #collision same col
            col_options = [0, 1, 2]
            col_options.remove(coll_cell.col)

            #if first col_option doesn't cause new collision swap with first option
            if self.is_possible(self.board[(coll_cell.block)][coll_cell.row][col_options[0]], cell.value)[0]:
                col = col_options[0]

            #other wise swap with second option
            else:
                col = col_options[1]

            current_value = self.board[(coll_cell.block)][coll_cell.row][col].value
            self.board[(coll_cell.block)][coll_cell.row][col].value = cell.value
            coll_cell.value = current_value

            #if swapped cell has collision, fix collision
            if not self.is_possible(self.board[(coll_cell.block)][coll_cell.row][col], self.board[(coll_cell.block)][coll_cell.row][col].value)[0]:
                self.is_possible(self.board[(coll_cell.block)][coll_cell.row][col], self.board[(coll_cell.block)][coll_cell.row][col].value)[1]
        
        #if collision cell has new collision after swapping, fix collision  
        if coll_cell.value != " " and not self.is_possible(coll_cell, coll_cell.value)[0]:
            self.fix_collision(coll_cell, self.is_possible(coll_cell, coll_cell.value)[1])  
            
    def find_empty_cell(self, key):
        list_empty_cells = []
        for row in range(3):
            for col in range(3):
                if self.board[key][row][col].value == " ":
                    list_empty_cells.append([row, col])
        return list_empty_cells

    def is_possible(self, cell, num):
      
        #check if possible in the same block
        for row in range(3):
            for col in range(3):
                if (cell.row != row or cell.col != col) and self.board[(cell.block)][row][col].value == num:
                    return False, self.board[(cell.block)][row][col]

        #check if possible in the same col    
        for block in self.BLOCKS_TO_CHECK[(cell.block)][1]:
            for row in range(3):
                if self.board[block][row][cell.col].value == num:
                    return False, self.board[block][row][cell.col]

        #check if possible in the same row
        for block in self.BLOCKS_TO_CHECK[(cell.block)][0]:
            for col in range(3):
                if self.board[block][cell.row][col].value == num:
                    return False, self.board[block][cell.row][col]   

        return True, cell

    def undo_last_move(self):
        if self.moves:
            block = self.moves[-1][0]
            row = self.moves[-1][1]
            col = self.moves[-1][2]
            prev_num = self.moves[-1][3]
            num = self.board[block][row][col].value
            if num == " " and prev_num != " ":
                self.cell_count += 1
            elif num != " " and prev_num == " ":
                self.cell_count -= 1
            self.board[block][row][col].value = prev_num
            self.moves.pop()
        self.print_board()


    def find_block_number(self, row, col):
        row_col_block = {
            0 : [1, 2, 3],
            1 : [4, 5, 6],
            2 : [7, 8, 9]
        }
        def convert_num(num):
            if num in [1, 2, 3]:
                return 0
            elif num in [4, 5, 6]:
                return 1
            else:
                return 2
        
        return row_col_block[convert_num(row)][convert_num(col)]
    
    def fill_one_cell(self, block, row, col, num):

        if self.board[block][row][col].fixed: 
            print("You can't change the number in this cell!! Pick another cell")
        else:
            if self.board[block][row][col].value == " ":
                if num == " ":
                    print("This cell is already empty.")
                else:
                    self.cell_count += 1
                    self.board[block][row][col].value = int(num)
                    
            else:
                if num == " ":
                    while True:
                        change = input(f"This cell has the number: {self.board[block][row][col].value}.\nWould you like TO DELETE this number? \ny or n: ")
                        if change in ['y', 'n']:
                            break 
                    if change == 'y':
                        self.board[block][row][col].value = " "
                        self.cell_count -= 1
                else: 
                    while True:
                        change = input(f"This cell has the number: {self.board[block][row][col].value}.\nWould you like to change this cell to number {num}? \ny or n: ")
                        if change in ['y', 'n']:
                            break
                    if change == 'y':
                        self.board[block][row][col].value = int(num)
                
    
    def print_board(self, game=True):

        print("\n  ", end=" ")
        for i in range(1, 10):
            if i == 4 or i == 5 or i== 7: 
                print("", end=" ")
            print("|  " + "C" + str(i), end=" ")
            if i == 7: 
                print("", end=" ")
            
        
        print("|"+"\n    -----------------   -----------------   -----------------")
        row_num = 1
        for init in [1, 4, 7]:
            for row in range(3):
                print("R" + str(row_num), end=" ")
                for x in range(3):
                    key = init + x
                    
                    
                    for col in range(3):
                        if game:
                            if col == 2:
                                if self.board[key][row][col].fixed:
                                    print("| ." + str(self.board[key][row][col].value) + ". |", end=" ")
                                else:
                                    print("|  " + str(self.board[key][row][col].value) + "  |", end=" ")
                                
                            else:
                                if self.board[key][row][col].fixed:
                                    print("| ." + str(self.board[key][row][col].value) + ".", end=" ")
                                else:
                                    print("|  " + str(self.board[key][row][col].value) + " ", end=" ")

                        else:
                            if col == 2:
                                print("|  " + str(self.result[key][row][col].value) + "  |", end=" ")                                
                            else:
                                print("|  " + str(self.result[key][row][col].value) + " ", end=" ")
                         
                        
                print("\n    -----------------   -----------------   -----------------")
                row_num += 1
            if init != 7:
                print("\n    -----------------   -----------------   -----------------")
        
    

    

         
    

    
            
    def board_correct(self):

        for block in self.board:
            for row in range(3):
                for col in range(3):
                    if self.board[block][row][col].value == " ":
                        print("The board is not complete")
                        return False
                    if not self.is_possible(self.board[block][row][col], self.board[block][row][col].value)[0]:
                        print(f"Error in block: {block}, row: {row}, col: {col}")  
                        return False
        print("Congratulations!!!!")  
        return True     



    def set_level(self, level):
        self.level = level



