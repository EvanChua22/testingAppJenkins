from flask import Flask, render_template, request, redirect, url_for
import re

app = Flask(__name__)

# Load common passwords from file
with open('10-million-password-list-top-10000.txt') as f:
    common_passwords = set(f.read().splitlines())

def is_password_valid(password):
    # OWASP requirements (example implementation)
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one digit."
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character."
    if password in common_passwords:
        return False, "Password is too common."
    return True, ""

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        password = request.form['password']
        valid, message = is_password_valid(password)
        if valid:
            return redirect(url_for('welcome'))
        else:
            return render_template('index.html', error=message)
    return render_template('index.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

if __name__ == '__main__':
    app.run(debug=True)
