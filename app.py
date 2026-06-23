"""
Vulnerable Web Application for Security Testing
WARNING: This application contains intentional security vulnerabilities.
DO NOT deploy in production. For educational and testing purposes only.
"""

import os
import sqlite3
import subprocess
import pickle
import base64
import hashlib
import requests
from flask import Flask, request, render_template, redirect, url_for, session, make_response, jsonify
from functools import wraps

app = Flask(__name__)

# VULNERABILITY: Hardcoded secret key (weak and predictable)
app.secret_key = 'super_secret_key_123'

# VULNERABILITY: Hardcoded credentials
DATABASE_USER = "admin"
DATABASE_PASSWORD = "admin123"
ADMIN_PASSWORD = "password123"

# VULNERABILITY: Hardcoded API keys
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
GITHUB_TOKEN = "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
STRIPE_API_KEY = "sk_live_xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
SENDGRID_API_KEY = "SG.xxxxxxxxxxxxxxxxxxxxxx.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# VULNERABILITY: Debug mode enabled in production
DEBUG_MODE = True

def init_db():
    """Initialize SQLite database with sample data"""
    conn = sqlite3.connect('vulnerable.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            role TEXT DEFAULT 'user',
            credit_card TEXT
        )
    ''')
    
    # Create products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL,
            description TEXT
        )
    ''')
    
    # Create comments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert sample data with sensitive information
    cursor.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'admin123', 'admin@vulnerable.com', 'admin', '4111-1111-1111-1111')")
    cursor.execute("INSERT OR IGNORE INTO users VALUES (2, 'john', 'john123', 'john@example.com', 'user', '4222-2222-2222-2222')")
    cursor.execute("INSERT OR IGNORE INTO users VALUES (3, 'jane', 'jane123', 'jane@example.com', 'user', '4333-3333-3333-3333')")
    
    cursor.execute("INSERT OR IGNORE INTO products VALUES (1, 'Laptop', 999.99, 'High-performance laptop')")
    cursor.execute("INSERT OR IGNORE INTO products VALUES (2, 'Phone', 599.99, 'Latest smartphone')")
    
    conn.commit()
    conn.close()

init_db()

# ==================== HOME PAGE ====================
@app.route('/')
def index():
    return render_template('index.html')

# ==================== SQL INJECTION ====================
@app.route('/sql-injection', methods=['GET', 'POST'])
def sql_injection():
    results = []
    error = None
    
    if request.method == 'POST':
        username = request.form.get('username', '')
        
        # VULNERABILITY: SQL Injection - Direct string concatenation
        conn = sqlite3.connect('vulnerable.db')
        cursor = conn.cursor()
        
        try:
            # Vulnerable query - DO NOT USE IN PRODUCTION
            query = f"SELECT * FROM users WHERE username = '{username}'"
            cursor.execute(query)
            results = cursor.fetchall()
        except Exception as e:
            error = str(e)
        
        conn.close()
    
    return render_template('sql_injection.html', results=results, error=error)

# ==================== XSS (Cross-Site Scripting) ====================
@app.route('/xss', methods=['GET', 'POST'])
def xss():
    comments = []
    
    conn = sqlite3.connect('vulnerable.db')
    cursor = conn.cursor()
    
    if request.method == 'POST':
        comment = request.form.get('comment', '')
        # VULNERABILITY: Stored XSS - No input sanitization
        cursor.execute(f"INSERT INTO comments (user_id, content) VALUES (1, '{comment}')")
        conn.commit()
    
    cursor.execute("SELECT * FROM comments ORDER BY id DESC")
    comments = cursor.fetchall()
    conn.close()
    
    # VULNERABILITY: Reflected XSS via GET parameter
    search = request.args.get('search', '')
    
    return render_template('xss.html', comments=comments, search=search)

# ==================== COMMAND INJECTION ====================
@app.route('/command-injection', methods=['GET', 'POST'])
def command_injection():
    output = ""
    
    if request.method == 'POST':
        hostname = request.form.get('hostname', '')
        
        # VULNERABILITY: Command Injection - Direct shell execution
        try:
            # Vulnerable: user input passed directly to shell
            output = subprocess.check_output(f"ping -c 2 {hostname}", shell=True, stderr=subprocess.STDOUT)
            output = output.decode('utf-8')
        except subprocess.CalledProcessError as e:
            output = e.output.decode('utf-8')
        except Exception as e:
            output = str(e)
    
    return render_template('command_injection.html', output=output)

# ==================== REMOTE CODE EXECUTION ====================
@app.route('/rce', methods=['GET', 'POST'])
def remote_code_execution():
    result = ""
    
    if request.method == 'POST':
        code = request.form.get('code', '')
        
        # VULNERABILITY: Remote Code Execution - Using eval()
        try:
            result = eval(code)
        except Exception as e:
            result = str(e)
    
    return render_template('rce.html', result=result)

