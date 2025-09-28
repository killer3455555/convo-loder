import psutil
import requests
import time
import json
import os
from datetime import datetime, timedelta
import threading

class SystemMonitor:
    def __init__(self):
        self.monitoring_data = {
            'cpu_history': [],
            'memory_history': [],
            'disk_history': [],
            'network_history': [],
            'uptime_checks': [],
            'health_status': 'healthy',
            'last_check': None
        }
        self.monitoring_file = 'monitoring_data.json'
        self.load_monitoring_data()
        self.start_monitoring()
    
    def load_monitoring_data(self):
        """Load monitoring data from file"""
        if os.path.exists(self.monitoring_file):
            try:
                with open(self.monitoring_file, 'r') as f:
                    saved_data = json.load(f)
                    self.monitoring_data.update(saved_data)
            except:
                pass
    
    def save_monitoring_data(self):
        """Save monitoring data to file"""
        try:
            with open(self.monitoring_file, 'w') as f:
                json.dump(self.monitoring_data, f, indent=2)
        except Exception as e:
            print(f"Error saving monitoring data: {e}")
    
    def get_system_stats(self):
        """Get current system statistics"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Network stats
            network = psutil.net_io_counters()
            
            stats = {
                'timestamp': datetime.now().isoformat(),
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_used_gb': round(memory.used / (1024**3), 2),
                'memory_total_gb': round(memory.total / (1024**3), 2),
                'disk_percent': disk.percent,
                'disk_used_gb': round(disk.used / (1024**3), 2),
                'disk_total_gb': round(disk.total / (1024**3), 2),
                'network_bytes_sent': network.bytes_sent,
                'network_bytes_recv': network.bytes_recv
            }
            
            return stats
        except Exception as e:
            print(f"Error getting system stats: {e}")
            return None
    
    def check_health(self):
        """Check application health"""
        try:
            # Check if the application is responding
            response = requests.get('http://localhost:5000/', timeout=10)
            if response.status_code == 200:
                return 'healthy'
            else:
                return 'unhealthy'
        except:
            return 'down'
    
    def perform_uptime_check(self):
        """Perform uptime check"""
        health_status = self.check_health()
        uptime_check = {
            'timestamp': datetime.now().isoformat(),
            'status': health_status,
            'response_time': None
        }
        
        try:
            start_time = time.time()
            response = requests.get('http://localhost:5000/', timeout=10)
            response_time = round((time.time() - start_time) * 1000, 2)  # in milliseconds
            uptime_check['response_time'] = response_time
        except:
            pass
        
        self.monitoring_data['uptime_checks'].append(uptime_check)
        self.monitoring_data['health_status'] = health_status
        self.monitoring_data['last_check'] = datetime.now().isoformat()
        
        # Keep only last 1000 checks
        if len(self.monitoring_data['uptime_checks']) > 1000:
            self.monitoring_data['uptime_checks'] = self.monitoring_data['uptime_checks'][-1000:]
        
        return uptime_check
    
    def collect_system_metrics(self):
        """Collect and store system metrics"""
        stats = self.get_system_stats()
        if stats:
            self.monitoring_data['cpu_history'].append({
                'timestamp': stats['timestamp'],
                'value': stats['cpu_percent']
            })
            
            self.monitoring_data['memory_history'].append({
                'timestamp': stats['timestamp'],
                'value': stats['memory_percent']
            })
            
            self.monitoring_data['disk_history'].append({
                'timestamp': stats['timestamp'],
                'value': stats['disk_percent']
            })
            
            # Keep only last 1000 entries for each metric
            for metric in ['cpu_history', 'memory_history', 'disk_history']:
                if len(self.monitoring_data[metric]) > 1000:
                    self.monitoring_data[metric] = self.monitoring_data[metric][-1000:]
        
        return stats
    
    def get_uptime_percentage(self, hours=24):
        """Calculate uptime percentage for the last N hours"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_checks = [
            check for check in self.monitoring_data['uptime_checks']
            if datetime.fromisoformat(check['timestamp']) > cutoff_time
        ]
        
        if not recent_checks:
            return 100.0
        
        healthy_checks = len([check for check in recent_checks if check['status'] == 'healthy'])
        return round((healthy_checks / len(recent_checks)) * 100, 2)
    
    def get_monitoring_summary(self):
        """Get monitoring summary"""
        current_stats = self.get_system_stats()
        uptime_24h = self.get_uptime_percentage(24)
        uptime_7d = self.get_uptime_percentage(24 * 7)
        
        # Get average response time from recent checks
        recent_checks = self.monitoring_data['uptime_checks'][-100:]  # Last 100 checks
        response_times = [check['response_time'] for check in recent_checks if check['response_time']]
        avg_response_time = round(sum(response_times) / len(response_times), 2) if response_times else 0
        
        return {
            'current_stats': current_stats,
            'health_status': self.monitoring_data['health_status'],
            'last_check': self.monitoring_data['last_check'],
            'uptime_24h': uptime_24h,
            'uptime_7d': uptime_7d,
            'avg_response_time': avg_response_time,
            'total_checks': len(self.monitoring_data['uptime_checks']),
            'cpu_trend': self.get_trend('cpu_history'),
            'memory_trend': self.get_trend('memory_history'),
            'disk_trend': self.get_trend('disk_history')
        }
    
    def get_trend(self, metric_name, hours=1):
        """Get trend for a metric over the last hour"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_data = [
            item for item in self.monitoring_data[metric_name]
            if datetime.fromisoformat(item['timestamp']) > cutoff_time
        ]
        
        if len(recent_data) < 2:
            return 'stable'
        
        values = [item['value'] for item in recent_data]
        first_half = values[:len(values)//2]
        second_half = values[len(values)//2:]
        
        avg_first = sum(first_half) / len(first_half)
        avg_second = sum(second_half) / len(second_half)
        
        diff = avg_second - avg_first
        if diff > 5:
            return 'increasing'
        elif diff < -5:
            return 'decreasing'
        else:
            return 'stable'
    
    def monitoring_loop(self):
        """Main monitoring loop"""
        while True:
            try:
                # Collect system metrics every 5 minutes
                self.collect_system_metrics()
                
                # Perform uptime check every 2 minutes
                self.perform_uptime_check()
                
                # Save data
                self.save_monitoring_data()
                
                # Sleep for 2 minutes
                time.sleep(120)
                
            except Exception as e:
                print(f"Error in monitoring loop: {e}")
                time.sleep(60)  # Wait 1 minute before retrying
    
    def start_monitoring(self):
        """Start monitoring in background thread"""
        monitor_thread = threading.Thread(target=self.monitoring_loop, daemon=True)
        monitor_thread.start()
        print("System monitoring started")

# Global monitor instance
system_monitor = SystemMonitor()
