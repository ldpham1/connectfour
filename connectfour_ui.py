"""
ICS 32 Project 2

UCI_ID: 68168196 Name: Lillian Pham
UCI_ID: 24492089 Name: Wei Zhang
"""

import cf_server
import shared_module as cf
import connectfour

def _run_interface() -> None:
    HOST = cf_server.read_host()
    PORT = cf_server.read_port()
    
    connection = cf_server.connect(HOST, PORT)
    game_state = connectfour.new_game()

    while True:
        username = _ask_for_username()
        response = cf_server.welcome(connection, username)
        if response == cf_server.WELCOME:
            break
        
    while _send_AI_GAME_to_server(connection):
        pass

    cf.start_game(game_state)
    _send_command_to_server(game_state, connection)

def _ask_for_username() -> str:
    while True:
        username = input("Username: ").strip()
        if " " in username:
            print("You have a space in your username, please enter a username without spaces")
        elif username == "":
            print("You didn't enter anything. Please enter a valid username.")
        else:
            return username

def _send_AI_GAME_to_server(connection):
    cf_server.AI_GAME(connection)

def _send_command_to_server(game_state: connectfour.GameState, connection):
    cf_server.send_move(game_state, connection)

if __name__ == "__main__":
    _run_interface()
