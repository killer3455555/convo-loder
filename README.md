# Lucifer Tool - Ultimate Facebook Tools Collection

A comprehensive Flask web application that combines multiple Facebook automation tools with a beautiful, animated interface.

## Features

### 🔐 Secure Login System
- Username: `Lucifer`
- Password: `Lucifer`
- Animated welcome screen with colorful text effects

### 🛠️ Available Tools

1. **Token Checker** - Verify Facebook access tokens and get user information
2. **Post UID Fetcher** - Extract all post UIDs from a Facebook account
3. **Facebook UID Fetcher** - Get group and conversation UIDs from Messenger
4. **Convo Loader** - Send bulk messages to Facebook conversations with multiple tokens
5. **CPU Monitor** - Real-time system performance monitoring with charts

### 📊 System Monitoring
- Real-time CPU and memory usage
- Active users tracking
- Running tasks monitoring
- Server uptime tracking (30-day target)
- Interactive performance charts

### 👨‍💼 Admin Contact
- WhatsApp: +923243037456
- Facebook: https://www.facebook.com/muddassir.OP

## Installation

### Local Development

1. Clone the repository:
```bash
git clone <repository-url>
cd lucifer-tool
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and go to `http://localhost:5000`

### Deployment

#### Render.com
1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Use the following settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT`

#### Heroku
1. Create a new Heroku app
2. Connect to your GitHub repository
3. Deploy from the main branch

#### Other Platforms
The application includes all necessary files for deployment:
- `Procfile` - Process configuration
- `requirements.txt` - Python dependencies
- `runtime.txt` - Python version specification

## File Structure

```
lucifer-tool/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Procfile              # Process configuration
├── runtime.txt           # Python version
├── README.md             # Documentation
├── templates/            # HTML templates
│   ├── login.html
│   ├── welcome.html
│   ├── dashboard.html
│   ├── token_checker.html
│   ├── post_uid_fetcher.html
│   ├── facebook_uid_fetcher.html
│   ├── convo_loader.html
│   └── cpu_monitor.html
└── static/               # Static files
    ├── images/           # Logo and background images
    ├── css/              # Custom stylesheets
    └── js/               # JavaScript files
```

## Usage

### Token Checker
1. Navigate to Token Checker from the dashboard
2. Paste your Facebook access token
3. Click "Check Token" to verify validity

### Post UID Fetcher
1. Go to Post UID Fetcher
2. Enter your Facebook access token
3. Click "Fetch Posts" to get all post UIDs
4. Export results as text file

### Facebook UID Fetcher
1. Access Facebook UID Fetcher
2. Provide your access token
3. Get all group and conversation UIDs
4. Copy individual UIDs or export all

### Convo Loader
1. Choose between single token or multiple tokens from file
2. Enter conversation UID (get from UID Fetcher)
3. Set your name prefix for messages
4. Upload message file (one message per line)
5. Set time interval between messages
6. Start the loading process
7. Save the Task ID to stop later if needed

### CPU Monitor
1. View real-time system statistics
2. Monitor CPU, memory, and disk usage
3. Track active users and running tasks
4. View server uptime progress
5. Enable/disable auto-refresh

## Security Features

- Session-based authentication
- Secure token handling (tokens are not stored)
- Input validation and sanitization
- CSRF protection with secret key

## Performance Features

- Real-time system monitoring
- Auto-refresh capabilities
- Responsive design for all devices
- Optimized for deployment platforms

## Customization

### Changing Login Credentials
Edit the login route in `app.py`:
```python
if username == 'YourUsername' and password == 'YourPassword':
```

### Adding New Tools
1. Create a new route in `app.py`
2. Add corresponding HTML template
3. Update the dashboard with new tool card

### Styling
- Modify CSS in individual HTML templates
- Add custom stylesheets in `static/css/`
- Update color schemes and animations

## Troubleshooting

### Common Issues

1. **Token Invalid Errors**
   - Ensure token has proper permissions
   - Check if token has expired
   - Verify token format

2. **Message Sending Fails**
   - Use appropriate time intervals (5-10 seconds recommended)
   - Check conversation UID format
   - Ensure tokens have messenger permissions

3. **Deployment Issues**
   - Verify all files are included
   - Check Python version compatibility
   - Ensure environment variables are set

### Support

For technical support or questions:
- WhatsApp: +923243037456
- Facebook: https://www.facebook.com/muddassir.OP

## License

This project is for educational purposes only. Use responsibly and in accordance with Facebook's Terms of Service.

## Credits

Developed by Muddassir - Always on Fire 🔥

---

**Note**: This tool is designed for legitimate use cases. Please respect Facebook's rate limits and terms of service when using automation features.
