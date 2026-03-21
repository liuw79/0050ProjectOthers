#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Web Server Startup Script
Auto-start local development server for UI preview
Support: Python 3.6+
"""

import http.server
import socketserver
import webbrowser
import os
import sys
import socket
from datetime import datetime

# Configuration
DEFAULT_PORT = 8080
DEFAULT_HOST = 'localhost'
AUTO_OPEN_BROWSER = True

def find_free_port(start_port=DEFAULT_PORT):
    """Find a free port starting from the given port"""
    port = start_port
    while port < start_port + 100:  # Try 100 ports
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((DEFAULT_HOST, port))
                return port
        except OSError:
            port += 1
    return None

def get_project_info():
    """Get project information"""
    files = []
    for file in ['index.html', 'personal-center.html', 'personal-center.css']:
        if os.path.exists(file):
            size = os.path.getsize(file)
            files.append(f"  - {file} ({size} bytes)")
    return files

def print_banner():
    """Print startup banner"""
    print("=" * 60)
    print("🚀 GAOWEI SCHOOL UI PROJECT - DEV SERVER")
    print("=" * 60)
    print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("📁 Project files detected:")
    
    files = get_project_info()
    if files:
        for file_info in files:
            print(file_info)
    else:
        print("  ⚠️  No HTML files found in current directory")
    
    print("=" * 60)

def print_success_info(host, port):
    """Print success information"""
    print(f"✅ Server started successfully!")
    print(f"🌐 Local URL: http://{host}:{port}")
    print(f"📱 Mobile URL: http://{get_local_ip()}:{port} (if on same network)")
    print()
    print("📋 Available pages:")
    print(f"   • Homepage: http://{host}:{port}/")
    print(f"   • Personal Center: http://{host}:{port}/personal-center.html")
    print()
    print("🛠️  Server Controls:")
    print("   • Press Ctrl+C to stop the server")
    if AUTO_OPEN_BROWSER:
        print("   • Browser will open automatically in 2 seconds...")
    print("=" * 60)

def get_local_ip():
    """Get local IP address"""
    try:
        # Connect to a remote address (doesn't actually connect)
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except:
        return "127.0.0.1"

def start_server():
    """Start the web server"""
    # Check if we're in the right directory
    if not os.path.exists('index.html') and not os.path.exists('personal-center.html'):
        print("❌ Error: No HTML files found!")
        print("   Please run this script in the project directory.")
        sys.exit(1)
    
    # Find available port
    port = find_free_port()
    if not port:
        print("❌ Error: Could not find an available port!")
        sys.exit(1)
    
    print_banner()
    
    try:
        # Create HTTP handler
        handler = http.server.SimpleHTTPRequestHandler
        
        # Create server
        with socketserver.TCPServer((DEFAULT_HOST, port), handler) as httpd:
            print_success_info(DEFAULT_HOST, port)
            
            # Auto-open browser
            if AUTO_OPEN_BROWSER:
                import threading
                def open_browser():
                    import time
                    time.sleep(2)  # Wait 2 seconds for server to fully start
                    webbrowser.open(f'http://{DEFAULT_HOST}:{port}')
                
                browser_thread = threading.Thread(target=open_browser)
                browser_thread.daemon = True
                browser_thread.start()
            
            # Start server
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n" + "="*60)
        print("🛑 Server stopped by user (Ctrl+C)")
        print("👋 Thank you for using Gaowei School UI Dev Server!")
        print("="*60)
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("Starting Gaowei School UI Development Server...")
    start_server() 