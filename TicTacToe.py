import random


def tictactoe():
    def board_display(board):
        print("     |     |     ")
        print("  " + board[1] + "  |  " + board[2] + "  |  " + board[3] + "  ")
        print("_____|_____|_____")
        print("     |     |     ")
        print("  " + board[4] + "  |  " + board[5] + "  |  " + board[6] + "  ")
        print("_____|_____|_____")
        print("     |     |     ")
        print("  " + board[7] + "  |  " + board[8] + "  |  " + board[9] + "  ")
        print("     |     |     ")

    def win_check(board, mark):
        checkset = set()
        wins = [{1, 5, 9}, {3, 5, 7}, {7, 8, 9}, {4, 5, 6}, {1, 2, 3}, {1, 4, 7}, {2, 5, 8}, {3, 6, 9}]
        for i, v in enumerate(board):
            if v == mark:
                checkset.add(i)
        for i in wins:
            if i == checkset or i.issubset(checkset):
                return True

    def player_choice(board):
        def space_check(position):
            return position == " "

        while True:
            try:
                select = int(input("Please, select a position from 1 to 9 for your marker. Press 0 to exit"))
            except:
                print("Please, enter a number.")
                continue
            if 9 >= select >= 1:
                if space_check(board[select]):
                    return select
                else:
                    print("Sorry, this position is already taken.")  
            elif select == 0:
                break
            else:
                print("Please, enter a number from 1 to 9")

    def full_board_check(board):
        return " " not in board[1:10]

    def replay():
        choice = input("Do you want to play again? Y/N").upper()
        while True:
            if choice == "Y":
                return True
            elif choice == "N":
                print("Thanks for playing! Come back again!")
                return False
            else:
                print("Please, answer Y or N")
     

    def start():
        chars = ["X", "O"]

        def name_yourself(player_num):
            return [p for p in [input(f"Player {i}, please, "
                                      f"choose your player's name.") for i, p in enumerate(range(player_num), 1)]]

        name, name2 = name_yourself(2)
        print(f"{name}, please pick X or O as your marker. Press 0 to exit")
        while True:
            char = input().upper()
            if char == "O" or char == "X":
                chars.remove(char)
                char_2 = chars[0]
                print(f"{name}'s symbol is {char} and {name2}'s symbol is {char_2}")
                return name, name2, char, char_2
            elif char == "0":
                print("Farewell! Come back again!")
                game = False
                break
            else:
                print("Please, enter a correct value.")
            

    def whos_first(name, name2):
        first = random.choice([name, name2])
        print(f"{first} goes first! Press enter to continue.")
        input()
        return first

    def turn(x, mark, x2, game, current):
        board_display(board)
        print(f"{x}'s turn")
        position = player_choice(board)
        try:
            board[position] = mark
        except:
            game = False
        if win_check(board, mark):
            print(f"Congratulations, {x}! You've won!")
            game = False
        elif full_board_check(board):
            print("It's a tie!")
            game = False
        else:
            current = x2
        return current, game

    while True:
        try:
            board = [' '] * 10
            game = True
            name, name2, char, char_2 = start()
            current = whos_first(name, name2)
        except:
            break
        while game:
            if current == name:
                current, game = turn(name, char, name2, game, current)
            else:
                current, game = turn(name2, char_2, name, game, current)

        if not replay():
            break

tictactoe()
