import connectfour

def start_game(game_state: connectfour.GameState):
    _print_instructions()
    print_board(game_state)

def ask_for_cmd() -> str:
    while True:
        try:
            player_input = input("Would you like to Drop or Pop? ").upper()
            if player_input.startswith("DROP") or player_input.startswith("POP"):
                return check_command(player_input)

def check_command(player_input: str) -> str:
    if player_input.startswith("DROP"):
        if 0 <= int(player_input[5:]) - 1 <= connectfour.BOARD_COLUMNS:
            return player_input
        else:
            _print_invalid_command()
    elif player_input.startswith("POP"):
        if 0 <= int(player_input[4:]) - 1 <= connectfour.BOARD_COLUMNS:
            return player_input
        else:
            _print_invalid_command()

def take_action_on_command(player_input: str, game_state: connectfour.GameState) -> connectfour.GameState:
    if player_input.startswith("DROP"):
        column_num = int(player_input[5:]) - 1
        return connectfour.drop(game_state, column_num)
    elif player_input.startswith("POP"):
        column_num = int(player_input[4:]) - 1
        return connectfour.pop(game_state, column_num)

def print_board(game_state: connectfour.GameState):
    _print_column_numbers()
    board = game_state.board
    board_columns = connectfour.BOARD_COLUMNS
    board_rows = connectfour.BOARD_ROWS
    for i in range(0, board_rows):
        for j in range(0, board_columns):
            print(_alter_board(board[j][i]), end = " ")
        print()

def _print_instructions():
    print("There are 7 columns to choose from.")
    print("Please enter DROP or POP, followed by a space and the column number.")
    print("DROP is the command to drop a game piece into the board.")
    print("POP is the command to remove the game piece at the bottom of the selected column.")
    print("However, you can only pop the game piece if it is your own.")
    print("You win if you can connect four pieces horizontally, vertically, or diagonally.")

def _alter_board(replace: int) -> str:
    if replace == 0:
        return "."
    elif replace == 1:
        return 'R'
    elif replace == 2:
        return "Y"

def _print_invalid_command():
    print("Your command is invalid. Please enter a valid command.")

def _print_column_numbers():
    column_list = []
    for num in range(connectfour.BOARD_COLUMNS):
        column_list.append(str(num + 1))
    print(" ".join(column_list))
