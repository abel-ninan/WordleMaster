from flask import Flask, request, render_template, session
from flask_session import Session
import woordle_methods

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'possible_words' not in session or 'best_guess' not in session:
        # On first access or new game, initialize with all possible answers
        session['possible_words'] = woordle_methods.read_in_file("possible_answers.txt")
        session['best_guess'] = woordle_methods.calculate_best_guess(session['possible_words'])
    
    if request.method == 'POST':
        guess = request.form['guess'].lower()
        feedback = request.form['feedback'].lower()
        # Filter the words based on the guess and feedback
        session['possible_words'] = woordle_methods.filter_words(session['possible_words'], guess, feedback)
        # Calculate the next best guess
        session['best_guess'] = woordle_methods.calculate_best_guess(session['possible_words'])

    # Check if there are no possible words left
    if not session['possible_words']:
        message = "No possible words left. Start a new game."
        session.pop('possible_words', None)  # Clear the session for a new game
        session.pop('best_guess', None)
    else:
        message = session['best_guess']

    session.modified = True  # Notify Flask that the session has changed
    return render_template('index.html', best_guess=message)

if __name__ == '__main__':
    app.run(debug=True)
