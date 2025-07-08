from flask import Flask, request, render_template_string
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

@app.route('/submit', methods=['POST'])
def submit():
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

    return render_template_string("""
        <h2>Vielen Dank für Ihre Anmeldung!</h2>
        <p>Wir haben Ihre Daten erhalten und melden uns bald bei Ihnen.</p>
        <a href="/">Zurück zur Startseite</a>
    """)

@app.route('/')
def home():
    return "Backend läuft!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
