from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import MySQLdb.cursors
import re
from functools import wraps

app = Flask(__name__)
app.secret_key = 'super_secret_key'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'quoramysql'  
app.config['MYSQL_DB'] = 'quora_clone'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
bcrypt = Bcrypt(app)

# Login Required Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    return redirect(url_for('feed'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        # Basic validation
        if not username or not email or not password:
            flash('Please fill out all fields.', 'error')
            return redirect(url_for('signup'))

        if len(username) < 3:
            flash('Username must be at least 3 characters.', 'error')
            return redirect(url_for('signup'))    

        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'error')
            return redirect(url_for('signup'))    
        
        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('signup'))

# Check password length
        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'error')
            return redirect(url_for('signup'))
            

        cursor = mysql.connection.cursor()
        try:
            cursor.execute(
    "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
    (username, email, password)
)
            mysql.connection.commit()
            flash('Account created successfully! Please login.', 'success')
            return redirect(url_for('login'))
        except MySQLdb.Error as e:
            flash(f'Error: {e}', 'error')
        finally:
            cursor.close()
            
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        
        if user and user['password_hash'] == password:
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash(f'Welcome back, {user["username"]}!', 'success')
            return redirect(url_for('feed'))
        else:
            flash('Invalid email or password.', 'error')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/feed')
@login_required
def feed():
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT q.*, u.username 
        FROM questions q 
        JOIN users u ON q.user_id = u.id 
        ORDER BY q.created_at DESC
    """)
    questions = cursor.fetchall()
    cursor.close()
    return render_template('feed.html', questions=questions)

@app.route('/ask', methods=['GET', 'POST'])
@login_required
def ask_question():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        
        if not title:
            flash('Question title is required.', 'error')
            return redirect(url_for('ask_question'))
            
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO questions (user_id, title, body) VALUES (%s, %s, %s)", 
                       (session['user_id'], title, body))
        mysql.connection.commit()
        cursor.close()
        flash('Question posted successfully!', 'success')
        return redirect(url_for('feed'))
        
    return render_template('ask.html')

@app.route('/question/<int:question_id>', methods=['GET', 'POST'])
@login_required
def view_question(question_id):
    cursor = mysql.connection.cursor()
    
    # Post answer logic
    if request.method == 'POST':
        body = request.form['body']
        if not body:
            flash('Answer cannot be empty.', 'error')
        else:
            cursor.execute("INSERT INTO answers (question_id, user_id, body) VALUES (%s, %s, %s)", 
                           (question_id, session['user_id'], body))
            mysql.connection.commit()
            flash('Answer posted!', 'success')
            return redirect(url_for('view_question', question_id=question_id))
            
    # Fetch question
    cursor.execute("""
        SELECT q.*, u.username 
        FROM questions q 
        JOIN users u ON q.user_id = u.id 
        WHERE q.id = %s
    """, (question_id,))
    question = cursor.fetchone()
    
    if not question:
        flash('Question not found.', 'error')
        return redirect(url_for('feed'))
        
    # Fetch answers
    cursor.execute("""
        SELECT a.*, u.username 
        FROM answers a 
        JOIN users u ON a.user_id = u.id 
        WHERE a.question_id = %s 
        ORDER BY a.created_at DESC
    """, (question_id,))
    answers = cursor.fetchall()
    
    cursor.close()
    return render_template('question.html', question=question, answers=answers)

if __name__ == '__main__':
    app.run(debug=True)