# VULNERABILITY: Insecure deserialization
@app.route('/deserialize', methods=['POST'])
def deserialize():
    data = request.form.get('data', '')
    try:
        # VULNERABILITY: Pickle deserialization of untrusted data
        decoded = base64.b64decode(data)
        obj = pickle.loads(decoded)
        return jsonify({"result": str(obj)})
    except Exception as e:
        return jsonify({"error": str(e)})

# ==================== REMOTE FILE INCLUSION ====================
@app.route('/rfi', methods=['GET', 'POST'])
def remote_file_inclusion():
    content = ""
    
    if request.method == 'POST' or request.args.get('file'):
        file_url = request.form.get('file') or request.args.get('file', '')
        
        # VULNERABILITY: Remote File Inclusion - Fetching arbitrary URLs
        try:
            response = requests.get(file_url, timeout=10)
            content = response.text
        except Exception as e:
            content = str(e)
    
    return render_template('rfi.html', content=content)

# VULNERABILITY: Local File Inclusion
@app.route('/lfi')
def local_file_inclusion():
    filename = request.args.get('file', 'default.txt')
    
    # VULNERABILITY: Path traversal - No validation
    try:
        with open(filename, 'r') as f:
            content = f.read()
    except Exception as e:
        content = str(e)
    
    return render_template('lfi.html', content=content)

# ==================== CSRF (Cross-Site Request Forgery) ====================
@app.route('/csrf', methods=['GET', 'POST'])
def csrf():
    message = ""
    
    if request.method == 'POST':
        # VULNERABILITY: No CSRF token validation
        new_email = request.form.get('email', '')
        new_password = request.form.get('password', '')
        
        if new_email or new_password:
            message = f"Settings updated! Email: {new_email}, Password changed: {'Yes' if new_password else 'No'}"
    
    return render_template('csrf.html', message=message)

# VULNERABILITY: Sensitive action without CSRF protection
@app.route('/transfer', methods=['POST'])
def transfer_money():
    amount = request.form.get('amount', 0)
    to_account = request.form.get('to_account', '')
    
    # No CSRF token check - vulnerable to CSRF attacks
    return jsonify({
        "status": "success",
        "message": f"Transferred ${amount} to account {to_account}"
    })

# ==================== CSS INJECTION ====================
@app.route('/css-injection', methods=['GET', 'POST'])
def css_injection():
    custom_css = ""
    
    if request.method == 'POST':
        # VULNERABILITY: CSS Injection - User-controlled CSS
        custom_css = request.form.get('css', '')
    
    # Also check GET parameter
    custom_css = custom_css or request.args.get('css', '')
    
    return render_template('css_injection.html', custom_css=custom_css)

# ==================== INSECURE AUTHENTICATION ====================
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        # VULNERABILITY: SQL Injection in login
        conn = sqlite3.connect('vulnerable.db')
        cursor = conn.cursor()
        
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(query)
        user = cursor.fetchone()
        conn.close()
        
        if user:
            # VULNERABILITY: Storing sensitive data in session without encryption
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['role'] = user[4]
            session['credit_card'] = user[5]  # Storing credit card in session!
            
            # VULNERABILITY: Insecure cookie settings
            response = make_response(redirect(url_for('dashboard')))
            response.set_cookie('user', username)  # No HttpOnly, no Secure flag
            response.set_cookie('auth_token', hashlib.md5(username.encode()).hexdigest())  # Weak hashing
            return response
        else:
            error = "Invalid credentials"
    
    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# ==================== INSECURE DIRECT OBJECT REFERENCE (IDOR) ====================
@app.route('/user/<int:user_id>')
def get_user(user_id):
    # VULNERABILITY: IDOR - No authorization check
    conn = sqlite3.connect('vulnerable.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return jsonify({
            "id": user[0],
            "username": user[1],
            "password": user[2],  # Exposing password!
            "email": user[3],
            "role": user[4],
            "credit_card": user[5]  # Exposing credit card!
        })
    return jsonify({"error": "User not found"}), 404

# ==================== XML EXTERNAL ENTITY (XXE) ====================
@app.route('/xxe', methods=['GET', 'POST'])
def xxe():
    result = ""
    
    if request.method == 'POST':
        xml_data = request.form.get('xml', '')
        
        # VULNERABILITY: XXE - Parsing XML without disabling external entities
        try:
            import xml.etree.ElementTree as ET
            # In a real vulnerable app, you'd use a parser that allows XXE
            root = ET.fromstring(xml_data)
            result = ET.tostring(root, encoding='unicode')
        except Exception as e:
            result = str(e)
    
    return render_template('xxe.html', result=result)

# ==================== SERVER-SIDE TEMPLATE INJECTION (SSTI) ====================
@app.route('/ssti', methods=['GET', 'POST'])
def ssti():
    output = ""
    
    if request.method == 'POST':
        template = request.form.get('template', '')
        
        # VULNERABILITY: SSTI - Rendering user input as template
        from flask import render_template_string
        try:
            output = render_template_string(template)
        except Exception as e:
            output = str(e)
    
    return render_template('ssti.html', output=output)

# ==================== OPEN REDIRECT ====================
@app.route('/redirect')
def open_redirect():
    # VULNERABILITY: Open Redirect - No URL validation
    url = request.args.get('url', '/')
    return redirect(url)

