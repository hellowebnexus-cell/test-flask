from flask import Flask, render_template, jsonify, request
import random
import string
import sqlite3
import os

app = Flask(__name__)
DATABASE = 'nexus.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS saved_strings (id INTEGER PRIMARY KEY AUTOINCREMENT, result TEXT NOT NULL, created_at DATETIME DEFAULT CURRENT_TIMESTAMP)')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate')
def generate_random():
    length = 16
    # Avoid visually similar characters for better readability
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    random_string = ''.join(random.choice(characters) for i in range(length))
    return jsonify({'result': random_string})

@app.route('/save', methods=['POST'])
def save_string():
    data = request.get_json()
    result = data.get('result')
    if result:
        conn = get_db_connection()
        conn.execute('INSERT INTO saved_strings (result) VALUES (?)', (result,))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': 'No result provided'}), 400

@app.route('/history', methods=['GET'])
def get_history():
    conn = get_db_connection()
    rows = conn.execute('SELECT id, result, created_at FROM saved_strings ORDER BY id DESC LIMIT 10').fetchall()
    conn.close()
    return jsonify({'history': [dict(ix) for ix in rows]})

if __name__ == '__main__':
    app.run(debug=True,port=5000)
