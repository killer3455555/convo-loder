import json
import os
from datetime import datetime, timedelta
import requests

class Analytics:
    def __init__(self):
        self.data_file = 'analytics_data.json'
        self.load_data()
    
    def load_data(self):
        """Load analytics data from file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.data = json.load(f)
            except:
                self.data = self.get_default_data()
        else:
            self.data = self.get_default_data()
    
    def get_default_data(self):
        """Get default analytics data structure"""
        return {
            'total_users': 0,
            'total_messages': 0,
            'total_deployments': 1,
            'active_sessions': {},
            'daily_stats': {},
            'user_activities': [],
            'start_time': datetime.now().isoformat()
        }
    
    def save_data(self):
        """Save analytics data to file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            print(f"Error saving analytics data: {e}")
    
    def track_user_activity(self, user_ip, activity, details=None):
        """Track user activity"""
        activity_data = {
            'timestamp': datetime.now().isoformat(),
            'user_ip': user_ip,
            'activity': activity,
            'details': details or {}
        }
        
        self.data['user_activities'].append(activity_data)
        
        # Keep only last 1000 activities
        if len(self.data['user_activities']) > 1000:
            self.data['user_activities'] = self.data['user_activities'][-1000:]
        
        # Update daily stats
        today = datetime.now().strftime('%Y-%m-%d')
        if today not in self.data['daily_stats']:
            self.data['daily_stats'][today] = {
                'unique_users': set(),
                'total_activities': 0,
                'messages_sent': 0
            }
        
        self.data['daily_stats'][today]['unique_users'].add(user_ip)
        self.data['daily_stats'][today]['total_activities'] += 1
        
        if activity == 'message_sent':
            self.data['daily_stats'][today]['messages_sent'] += 1
            self.data['total_messages'] += 1
        
        # Convert set to list for JSON serialization
        self.data['daily_stats'][today]['unique_users'] = list(self.data['daily_stats'][today]['unique_users'])
        
        self.save_data()
    
    def add_active_session(self, user_ip, session_data):
        """Add active session"""
        self.data['active_sessions'][user_ip] = {
            'start_time': datetime.now().isoformat(),
            'last_activity': datetime.now().isoformat(),
            'session_data': session_data
        }
        self.save_data()
    
    def update_session_activity(self, user_ip):
        """Update last activity for session"""
        if user_ip in self.data['active_sessions']:
            self.data['active_sessions'][user_ip]['last_activity'] = datetime.now().isoformat()
            self.save_data()
    
    def remove_inactive_sessions(self, timeout_minutes=30):
        """Remove inactive sessions"""
        cutoff_time = datetime.now() - timedelta(minutes=timeout_minutes)
        active_sessions = {}
        
        for user_ip, session in self.data['active_sessions'].items():
            last_activity = datetime.fromisoformat(session['last_activity'])
            if last_activity > cutoff_time:
                active_sessions[user_ip] = session
        
        self.data['active_sessions'] = active_sessions
        self.save_data()
    
    def get_stats(self):
        """Get current statistics"""
        self.remove_inactive_sessions()
        
        # Calculate uptime
        start_time = datetime.fromisoformat(self.data['start_time'])
        uptime_seconds = (datetime.now() - start_time).total_seconds()
        uptime_hours = int(uptime_seconds / 3600)
        uptime_minutes = int((uptime_seconds % 3600) / 60)
        
        # Get today's stats
        today = datetime.now().strftime('%Y-%m-%d')
        today_stats = self.data['daily_stats'].get(today, {
            'unique_users': [],
            'total_activities': 0,
            'messages_sent': 0
        })
        
        return {
            'active_users': len(self.data['active_sessions']),
            'total_messages': self.data['total_messages'],
            'total_deployments': self.data['total_deployments'],
            'uptime': f"{uptime_hours}h {uptime_minutes}m",
            'uptime_seconds': int(uptime_seconds),
            'today_unique_users': len(today_stats['unique_users']),
            'today_activities': today_stats['total_activities'],
            'today_messages': today_stats['messages_sent'],
            'recent_activities': self.data['user_activities'][-10:]  # Last 10 activities
        }
    
    def send_admin_notification(self, message, user_info=None):
        """Send notification to admin"""
        try:
            # This would integrate with Facebook Messenger API
            admin_uid = "100017068697026"
            notification_data = {
                'timestamp': datetime.now().isoformat(),
                'message': message,
                'user_info': user_info,
                'admin_uid': admin_uid
            }
            
            # Log the notification (in real implementation, send via Facebook API)
            print(f"Admin Notification: {message}")
            if user_info:
                print(f"User Info: {user_info}")
            
            # Track this as an activity
            self.track_user_activity('system', 'admin_notification', notification_data)
            
        except Exception as e:
            print(f"Failed to send admin notification: {e}")

# Global analytics instance
analytics = Analytics()
