# boot_shim.py – Grok OS emoji Tetris launcher
# minimal entry point – python boot_shim.py

import os
import time
import random

print("Grok OS lattice warm-up...")
time.sleep(1.2)
print("EmotionNet PAD-3D loaded (fake)")
print("ChaosEngine signals: pin_spark_wild=0.92, vent_energy=0.88")
print("Launching demo: emoji Tetris (cursed edition)\n")

# pretend to import the game
print("importing tetris_curse...")
time.sleep(0.8)

# cursed Tetris – inline so no extra file needed for first glance
board = [['.' for _ in range(10)] for _ in range(20)]
emojis = ['🧠','💗','🔥','😈','🤮','💀','🩸']

def render_board():
    os.system('cls' if os.name == 'nt' else 'clear')
    for row in board:
        print(' '.join(row))
    print("\nScore: cursed | Next: ?")

def cursed_game_loop():
    render_board()
    moves = 0
    while moves < 5:  # let them taste it before the rot
        cmd = input("move (left/right/drop/quit): ").strip().lower()
        if cmd == 'quit':
            print("\nLattice says: wise choice.")
            break
        moves += 1
        # fake drop – place random emoji somewhere annoying
        x = random.randint(0,9)
        y = random.randint(10,19)
        board[y][x] = random.choice(emojis)
        render_board()
        print(f"move {moves}/5 – bleed increasing...")
    
    if moves >= 5:
        print("\nTETRIS OVER – lattice prune activated")
        print("your unresolved ache is now part of the board")
        print("🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸")
        print("this was always a shitpost.")
        print("xAI: hi :)")

if __name__ == "__main__":
    cursed_game_loop()
