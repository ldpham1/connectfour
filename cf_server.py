"""
ICS 32 Project 2

UCI_ID: 68168196 Name: Lillian Pham
UCI_ID: 24492089 Name: Wei Zhang
"""

import socket
from collections import namedtuple
import shared_module as cf
import connectfour

ServerConnection = namedtuple("Connection", ["socket", "input", "output"])

WELCOME = 0
READY = 1
OKAY = 2
INVALID = 3

def read_host() -> str:
    while True:
        host = input("Host: ").strip()
        if host == "":
            print("Please specify a host.")
        elif host != "woodhouse.ics.uci.edu":
            print("Please enter 'woodhouse.ics.uci.edu' for the host.")
        else:
            return host

def read_port() -> int:
    while True:
        try:
            port = int(input("Port: ").strip())
            if port < 0 or port > 65535:
                print("Ports must be an integer between 0 and 65535.")
            elif port != 4444:
                print("Please enter the port number '4444'.")
            else:
                return port

        except ValueError:
            print("Ports must be an integer between 0 and 65535.")
  
def connect(host: str, port: int) -> ServerConnection:
    cf_socket = socket.socket()
    cf_socket.connect((host, port))
    cf_socket_input = cf_socket.makefile("r")
    cf_socket_output = cf_socket.makefile("w")
    return ServerConnection(
        socket = cf_socket,
        input = cf_socket_input,
        output = cf_socket_output)

def welcome(connection: ServerConnection, username: str) -> WELCOME:
    _write_line(connection, "I32CFSP_HELLO " + username)
    response = _read_line(connection)
    if response.startswith("WELCOME"):
        print(response)
        return WELCOME

def AI_GAME(connection: ServerConnection) -> READY:
    _write_line(connection, "AI_GAME")
    response = _read_line(connection)
    if response == "READY":
        print(response)
        return READY
    else:
        print(response)
        _close_sockets(connection)

def send_move(game_state: connectfour.GameState, connection: ServerConnection):
    winner = connectfour.winner(game_state)
    while winner == connectfour.NONE:
        try:
            user_input = cf.ask_for_cmd()
            game_state = cf.take_action_on_command(user_input, game_state)
            _write_line(connection, user_input)

            response, game_state = _check_responses(connection, game_state)

            if _end_game(connection, response, game_state) == False:
                break

            cf.print_board(game_state)
        except connectfour.InvalidMoveError:
            print("Invalid move. Please try again.")
        except connectfour.GameOverError:
            print("You cannot make any additional moves. The game has ended.")
        except ValueError:
            print("Invalid column. Please try again.")

def _read_line(connection: ServerConnection) -> str:
    line = connection.input.readline()[:-1]
    return line

def _write_line(connection: ServerConnection, line: str):
    connection.output.write(str(line) + "\r\n")
    connection.output.flush()

def _check_responses(connection: ServerConnection, game_state: connectfour.GameState) -> tuple:
    for i in range(3):
        response = _read_line(connection)
        print(response)
        
        if response.startswith("DROP") or response.startswith("POP"):
            cf.check_command(response)
            game_state = cf.take_action_on_command(response, game_state)
        
        elif response == "WINNER_RED":
            break
        
    return response, game_state

def _close_sockets(connection: ServerConnection):
    connection.input.close()
    connection.output.close()
    connection.socket.close()
    
def _end_game(connection: ServerConnection, response: str, game_state: connectfour.GameState) -> bool:
    server_status = True
    if response == "WINNER_RED" or response == "WINNER_YELLOW":
        server_status = False
        cf.print_board(game_state)
        _close_sockets(connection)
        print("The game has ended. Closing server...")
        print("Server Closed.")
        return server_status
    return server_status

