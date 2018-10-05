import connectfour
import shared_module as cf

def run_game():
    game_state = connectfour.new_game()
    cf.start_game(game_state)
    continue_game(game_state)
        
def continue_game(game_state: connectfour.GameState):
    winner = connectfour.winner(game_state)
    while winner == connectfour.NONE:
        try:
            player_input = cf.ask_for_cmd()
            game_state = cf.take_action_on_command(player_input, game_state)
            cf.print_board(game_state)
            winner = connectfour.winner(game_state)
            _determine_winner(winner)
        except connectfour.InvalidMoveError:
            print("Invalid move. Please try again.")
        except connectfour.GameOverError:
            print("You cannot make any additional moves. The game has ended.")
        except ValueError:
            print("Invalid column. Please try again.")

def _determine_winner(winner: int):
    if winner == connectfour.RED:
        print("Player RED has won.")
    elif winner == connectfour.YELLOW:
        print("Player YELLOW has won.")

if __name__ == "__main__":
    run_game()
