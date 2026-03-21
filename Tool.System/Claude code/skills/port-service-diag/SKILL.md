---
name: port-service-diag
description: Diagnose port occupation and service connection issues. Use when services fail to start with "port already in use", connection refused, or authentication rejected errors. Covers port conflicts, process analysis, token derivation patterns, and service restart strategies.
argument-hint: [port]
disable-model-invocation: true
allowed-tools: Bash(lsof *), Bash(netstat *), Bash(ps *), Bash(curl *), Bash(kill *), Bash(node *), Bash(cat *), Bash(grep *), Bash(systemctl *), Bash(launchctl *), Read, Grep, Glob
---

# Port & Service Connection Diagnostic

Systematic approach to diagnosing port occupation and service connection issues.

## Usage
```
/port-service-diag 8080      # Diagnose specific port
/port-service-diag           # Interactive mode
```

## Quick Check

### Port Status
!`echo "=== Common Service Ports ===" && lsof -i :80 -i :443 -i :3000 -i :8080 -i :8765 -i :18789 -i :18792 2>/dev/null | head -15 || echo "No common ports in use"`

---

## Diagnostic Workflow

### 1. Port Occupation Check

**Find what's using a port**:
```bash
# macOS/Linux
lsof -i :<PORT>

# Alternative
netstat -an | grep <PORT>
ss -tlnp | grep <PORT>  # Linux only
```

**Decision tree**:
- Same service expected? → Service is already running (normal)
- Different service? → Conflict, need to stop or reconfigure
- No output? → Port is free, service may be down

### 2. Process Analysis

**Identify the process**:
```bash
# Get PID from port
PID=$(lsof -t -i :<PORT>)

# Get process details
ps -p $PID -o pid,ppid,user,command

# Get process tree (what started it)
pstree -p $PID  # Linux
ps -o pid= -p $PID  # macOS
```

**Check if it's a managed service**:
```bash
# systemd (Linux)
systemctl status <service-name>

# launchd (macOS)
launchctl list | grep <service>
brew services list | grep <service>
```

### 3. Configuration Sync Check

**Service config vs running state mismatch** is a common issue.

**Symptoms**:
- "Token rejected" errors
- Changes not taking effect
- Doctor/health check shows mismatch

**Check config file**:
```bash
# Find config
find ~ -name "*.json" -path "*<service>*" 2>/dev/null

# Check for environment variables in service definition
# macOS launchd
cat ~/Library/LaunchAgents/<service>.plist | grep -A 1 "<key>.*KEY\|<key>.*TOKEN"

# Linux systemd
systemctl show <service> -p Environment
```

**Fix: Reinstall/reload service**:
```bash
# Generic pattern
<service> stop
<service> uninstall  # or disable
<service> install    # or enable
<service> start
```

### 4. Token/Auth Derivation Pattern

**Many services use derived tokens, not direct tokens.**

**Common derivation patterns**:

```bash
# HMAC-SHA256 derivation (most common)
node -e "
const crypto = require('crypto');
const secret = 'YOUR_SECRET';
const payload = 'context:port';
const derived = crypto.createHmac('sha256', secret).update(payload).digest('hex');
console.log(derived);
"

# SHA256 hash
echo -n "secret:data" | sha256sum

# Base64 encoded
echo -n "secret:data" | base64
```

**Test authentication**:
```bash
# HTTP header auth
curl -H "x-auth-token: <TOKEN>" http://localhost:<PORT>/health

# Query param auth
curl "http://localhost:<PORT>/health?token=<TOKEN>"

# Basic auth
curl -u user:pass http://localhost:<PORT>/health
```

### 5. WebSocket Connection Test

```bash
# Install wscat if needed
npm install -g wscat

# Test WebSocket with auth
wscat -c "ws://localhost:<PORT>/path?token=<TOKEN>"

# Or use curl for upgrade check
curl -i -N \
  -H "Connection: Upgrade" \
  -H "Upgrade: websocket" \
  -H "Sec-WebSocket-Key: test" \
  -H "Sec-WebSocket-Version: 13" \
  "http://localhost:<PORT>/path"
```

---

## Common Patterns

### Pattern: "Port already in use"

```
Error: listen EADDRINUSE: address already in use
```

**Steps**:
1. `lsof -i :<PORT>` - Find what's using it
2. Decide: kill it or change port
3. If killing: `kill $(lsof -t -i :<PORT>)`
4. If changing: update config and restart

### Pattern: "Authentication rejected"

```
Error: 401 Unauthorized
```

**Steps**:
1. Check if using direct token vs derived token
2. Look for HMAC/hash derivation in source or docs
3. Calculate derived token and test
4. Check if service config synced with service runtime

### Pattern: "Connection refused"

```
Error: connect ECONNREFUSED
```

**Steps**:
1. Check if service is running: `ps aux | grep <service>`
2. Check if listening: `lsof -i :<PORT>`
3. Check firewall: `ufw status` / `pfctl -s all`
4. Check service logs: `journalctl -u <service>` or log files

### Pattern: "Service not picking up config changes"

**Steps**:
1. Check if service uses environment variables from service manager
2. Reinstall service to sync: `<service> uninstall && <service> install`
3. Or reload: `systemctl daemon-reload` / `launchctl unload && load`

---

## Decision Matrix

| Symptom | Likely Cause | First Check |
|---------|--------------|-------------|
| Port in use | Old process | `lsof -i :PORT` |
| Auth rejected | Wrong/derived token | Check token derivation |
| Config ignored | Service not reloaded | Reinstall service |
| Random disconnects | Resource limits | Check logs, memory |

---

## Full Diagnostic Script Template

```bash
#!/bin/bash
PORT=${1:-8080}
echo "=== Port $PORT Diagnostic ==="

echo -e "\n1. Port Status:"
lsof -i :$PORT 2>/dev/null || echo "   Port is FREE"

echo -e "\n2. Process Details:"
PID=$(lsof -t -i :$PORT 2>/dev/null)
[ -n "$PID" ] && ps -p $PID -o pid,ppid,user,command || echo "   No process"

echo -e "\n3. Connectivity:"
curl -s -m 2 http://localhost:$PORT/health 2>/dev/null || echo "   No HTTP response"

echo -e "\n4. Service Status (if known):"
# Add service-specific checks here
```

---

## Key Takeaways

1. **Always check both config file AND running service state** - they can drift
2. **Token derivation is common** - don't assume direct token usage
3. **Reinstall service after config changes** - ensures sync
4. **Same PID on multiple ports is normal** - single process can listen on many
