import random
import time
from datetime import datetime
import csv
import sys

# Log user selections to a CSV file
def log_user_selection(username, selected_numbers):
    with open('user_selections.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username] + selected_numbers)

# User selects numbers before 19:30
def user_select_numbers():
    user_time_message = check_time()
    print(user_time_message)
    
    if user_time_message == "You can select your numbers.":
        username = input("Enter your username: ")
        user_selection = [int(x) for x in input("Enter 5 numbers (1-36) separated by spaces: ").split()]
        print("Your numbers are saved. Wait until the draw at 20:00.")
        log_user_selection(username, user_selection)
    
    elif user_time_message == "Selections closed. Please wait for the draw.":
        countdown_to_draw()

# Function to check time for the user's draw selection
def check_time():
    current_time = datetime.now()
    selection_cutoff = current_time.replace(hour=19, minute=30, second=0, microsecond=0)
    draw_time = current_time.replace(hour=20, minute=0, second=0, microsecond=0)
    
    if current_time < selection_cutoff:
        return "You can select your numbers."
    elif selection_cutoff <= current_time < draw_time:
        return "Selections closed. Please wait for the draw."
    else:
        return "The draw is happening."

# Countdown to 20:00 for users
def countdown_to_draw():
    current_time = datetime.now()
    draw_time = current_time.replace(hour=20, minute=0, second=0, microsecond=0)
    seconds_left = int((draw_time - current_time).total_seconds())
    
    while seconds_left > 0:
        mins, secs = divmod(seconds_left, 60)
        time_str = '{:02d}:{:02d}'.format(mins, secs)
        print(f"Countdown to draw: {time_str}", end='\r')
        time.sleep(1)
        seconds_left -= 1
    
    print("\nDraw starting...")

# Simulate drawing the numbers for users
def draw_numbers():
    encrypted_draw = read_encrypted_draw_from_file()  # Encrypted data that only admin can decrypt
    print("Drawing numbers...")
    for i in range(5):
        print(f"Number {i + 1}: {random.randint(1, 36)}")  # Appears random, but matches admin draw
        time.sleep(1)

# Read the encrypted draw numbers (without decrypting) for user visibility
def read_encrypted_draw_from_file():
    with open('draw_results.txt', 'r') as f:
        return f.read()

# Check how many numbers the user guessed correctly
def check_results(user_selection, drawn_numbers):
    correct_guesses = set(user_selection) & set(drawn_numbers)
    return len(correct_guesses)

# Example user game flow
if __name__ == "__main__":
    # User selects numbers before 19:30
    user_time_message = check_time()
    print(user_time_message)

    if user_time_message == "You can select your numbers.":
        user_selection = [int(x) for x in input("Enter 5 numbers (1-36) separated by spaces: ").split()]
        print("Your numbers are saved. Wait until the draw at 20:00.")
        log_user_selection("User1", user_selection)  # Add logging of user selection
    
    current_time = datetime.now()
    draw_time = current_time.replace(hour=20, minute=0, second=0, microsecond=0)

    # If it's before 20:00
    if current_time < draw_time:
        print("Your numbers are saved. Wait until the draw at 20:00.")
        sys.exit()  # Exit the game, preventing the draw from starting

    # Proceed with the draw after 20:00
    print("Drawing numbers...")
    draw_numbers()

    # Compare results (this would be done after all numbers are drawn)
    # In reality, this would match admin numbers, but we're simulating random here
    simulated_draw = [random.randint(1, 36) for _ in range(5)]
    correct = check_results(user_selection, simulated_draw)
    print(f"You guessed {correct} numbers correctly.")
