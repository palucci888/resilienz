from flask import Flask, request, render_template_string, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_NAME = 'anmeldungen.db'

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS anmeldungen (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                alter_person INTEGER NOT NULL,
                problemtyp TEXT,
                kontakt TEXT NOT NULL
            )
        ''')
        conn.commit()

init_db()

@app.route('/', methods=['GET'])
def home():
    return render_template_string("""
        <h2>Anmeldeformular</h2>
        <form method="POST" action="/submit">
            Name: <input type="text" name="name" required><br>
            Alter: <input type="number" name="alter" required><br>
            Problemtyp: <input type="text" name="problemtyp"><br>
            Kontakt: <input type="text" name="kontakt" required><br>
            <input type="submit" value="Absenden">
        </form>
    """)

# POST verarbeitet das Formular, GET leitet freundlich auf die Startseite um (Schutz vor Method Not Allowed)
@app.route('/submit', methods=['POST'])
def submit_post():
    name = request.form.get('name')
    alter = request.form.get('alter')
    problemtyp = request.form.get('problemtyp')
    kontakt = request.form.get('kontakt')

    if not name or not alter or not kontakt:
        return "Fehler: Bitte alle Pflichtfelder ausfüllen.", 400

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO anmeldungen (name, alter_person, problemtyp, kontakt)
            VALUES (?, ?, ?, ?)
        ''', (name, int(alter), problemtyp, kontakt))
        conn.commit()

    return redirect(url_for('danke'))

@app.route('/submit', methods=['GET'])
def submit_get():
    # Falls jemand /submit
