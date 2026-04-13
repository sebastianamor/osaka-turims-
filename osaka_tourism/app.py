from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import sqlite3
import hashlib
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = 'osaka_tourism_secret_2024'

DB_PATH = 'osaka.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        language TEXT DEFAULT 'en',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS favorites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        place_id TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        place_id TEXT,
        rating INTEGER,
        comment TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = hash_password(request.form['password'])
        language = request.form.get('language', 'en')
        try:
            conn = get_db()
            conn.execute('INSERT INTO users (username, email, password, language) VALUES (?, ?, ?, ?)',
                         (username, email, password, language))
            conn.commit()
            conn.close()
            flash('registration_success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('user_exists')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = hash_password(request.form['password'])
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE username=? AND password=?',
                            (username, password)).fetchone()
        conn.close()
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['language'] = user['language']
            return redirect(url_for('explore'))
        flash('invalid_credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/explore')
@login_required
def explore():
    return render_template('explore.html', username=session['username'])

@app.route('/transport')
@login_required
def transport():
    return render_template('transport.html')

@app.route('/history')
@login_required
def history():
    return render_template('history.html')

@app.route('/api/favorites', methods=['GET', 'POST', 'DELETE'])
@login_required
def favorites():
    conn = get_db()
    if request.method == 'GET':
        favs = conn.execute('SELECT place_id FROM favorites WHERE user_id=?',
                            (session['user_id'],)).fetchall()
        conn.close()
        return jsonify([f['place_id'] for f in favs])
    elif request.method == 'POST':
        place_id = request.json.get('place_id')
        existing = conn.execute('SELECT id FROM favorites WHERE user_id=? AND place_id=?',
                                (session['user_id'], place_id)).fetchone()
        if not existing:
            conn.execute('INSERT INTO favorites (user_id, place_id) VALUES (?, ?)',
                         (session['user_id'], place_id))
            conn.commit()
        conn.close()
        return jsonify({'status': 'ok'})
    elif request.method == 'DELETE':
        place_id = request.json.get('place_id')
        conn.execute('DELETE FROM favorites WHERE user_id=? AND place_id=?',
                     (session['user_id'], place_id))
        conn.commit()
        conn.close()
        return jsonify({'status': 'ok'})

@app.route('/api/reviews', methods=['GET', 'POST'])
@login_required
def reviews():
    conn = get_db()
    if request.method == 'GET':
        place_id = request.args.get('place_id')
        reviews = conn.execute(
            '''SELECT r.*, u.username FROM reviews r
               JOIN users u ON r.user_id = u.id
               WHERE r.place_id=? ORDER BY r.created_at DESC''',
            (place_id,)).fetchall()
        conn.close()
        return jsonify([dict(r) for r in reviews])
    elif request.method == 'POST':
        data = request.json
        conn.execute('INSERT INTO reviews (user_id, place_id, rating, comment) VALUES (?, ?, ?, ?)',
                     (session['user_id'], data['place_id'], data['rating'], data['comment']))
        conn.commit()
        conn.close()
        return jsonify({'status': 'ok'})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
