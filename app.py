from flask import Flask, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

# ---------- DATABASE CONNECTION ----------
def get_db():
    conn = sqlite3.connect('coffee.db')
    conn.row_factory = sqlite3.Row
    return conn

# ---------- INITIALIZE DATABASE ----------
def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS coffee (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            votes INTEGER DEFAULT 0
        )
    ''')

    # Insert default data only if empty
    cursor.execute("SELECT COUNT(*) FROM coffee")
    if cursor.fetchone()[0] == 0:
        coffee_list = ['Espresso', 'Latte', 'Cappuccino', 'Americano']
        for coffee in coffee_list:
            cursor.execute("INSERT INTO coffee (name) VALUES (?)", (coffee,))

    conn.commit()
    conn.close()

# ---------- HOME PAGE ----------
@app.route('/')
def index():
    conn = get_db()
    coffees = conn.execute("SELECT * FROM coffee").fetchall()
    conn.close()
    return render_template('index.html', coffees=coffees)

# ---------- VOTE FUNCTION ----------
@app.route('/vote/<int:coffee_id>')
def vote(coffee_id):
    conn = get_db()
    conn.execute(
        "UPDATE coffee SET votes = votes + 1 WHERE id = ?",
        (coffee_id,)
    )
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

# ---------- MAIN ----------
if __name__ == '__main__':
    print("Starting Coffee Rating App...")  # debug check
    init_db()
   app.run(host='0.0.0.0', port=5000)
