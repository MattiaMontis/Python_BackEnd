from flask import Flask, request, render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

# Creazione dell'oggetto Flask
app = Flask(__name__)

# Funzione per inizializzare il database SQLite
def init_db():
    conn = sqlite3.connect('users.db')  # Connessione al file del database
    c = conn.cursor()  # Creazione del cursore per eseguire query SQL
    # Creazione della tabella 'users' se non esiste
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  # ID unico per ogni utente
            username TEXT NOT NULL,               # Nome utente
            password TEXT NOT NULL                # Hash della password
        )
    ''')
    conn.commit()  # Salva i cambiamenti nel database
    conn.close()   # Chiude la connessione al database

# Inizializza il database all'avvio dell'applicazione
init_db()

# Rotta per la registrazione degli utenti
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':  # Gestione dei dati inviati dal modulo di registrazione
        username = request.form['username']  # Nome utente inserito dall'utente
        password = request.form['password']  # Password inserita dall'utente
        confirm_password = request.form['confirm_password']  # Conferma della password
        
        # Verifica se le password corrispondono
        if password != confirm_password:
            return "Le password non corrispondono, riprova."

        # Verifica se il nome utente esiste già nel database
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        existing_user = c.fetchone()  # Recupera l'utente se esiste
        conn.close()

        if existing_user:
            return "Il nome utente esiste già. Scegli un nome utente diverso."

        # Genera un hash della password e salva i dati nel database
        hashed_password = generate_password_hash(password)
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        conn.close()

        # Reindirizza l'utente alla pagina di login
        return redirect(url_for('login'))

    # Rende il template HTML per la registrazione
    return render_template('register.html')

# Rotta per il login degli utenti
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  # Gestione dei dati inviati dal modulo di login
        username = request.form['username']  # Nome utente inserito dall'utente
        password = request.form['password']  # Password inserita dall'utente
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        # Recupera l'hash della password per il nome utente specificato
        c.execute('SELECT password FROM users WHERE username = ?', (username,))
        stored_password = c.fetchone()
        conn.close()

        # Verifica se la password corrisponde all'hash salvato nel database
        if stored_password and check_password_hash(stored_password[0], password):
            return 'Login success'  # Login riuscito
        else:
            return 'Invalid credentials'  # Credenziali non valide

    # Rende il template HTML per il login
    return render_template('login.html')

# Rotta per visualizzare la lista degli utenti
@app.route('/view_users')
def view_users():
    # Connessione al database SQLite
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Recupera tutti gli utenti dal database
    c.execute('SELECT * FROM users')
    users = c.fetchall()  # Recupera tutti i risultati

    # Chiude la connessione al database
    conn.close()

    # Rende il template HTML con i dati degli utenti
    return render_template('view_users.html', users=users)

# Esegue l'applicazione Flask
if __name__ == '__main__':
    # Modalità debug attivata per lo sviluppo
    app.run(debug=True)
