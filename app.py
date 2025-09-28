from flask import Flask, request, render_template, redirect, url_for, session, jsonify, flash
import requests
from threading import Thread, Event
import time
import random
import string
import os
import psutil
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'lucifer_secret_key_2025'
app.debug = True

# Global variables for task management
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
active_users = set()

# Admin contact info
ADMIN_WHATSAPP = "+923243037456"
ADMIN_FACEBOOK = "https://www.facebook.com/muddassir.OP"

def send_messages(access_tokens, thread_id, mn, time_interval, messages, task_id):
    """Function to send messages in a thread"""
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
                    print(f"Message Sent Successfully From token {access_token}: {message}")
                else:
                    print(f"Message Sent Failed From token {access_token}: {message}")
                time.sleep(time_interval)

@app.route('/')
def index():
    """Landing page with login"""
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    """Handle login authentication"""
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username == 'Lucifer' and password == 'Lucifer':
        session['logged_in'] = True
        session['username'] = username
        active_users.add(session.get('_id', 'anonymous'))
        return redirect(url_for('welcome'))
    else:
        flash('Invalid credentials! Use Username: Lucifer, Password: Lucifer')
        return redirect(url_for('index'))

@app.route('/welcome')
def welcome():
    """Welcome page with animation"""
    if 'logged_in' not in session:
        return redirect(url_for('index'))
    return render_template('welcome.html')

@app.route('/dashboard')
def dashboard():
    """Main dashboard with all tools"""
    if 'logged_in' not in session:
        return redirect(url_for('index'))
    return render_template('dashboard.html', 
                         admin_whatsapp=ADMIN_WHATSAPP, 
                         admin_facebook=ADMIN_FACEBOOK)

@app.route('/token-checker', methods=['GET', 'POST'])
def token_checker():
    """Token validation tool"""
    if 'logged_in' not in session:
        return redirect(url_for('index'))
    
    result = None
    if request.method == 'POST':
        token = request.form.get('token')
        try:
            url = f"https://graph.facebook.com/v15.0/me?access_token={token}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                result = {
                    'status': 'valid',
                    'name': data.get('name', 'Unknown'),
                    'id': data.get('id', 'Unknown')
                }
            else:
                result = {'status': 'invalid', 'error': 'Token is invalid or expired'}
        except Exception as e:
            result = {'status': 'error', 'error': str(e)}
    
    return render_template('token_checker.html', result=result)

@app.route('/post-uid-fetcher', methods=['GET', 'POST'])
def post_uid_fetcher():
    """Fetch all posts UIDs for a given token"""
    if 'logged_in' not in session:
        return redirect(url_for('index'))
    
    posts = []
    if request.method == 'POST':
        token = request.form.get('token')
        try:
            url = f"https://graph.facebook.com/v15.0/me/posts?fields=id,message,created_time&access_token={token}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                posts = data.get('data', [])
            else:
                flash('Failed to fetch posts. Check your token.')
        except Exception as e:
            flash(f'Error: {str(e)}')
    
    return render_template('post_uid_fetcher.html', posts=posts)

@app.route('/facebook-uid-fetcher', methods=['GET', 'POST'])
def facebook_uid_fetcher():
    """Fetch Facebook group UIDs"""
    if 'logged_in' not in session:
        return redirect(url_for('index'))
    
    groups = []
    if request.method == 'POST':
        token = request.form.get('token')
        try:
            url = f"https://graph.facebook.com/v15.0/me/conversations?fields=id,name&access_token={token}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                groups = data.get('data', [])
            else:
                error_msg = response.json().get('error', {}).get('message', 'Invalid Token')
                groups = [{"name": "❌ Error", "id": error_msg}]
        except Exception as e:
            groups = [{"name": "❌ Exception", "id": str(e)}]
    
    return render_template('facebook_uid_fetcher.html', groups=groups)

@app.route('/convo-loader', methods=['GET', 'POST'])
def convo_loader():
    """Multi-token conversation loader"""
    if 'logged_in' not in session:
        return redirect(url_for('index'))
    
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

        task_id = ''.join(random.choices(string.ascii_letters + string.digits, k=20))

        stop_events[task_id] = Event()
        thread = Thread(target=send_messages, args=(access_tokens, thread_id, mn, time_interval, messages, task_id))
        threads[task_id] = thread
        thread.start()

        flash(f'Task started with ID: {task_id}')
        return redirect(url_for('convo_loader'))
    
    return render_template('convo_loader.html')

@app.route('/stop-task', methods=['POST'])
def stop_task():
    """Stop a running task"""
    if 'logged_in' not in session:
        return redirect(url_for('index'))
    
    task_id = request.form.get('taskId')
    if task_id in stop_events:
        stop_events[task_id].set()
        flash(f'Task with ID {task_id} has been stopped.')
    else:
        flash(f'No task found with ID {task_id}.')
    
    return redirect(url_for('convo_loader'))

@app.route('/cpu-monitor')
def cpu_monitor():
    """CPU and system monitoring"""
    if 'logged_in' not in session:
        return redirect(url_for('index'))
    
    # Get system information
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    # Get uptime
    boot_time = psutil.boot_time()
    uptime = datetime.now() - datetime.fromtimestamp(boot_time)
    
    system_info = {
        'cpu_percent': cpu_percent,
        'memory_percent': memory.percent,
        'memory_used': round(memory.used / (1024**3), 2),  # GB
        'memory_total': round(memory.total / (1024**3), 2),  # GB
        'disk_percent': disk.percent,
        'disk_used': round(disk.used / (1024**3), 2),  # GB
        'disk_total': round(disk.total / (1024**3), 2),  # GB
        'uptime_days': uptime.days,
        'uptime_hours': uptime.seconds // 3600,
        'uptime_minutes': (uptime.seconds % 3600) // 60,
        'active_users': len(active_users),
        'running_tasks': len([t for t in threads.values() if t.is_alive()])
    }
    
    return render_template('cpu_monitor.html', system_info=system_info)

@app.route('/api/system-stats')
def api_system_stats():
    """API endpoint for real-time system stats"""
    if 'logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    cpu_percent = psutil.cpu_percent(interval=0.1)
    memory = psutil.virtual_memory()
    
    return jsonify({
        'cpu': cpu_percent,
        'memory': memory.percent,
        'active_users': len(active_users),
        'running_tasks': len([t for t in threads.values() if t.is_alive()])
    })

@app.route('/logout')
def logout():
    """Logout user"""
    if '_id' in session:
        active_users.discard(session.get('_id', 'anonymous'))
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
