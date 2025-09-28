<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Convo Loader - Lucifer Tool</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        body {
            background: linear-gradient(-45deg, #0f0f23, #1a1a2e, #16213e, #0f0f23);
            background-size: 400% 400%;
            animation: gradientBG 15s ease infinite;
            min-height: 100vh;
            color: white;
            font-family: 'Arial', sans-serif;
        }

        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .container {
            max-width: 800px;
            margin-top: 50px;
        }

        .tool-header {
            text-align: center;
            margin-bottom: 40px;
        }

        .tool-title {
            font-size: 2.5rem;
            font-weight: bold;
            color: #ff6b6b;
            margin-bottom: 10px;
        }

        .tool-description {
            color: rgba(255, 255, 255, 0.8);
            font-size: 1.1rem;
        }

        .form-card {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 40px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            margin-bottom: 30px;
        }

        .form-control, .form-select {
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 10px;
            color: white;
            padding: 15px;
            margin-bottom: 20px;
        }

        .form-control:focus, .form-select:focus {
            background: rgba(255, 255, 255, 0.2);
            border-color: #ff6b6b;
            box-shadow: 0 0 20px rgba(255, 107, 107, 0.3);
            color: white;
        }

        .form-control::placeholder {
            color: rgba(255, 255, 255, 0.7);
        }

        .form-select option {
            background: #1a1a2e;
            color: white;
        }

        .btn-start {
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
            border: none;
            border-radius: 10px;
            padding: 15px 40px;
            font-weight: bold;
            font-size: 1.1rem;
            width: 100%;
            transition: all 0.3s ease;
            margin-bottom: 20px;
        }

        .btn-start:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(255, 107, 107, 0.4);
        }

        .btn-stop {
            background: linear-gradient(45deg, #dc3545, #c82333);
            border: none;
            border-radius: 10px;
            padding: 15px 40px;
            font-weight: bold;
            font-size: 1.1rem;
            width: 100%;
            transition: all 0.3s ease;
        }

        .btn-stop:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(220, 53, 69, 0.4);
        }

        .back-btn {
            background: rgba(108, 117, 125, 0.8);
            border: none;
            border-radius: 10px;
            padding: 10px 20px;
            color: white;
            text-decoration: none;
            display: inline-block;
            margin-bottom: 20px;
            transition: all 0.3s ease;
        }

        .back-btn:hover {
            background: rgba(108, 117, 125, 1);
            color: white;
            text-decoration: none;
        }

        .alert {
            border-radius: 10px;
            border: none;
            backdrop-filter: blur(10px);
        }

        .alert-success {
            background: rgba(40, 167, 69, 0.2);
            color: #28a745;
            border: 1px solid rgba(40, 167, 69, 0.3);
        }

        .alert-danger {
            background: rgba(220, 53, 69, 0.2);
            color: #dc3545;
            border: 1px solid rgba(220, 53, 69, 0.3);
        }

        .token-input-section {
            display: none;
        }

        .token-input-section.active {
            display: block;
        }

        .info-card {
            background: rgba(23, 162, 184, 0.1);
            border: 1px solid rgba(23, 162, 184, 0.3);
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }

        .info-title {
            color: #17a2b8;
            font-weight: bold;
            margin-bottom: 10px;
        }

        .file-input {
            position: relative;
            overflow: hidden;
            display: inline-block;
            width: 100%;
        }

        .file-input input[type=file] {
            position: absolute;
            left: -9999px;
        }

        .file-input-label {
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 10px;
            padding: 15px;
            display: block;
            cursor: pointer;
            transition: all 0.3s ease;
            text-align: center;
        }

        .file-input-label:hover {
            background: rgba(255, 255, 255, 0.2);
            border-color: #ff6b6b;
        }

        .stop-section {
            background: rgba(220, 53, 69, 0.1);
            border: 1px solid rgba(220, 53, 69, 0.3);
            border-radius: 20px;
            padding: 30px;
            margin-top: 30px;
        }

        .stop-title {
            color: #dc3545;
            font-weight: bold;
            font-size: 1.3rem;
            margin-bottom: 20px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <a href="{{ url_for('dashboard') }}" class="back-btn">
            <i class="fas fa-arrow-left me-2"></i>Back to Dashboard
        </a>

        <div class="tool-header">
            <h1 class="tool-title">
                <i class="fas fa-comments me-3"></i>Convo Loader
            </h1>
            <p class="tool-description">
                Send bulk messages to Facebook conversations with multiple tokens
            </p>
        </div>

        {% with messages = get_flashed_messages() %}
            {% if messages %}
                <div class="alert {% if 'stopped' in messages[0] or 'started' in messages[0] %}alert-success{% else %}alert-danger{% endif %}">
                    <i class="fas fa-info-circle me-2"></i>{{ messages[0] }}
                </div>
            {% endif %}
        {% endwith %}

        <div class="form-card">
            <form method="POST" enctype="multipart/form-data">
                <div class="mb-3">
                    <label for="tokenOption" class="form-label">
                        <i class="fas fa-cog me-2"></i>Token Option
                    </label>
                    <select class="form-select" id="tokenOption" name="tokenOption" onchange="toggleTokenInput()" required>
                        <option value="single">Single Token</option>
                        <option value="multiple">Multiple Tokens (File)</option>
                    </select>
                </div>

                <div class="token-input-section active" id="singleTokenInput">
                    <div class="mb-3">
                        <label for="singleToken" class="form-label">
                            <i class="fas fa-key me-2"></i>Enter Single Token
                        </label>
                        <textarea class="form-control" id="singleToken" name="singleToken" rows="3" 
                                  placeholder="Paste your Facebook access token here..."></textarea>
                    </div>
                </div>

                <div class="token-input-section" id="tokenFileInput">
                    <div class="mb-3">
                        <label class="form-label">
                            <i class="fas fa-file-upload me-2"></i>Choose Token File
                        </label>
                        <div class="file-input">
                            <input type="file" id="tokenFile" name="tokenFile" accept=".txt">
                            <label for="tokenFile" class="file-input-label">
                                <i class="fas fa-cloud-upload-alt me-2"></i>
                                <span id="tokenFileName">Click to select token file (.txt)</span>
                            </label>
                        </div>
                        <small class="text-muted">
                            <i class="fas fa-info-circle me-1"></i>
                            Upload a .txt file with one token per line
                        </small>
                    </div>
                </div>

                <div class="mb-3">
                    <label for="threadId" class="form-label">
                        <i class="fas fa-hashtag me-2"></i>Enter Inbox/Convo UID
                    </label>
                    <input type="text" class="form-control" id="threadId" name="threadId" 
                           placeholder="Enter conversation/inbox UID here..." required>
                    <small class="text-muted">
                        <i class="fas fa-lightbulb me-1"></i>
                        Use the UID Fetcher tool to get conversation UIDs
                    </small>
                </div>

                <div class="mb-3">
                    <label for="kidx" class="form-label">
                        <i class="fas fa-user me-2"></i>Enter Your Hater Name
                    </label>
                    <input type="text" class="form-control" id="kidx" name="kidx" 
                           placeholder="Enter your name/prefix for messages..." required>
                </div>

                <div class="mb-3">
                    <label for="time" class="form-label">
                        <i class="fas fa-clock me-2"></i>Enter Time Interval (seconds)
                    </label>
                    <input type="number" class="form-control" id="time" name="time" 
                           placeholder="Time between messages in seconds..." min="1" required>
                    <small class="text-muted">
                        <i class="fas fa-exclamation-triangle me-1"></i>
                        Recommended: 5-10 seconds to avoid being blocked
                    </small>
                </div>

                <div class="mb-3">
                    <label class="form-label">
                        <i class="fas fa-file-alt me-2"></i>Choose Your Message File
                    </label>
                    <div class="file-input">
                        <input type="file" id="txtFile" name="txtFile" accept=".txt" required>
                        <label for="txtFile" class="file-input-label">
                            <i class="fas fa-file-upload me-2"></i>
                            <span id="txtFileName">Click to select message file (.txt)</span>
                        </label>
                    </div>
                    <small class="text-muted">
                        <i class="fas fa-info-circle me-1"></i>
                        Upload a .txt file with one message per line
                    </small>
                </div>

                <button type="submit" class="btn btn-start">
                    <i class="fas fa-rocket me-2"></i>Start Message Loading
                </button>
            </form>
        </div>

        <div class="info-card">
            <div class="info-title">
                <i class="fas fa-info-circle me-2"></i>How to Use:
            </div>
            <ul class="mb-0">
                <li>Choose between single token or multiple tokens from file</li>
                <li>Get conversation UID using the UID Fetcher tool</li>
                <li>Upload a text file with your messages (one per line)</li>
                <li>Set appropriate time interval to avoid being blocked</li>
                <li>Save the Task ID to stop the process later</li>
            </ul>
        </div>

        <div class="stop-section">
            <div class="stop-title">
                <i class="fas fa-stop-circle me-2"></i>Stop Running Task
            </div>
            <form method="POST" action="{{ url_for('stop_task') }}">
                <div class="mb-3">
                    <label for="taskId" class="form-label">
                        <i class="fas fa-id-badge me-2"></i>Enter Task ID to Stop
                    </label>
                    <input type="text" class="form-control" id="taskId" name="taskId" 
                           placeholder="Enter the task ID you want to stop..." required>
                </div>
                <button type="submit" class="btn btn-stop">
                    <i class="fas fa-stop me-2"></i>Stop Task
                </button>
            </form>
        </div>
    </div>

    <script>
        function toggleTokenInput() {
            const tokenOption = document.getElementById('tokenOption').value;
            const singleInput = document.getElementById('singleTokenInput');
            const fileInput = document.getElementById('tokenFileInput');
            
            if (tokenOption === 'single') {
                singleInput.classList.add('active');
                fileInput.classList.remove('active');
            } else {
                singleInput.classList.remove('active');
                fileInput.classList.add('active');
            }
        }

        // File input handlers
        document.getElementById('tokenFile').addEventListener('change', function() {
            const fileName = this.files[0] ? this.files[0].name : 'Click to select token file (.txt)';
            document.getElementById('tokenFileName').textContent = fileName;
        });

        document.getElementById('txtFile').addEventListener('change', function() {
            const fileName = this.files[0] ? this.files[0].name : 'Click to select message file (.txt)';
            document.getElementById('txtFileName').textContent = fileName;
        });

        // Form validation
        document.querySelector('form').addEventListener('submit', function(e) {
            const tokenOption = document.getElementById('tokenOption').value;
            const singleToken = document.getElementById('singleToken').value.trim();
            const tokenFile = document.getElementById('tokenFile').files[0];
            
            if (tokenOption === 'single' && !singleToken) {
                e.preventDefault();
                alert('Please enter a single token or switch to file option.');
                return;
            }
            
            if (tokenOption === 'multiple' && !tokenFile) {
                e.preventDefault();
                alert('Please select a token file or switch to single token option.');
                return;
            }
        });
    </script>
</body>
</html>