# ==================== INFORMATION DISCLOSURE ====================
@app.route('/debug')
def debug_info():
    # VULNERABILITY: Information disclosure
    return jsonify({
        "database_user": DATABASE_USER,
        "database_password": DATABASE_PASSWORD,
        "aws_key": AWS_ACCESS_KEY,
        "aws_secret": AWS_SECRET_KEY,
        "github_token": GITHUB_TOKEN,
        "debug_mode": DEBUG_MODE,
        "secret_key": app.secret_key,
        "environment": dict(os.environ)  # Exposing all environment variables!
    })

@app.route('/error')
def trigger_error():
    # VULNERABILITY: Detailed error messages
    x = 1 / 0  # This will cause an error with stack trace in debug mode

# ==================== INSECURE FILE UPLOAD ====================
@app.route('/upload', methods=['GET', 'POST'])
def file_upload():
    message = ""
    
    if request.method == 'POST':
        file = request.files.get('file')
        
        if file:
            # VULNERABILITY: No file type validation, no size limit
            # Saving directly to accessible directory
            filename = file.filename  # No sanitization!
            filepath = os.path.join('static/uploads', filename)
            os.makedirs('static/uploads', exist_ok=True)
            file.save(filepath)
            message = f"File uploaded to: /static/uploads/{filename}"
    
    return render_template('upload.html', message=message)

# ==================== WEAK CRYPTOGRAPHY ====================
@app.route('/crypto', methods=['GET', 'POST'])
def weak_crypto():
    result = ""
    
    if request.method == 'POST':
        data = request.form.get('data', '')
        action = request.form.get('action', 'hash')
        
        if action == 'hash':
            # VULNERABILITY: Using MD5 for password hashing
            result = hashlib.md5(data.encode()).hexdigest()
        elif action == 'encode':
            # VULNERABILITY: Base64 is not encryption
            result = base64.b64encode(data.encode()).decode()
    
    return render_template('crypto.html', result=result)

# ==================== MASS ASSIGNMENT ====================
@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ""
    
    if request.method == 'POST':
        # VULNERABILITY: Mass assignment - accepting all form fields
        user_data = dict(request.form)
        
        # User could add role=admin to become admin!
        conn = sqlite3.connect('vulnerable.db')
        cursor = conn.cursor()
        
        username = user_data.get('username', '')
        password = user_data.get('password', '')
        email = user_data.get('email', '')
        role = user_data.get('role', 'user')  # User can control this!
        
        cursor.execute(f"""
            INSERT INTO users (username, password, email, role) 
            VALUES ('{username}', '{password}', '{email}', '{role}')
        """)
        conn.commit()
        conn.close()
        
        message = f"User {username} registered with role: {role}"
    
    return render_template('register.html', message=message)

# ==================== HEADER INJECTION ====================
@app.route('/header-injection')
def header_injection():
    # VULNERABILITY: HTTP Header Injection
    redirect_url = request.args.get('url', '/')
    response = make_response(redirect(redirect_url))
    
    # User-controlled header value
    custom_header = request.args.get('header', '')
    if custom_header:
        response.headers['X-Custom-Header'] = custom_header
    
    return response

# ==================== NOSQL INJECTION (Simulated) ====================
@app.route('/nosql', methods=['GET', 'POST'])
def nosql_injection():
    result = ""
    
    if request.method == 'POST':
        # VULNERABILITY: NoSQL Injection simulation
        query = request.form.get('query', '')
        
        # In MongoDB this would be vulnerable:
        # db.users.find(JSON.parse(query))
        result = f"Query executed: {query}"
    
    return render_template('nosql.html', result=result)

# ==================== API WITHOUT RATE LIMITING ====================
@app.route('/api/search')
def api_search():
    # VULNERABILITY: No rate limiting - susceptible to brute force/DoS
    query = request.args.get('q', '')
    
    conn = sqlite3.connect('vulnerable.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM products WHERE name LIKE '%{query}%'")
    products = cursor.fetchall()
    conn.close()
    
    return jsonify({"products": products})

# ==================== BROKEN ACCESS CONTROL ====================
@app.route('/admin')
def admin_panel():
    # VULNERABILITY: Only client-side check, no server-side authorization
    # The template checks session['role'] but anyone can access this endpoint
    return render_template('admin.html')

@app.route('/admin/delete-user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    # VULNERABILITY: No authorization check
    conn = sqlite3.connect('vulnerable.db')
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM users WHERE id = {user_id}")
    conn.commit()
    conn.close()
    
    return jsonify({"status": "deleted", "user_id": user_id})

# Error handlers that leak information
@app.errorhandler(500)
def internal_error(error):
    # VULNERABILITY: Detailed error information
    return f"<h1>Internal Server Error</h1><pre>{str(error)}</pre>", 500

if __name__ == '__main__':
    # VULNERABILITY: Debug mode enabled, binding to all interfaces
    app.run(host='0.0.0.0', port=5000, debug=True)
