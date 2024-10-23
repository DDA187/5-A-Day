from flask import Flask, render_template, request, redirect, url_for
import random
from datetime import datetime
import csv

app = Flask(__name__)

# Function to log user selections
def log_user_selection(username, selected_numbers):
    with open('user_selections.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username] + selected_numbers)

# Function to read user selections from CSV
def read_user_selections():
    user_data = []
    with open('user_selections.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            username = row[0]
            selected_numbers = list(map(int, row[1:]))
            user_data.append((username, selected_numbers))
    return user_data

# Function to handle user number selection
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        selected_numbers = [int(x) for x in request.form.getlist('numbers')]
        log_user_selection(username, selected_numbers)
        return redirect(url_for('thanks'))
    return render_template('index.html')

@app.route('/thanks')
def thanks():
    return "Thank you for your submission! Results will be available at 20:00."

# Function to display results after 20:00
@app.route('/results')
def results():
    current_time = datetime.now().strftime("%H:%M")
    if current_time < "20:00":
        return "Results will be available after 20:00."
    
    # Simulate the draw numbers
    drawn_numbers = random.sample(range(1, 37), 5)
    winners = check_users_against_draw(drawn_numbers)
    
    return render_template('results.html', drawn_numbers=drawn_numbers, winners=winners)

# Function to check user selections against drawn numbers
def check_users_against_draw(drawn_numbers):
    user_data = read_user_selections()
    winners = []
    for username, selection in user_data:
        correct_guesses = set(selection) & set(drawn_numbers)
        if len(correct_guesses) > 0:
            winners.append((username, len(correct_guesses)))
    return winners

if __name__ == '__main__':
    app.run(debug=True)
