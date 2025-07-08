from flask import Flask, request, render_template_string, redirect, url_for, Response
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
        <form method="post" action="/submit">
            Name: <input type="text" name="name" required><br>
            Alter: <input type="number" name="alter" required><br>
            Problemtyp: <input type="text" name="problemtyp"><br>
            Kontakt: <input type="text" name="kontakt" required><br>
            <input type="submit" value="Absenden">
        </form>
    """)

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
    # Nach erfolgreicher Anmeldung weiterleiten
    return redirect(url_for('danke'))

# Diese Route fängt versehentliche GET-Anfragen auf /submit ab!
@app.route('/submit', methods=['GET'])
def submit_get():
    return redirect(url_for('home'))

@app.route('/danke', methods=['GET'])
def danke():
    return render_template_string("""
        <meta http-equiv="refresh" content="4; url=https://palucci888.github.io/resilienz/">
        <h2>Vielen Dank für Ihre Anmeldung!</h2>
        <p>Wir haben Ihre Daten erhalten und melden uns bald bei Ihnen.</p>
        <p>Sie werden in wenigen Sekunden zur Startseite zurückgeleitet.</p>
        <a href="https://palucci888.github.io/resilienz/">Zurück zur Startseite</a>
    """)

# --- Passwortschutz für die Anmeldeliste ---
def check_auth(username, password):
    return username == 'admin' and password == 'dein-passwort123'  # <--- HIER ANPASSEN

def authenticate():
    return Response(
        'Login erforderlich!', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )

@app.route('/anmeldungen', methods=['GET'])
def anmeldungen():
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM anmeldungen')
        rows = cursor.fetchall()
    return render_template_string("""
        <h2>Alle Anmeldungen</h2>
        <table border="1">
            <tr>
                <th>ID</th><th>Name</th><th>Alter</th><th>Problemtyp</th><th>Kontakt</th>
            </tr>
            {% for row in rows %}
            <tr>
                <td>{{ row[0] }}</td>
                <td>{{ row[1] }}</td>
                <td>{{ row[2] }}</td>
                <td>{{ row[3] }}</td>
                <td>{{ row[4] }}</td>
            </tr>
            {% endfor %}
        </table>
        <a href="/">Zurück zur Startseite</a>
    """, rows=rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
