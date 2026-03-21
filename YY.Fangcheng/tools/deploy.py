#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
房产项目最终稳定部署方案 - Docker Proxy版本
Architecture: Docker Nginx (SSL/443) -> Backend HTTP (9000)
"""

import os
import sys
import logging
import paramiko
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def deploy_docker_https():
    """Deploy stable HTTPS using Docker nginx container"""
    try:
        logger.info("🚀 Starting Docker HTTPS deployment...")
        
        # SSH connection
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect('op.gaowei.com', username='root', 
                   key_filename=os.path.expanduser('~/.ssh/id_rsa'))
        
        logger.info("SSH connected successfully")
        
        # Step 1: Ensure backend HTTP server is running
        logger.info("📦 Step 1: Ensuring backend HTTP server...")
        
        # Check if backend is running
        stdin, stdout, stderr = ssh.exec_command("pgrep -f 'python3.*http.server.*9000'")
        backend_pid = stdout.read().decode().strip()
        
        if not backend_pid:
            logger.info("Starting backend HTTP server...")
            stdin, stdout, stderr = ssh.exec_command("cd /var/www/fangcheng && nohup python3 -m http.server 9000 > /tmp/backend.log 2>&1 & echo $!")
            backend_pid = stdout.read().decode().strip()
            logger.info(f"Backend server started with PID: {backend_pid}")
        else:
            logger.info(f"Backend server already running with PID: {backend_pid}")
        
        # Step 2: Stop old nginx if running
        logger.info("🛑 Step 2: Stopping old nginx...")
        ssh.exec_command("/usr/local/nginx/sbin/nginx -s stop 2>/dev/null || true")
        
        # Step 3: Manage Docker container
        logger.info("🐳 Step 3: Managing Docker container...")
        
        # Check if container exists
        stdin, stdout, stderr = ssh.exec_command("docker ps -a | grep fangcheng_nginx")
        container_exists = stdout.read().decode().strip()
        
        if container_exists:
            logger.info("Removing existing container...")
            ssh.exec_command("docker rm -f fangcheng_nginx")
        
        # Start new container
        logger.info("Starting new Docker container...")
        stdin, stdout, stderr = ssh.exec_command(
            "docker run -d --name fangcheng_nginx --restart unless-stopped "
            "-p 8888:443 "
            "-v /root/cert:/etc/nginx/ssl:ro "
            "-v /opt/fangcheng_nginx.conf:/etc/nginx/nginx.conf:ro "
            "nginx:alpine"
        )
        
        container_id = stdout.read().decode().strip()
        error_msg = stderr.read().decode().strip()
        
        if error_msg and "Error" in error_msg:
            logger.error(f"Failed to start container: {error_msg}")
            return False
        
        logger.info(f"Container started successfully: {container_id[:12]}")
        
        # Step 4: Health checks
        logger.info("🩺 Step 4: Performing health checks...")
        time.sleep(5)  # Wait for container to fully start
        
        # Check backend service
        stdin, stdout, stderr = ssh.exec_command("netstat -tlnp | grep :9000")
        backend_status = stdout.read().decode().strip()
        if backend_status:
            logger.info("✅ Backend HTTP server (9000) is running")
        else:
            logger.warning("⚠️ Backend HTTP server (9000) not detected")
        
        # Check Docker container
        stdin, stdout, stderr = ssh.exec_command("docker ps | grep fangcheng_nginx")
        container_status = stdout.read().decode().strip()
        if container_status:
            logger.info("✅ Docker nginx container is running")
        else:
            logger.warning("⚠️ Docker nginx container not running")
        
        # Check frontend service
        stdin, stdout, stderr = ssh.exec_command("netstat -tlnp | grep :8888")
        frontend_status = stdout.read().decode().strip()
        if frontend_status:
            logger.info("✅ Frontend HTTPS proxy (8888) is running")
        else:
            logger.warning("⚠️ Frontend HTTPS proxy (8888) not detected")
        
        # Test HTTPS access
        logger.info("Testing HTTPS access...")
        stdin, stdout, stderr = ssh.exec_command("curl -I https://localhost:8888 -k 2>/dev/null | head -1")
        https_response = stdout.read().decode().strip()
        if "200 OK" in https_response:
            logger.info("✅ HTTPS access test passed")
        else:
            logger.warning(f"⚠️ HTTPS access test failed: {https_response}")
        
        logger.info("🎉 Docker HTTPS deployment completed!")
        logger.info("📍 Access URL: https://op.gaowei.com:8888")
        logger.info("🏗️ Architecture: Docker Nginx (SSL:443) -> Backend (HTTP:9000)")
        logger.info("🔄 Container auto-restart: enabled")
        
        ssh.close()
        return True
        
    except Exception as e:
        logger.error(f"Docker deployment failed: {e}")
        return False

def show_status():
    """Show deployment status"""
    try:
        logger.info("📊 Checking deployment status...")
        
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect('op.gaowei.com', username='root', 
                   key_filename=os.path.expanduser('~/.ssh/id_rsa'))
        
        # Check Docker container
        stdin, stdout, stderr = ssh.exec_command("docker ps | grep fangcheng")
        container_status = stdout.read().decode().strip()
        if container_status:
            logger.info(f"🐳 Docker container: {container_status}")
        else:
            logger.warning("⚠️ Docker container not running")
        
        # Check backend process
        stdin, stdout, stderr = ssh.exec_command("pgrep -f 'python3.*http.server.*9000'")
        backend_pid = stdout.read().decode().strip()
        if backend_pid:
            logger.info(f"📦 Backend process: PID {backend_pid}")
        else:
            logger.warning("⚠️ Backend process not running")
        
        # Check ports
        stdin, stdout, stderr = ssh.exec_command("netstat -tlnp | grep -E ':(8888|9000)'")
        port_status = stdout.read().decode().strip()
        if port_status:
            logger.info(f"🔌 Port status:\n{port_status}")
        else:
            logger.warning("⚠️ No ports detected")
        
        ssh.close()
        
    except Exception as e:
        logger.error(f"Status check failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "status":
        show_status()
    else:
        deploy_docker_https() 