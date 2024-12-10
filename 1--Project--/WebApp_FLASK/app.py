from flask import Flask, request, render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/register', methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']  # Campo per confermare la password
        
        # Verifica se le password corrispondono
        if password != confirm_password:
            return "Le password non corrispondono, riprova."

        # Verifica se il nome utente esiste già nel database
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        existing_user = c.fetchone()
        conn.close()

        if existing_user:
            return "Il nome utente esiste già. Scegli un nome utente diverso."

        # Se le password corrispondono e il nome utente è disponibile, salva i dati
        hashed_password = generate_password_hash(password)

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        conn.close()

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('SELECT password FROM users WHERE username = ?', (username,))
        stored_password = c.fetchone()
        conn.close()
        if stored_password and check_password_hash(stored_password[0], password):
            return 'Login success'
        else:
            return 'Invalid credentials'
    return render_template('login.html')

@app.route('/view_users')
def view_users():
    # Connessione al database SQLite
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Esegui una query per ottenere tutti gli utenti
    c.execute('SELECT * FROM users')
    users = c.fetchall()

    # Chiudi la connessione al database
    conn.close()

    # Mostra i dati in una pagina HTML
    return render_template('view_users.html', users=users)


if __name__ == '__main__':
    app.run(debug=True)
