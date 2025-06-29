# Simple Ludo Game Logic (text-based)

import random
import time

# Inisialisasi posisi token
player_positions = {"Player 1": 0, "Player 2": 0}
turn = "Player 1"
goal = 30  # target posisi untuk menang

def roll_dice():
    return random.randint(1, 6)

def move_player(player, steps):
    player_positions[player] += steps
    if player_positions[player] > goal:
        player_positions[player] = goal
    print(f"{player} rolled {steps} and moved to {player_positions[player]}")

def check_winner():
    for player, pos in player_positions.items():
        if pos == goal:
            print(f"\n🎉 {player} wins the game! 🎉")
            return True
    return False

def display_board():
    board = ["_" for _ in range(goal+1)]
    for player, pos in player_positions.items():
        if pos <= goal:
            board[pos] = player[0]  # P1 / P2
    print("Board: ", " ".join(board))

# Main game loop
def play_game():
    global turn
    game_over = False
    print("🎲 Ludo Game Start (2 Players, 1 Token Each)\n")
    
    while not game_over:
        input(f"{turn}, press Enter to roll the dice...")
        steps = roll_dice()
        move_player(turn, steps)
        display_board()
        game_over = check_winner()
        if not game_over:
            turn = "Player 2" if turn == "Player 1" else "Player 1"
        time.sleep(1)
        
    print("Game Over.")

play_game()
