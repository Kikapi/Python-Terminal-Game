import sudoku

#Codecademy Portfolio Project: Python Terminal Game (Computer Science path)

"""Sudoku is a logic-based, combinatorial number-placement puzzle. 
    In classic Sudoku, the objective is to fill a 9 × 9 grid with digits so that each column, each row, 
    and each of the nine 3 × 3 subgrids that compose the grid (also called "boxes", "blocks", or "regions") 
    contain all of the digits from 1 to 9. The puzzle setter provides a partially completed grid, which for a 
    well-posed puzzle has a single solution. (Wikipedia)"""



print("Welcome to Sudoku!!!")

game_on = True
while game_on:
    new_game = sudoku.Board()
    #Select puzzle level
    while True:
        level = input("Select level: \nEnter 1 for Very Easy\n2 for Easy\n3 for Medium \n4 for Hard \n5 for Expert: ")
        if level in ['1', '2', '3', '4', '5']:
            new_game.set_level(int(level))
            break
        else:
            print("That's not a valid option!!")

    new_game.create_new_board()
    new_game.print_board()
    print("\nLet's get started!!!\n")
    print("\nEnter 'e' to see the solution and exit the game")
    print("\nEnter 'u' to undo last move")
    
    

    while new_game.cell_count < 81: 
        exit = False
        undo = False
        back = False

        while not exit and not undo and not back:
            col = input("\nSelect column: ")
            if col == 'e':
                exit = True
                break
            elif col == 'u':
                new_game.undo_last_move()
                undo = True
            elif col == 'b':
                back = True
                break
            elif col not in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                print("Column number must be between 1 and 9") 
            else:
                col = int(col)            
                break
        while not exit and not undo and not back:
            row = input("\nSelect row: ")
            if row == 'e':
                exit = True
                break
            elif row == 'u':
                new_game.undo_last_move()
                undo = True
            elif row == 'b':
                back = True
                break
            elif row not in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:            
                print("Row number must be between 1 and 9")
            else:
                row = int(row)
                break
        while not exit and not undo and not back:
            num = input("\nSelect number ('0' to clear the cell): ")
            if num == 'e':
                exit = True
                break
            elif num == 'u':
                new_game.undo_last_move()
                undo = True
            elif num == 'b':
                back = True
                break
            elif num == '0':
                num = " "
                break
            elif num not in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                print("Number must be between 1 and 9")
            else:
                num = int(num)
                break

        if exit:
            new_game.print_board(False)
            break
        elif not undo and not back:
            block = new_game.find_block_number(row, col)
            row = (row % 3 - 1)
            col = (col % 3 - 1)
            old_value = new_game.board[block][row][col].value
            new_game.moves.append([block, row, col, old_value])
            new_game.fill_one_cell(block, row, col, num)
            new_game.print_board()
                    
            
    if new_game.cell_count == 81:
        print("You have completed the board! Let's check if your solution is correct... \n")
        new_game.board_correct()
    play_again = input("\nWould you like to play again?? ('y' or 'n'): ")
    if play_again == 'y':
        print("\nLet's play again!!")
        
    else:    
        print("\nHope you had a great time!! See you soon!!")
        game_on = False