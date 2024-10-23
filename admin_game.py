import csv
import random
import os
from cryptography.fernet import Fernet
from datetime import datetime

# Generate or load encryption key for admin
key = b'4h1QTbiqH0GieACZ-MWkeaQi-bSG3gstd8-NqV-ygk0='  # You should replace this with your actual Fernet key
cipher_suite = Fernet(key)

# Function to setup predetermined draw numbers
def setup_draw():
    numbers = random.sample(range(1, 37), 5)  # Draw 5 unique numbers between 1 and 36
    print(f"Predetermined numbers for today's draw are: {numbers}")
    
    # Encrypt the numbers before saving
    encrypted_numbers = cipher_suite.encrypt(str(numbers).encode())

    # Save encrypted numbers to file
    with open('draw_results.txt', 'wb') as f:
        f.write(encrypted_numbers)

    print("Predetermined draw saved.")

# Function to view the predetermined draw before 20:00 (admin only)
def view_draw():
    with open('draw_results.txt', 'rb') as f:
        encrypted_data = f.read()

    # Decrypt the draw numbers
    decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
    print(f"Today's predetermined draw numbers are: {decrypted_data}")

# Function to read user selections from CSV
def read_user_selections():
    user_data = []
    if os.path.exists('user_selections.csv'):
        with open('user_selections.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                user_data.append(row)  # Append each row (username + 5 numbers)
    return user_data

# Check which users guessed correctly based on the draw
def check_users_against_draw(drawn_numbers):
    user_data = read_user_selections()

    winners = []
    for row in user_data:
        username = row[0]  # First column is username
        selection = [int(num) for num in row[1:]]  # Remaining columns are user's numbers
        correct_guesses = set(selection) & set(drawn_numbers)
        
        if len(correct_guesses) > 0:
            winners.append((username, len(correct_guesses)))
    
    return winners

# Display results of users' guesses after the draw
def display_user_results():
    # Decrypt the draw numbers first
    with open('draw_results.txt', 'rb') as f:
        encrypted_data = f.read()
    drawn_numbers = eval(cipher_suite.decrypt(encrypted_data).decode())

    print(f"The drawn numbers were: {drawn_numbers}")
    
    # Check user selections against the draw
    winners = check_users_against_draw(drawn_numbers)
    
    if winners:
        for winner in winners:
            print(f"User {winner[0]} guessed {winner[1]} numbers correctly!")
    else:
        print("No users guessed the numbers correctly.")

# Main game logic for admin
if __name__ == "__main__":
    while True:
        action = input("Type 'setup' to set up today's draw, 'view' to see the numbers before 20:00, or 'results' to check user results: ").strip().lower()

        if action == 'setup':
            setup_draw()

        elif action == 'view':
            current_time = datetime.now().strftime("%H:%M")
            if current_time < "20:00":
                view_draw()
            else:
                print("It's past 20:00. You can no longer view the draw.")

        elif action == 'results':
            display_user_results()

        else:
            print("Invalid input. Please try again.")
