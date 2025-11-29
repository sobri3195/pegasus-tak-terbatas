# 🦅 Pegasus Tak Terbatas - Quick Start Guide

**Created by: dr. Sobri (Muhammad Sobri Maulana)**

---

## 🚀 Installation (1 Minute)

```bash
# 1. Clone repository
git clone https://github.com/sobri3195/pegasus-tak-terbatas.git
cd pegasus-tak-terbatas

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install Ollama & models
ollama run IHA089/drana-infinity-v1

# 4. Start server
python3 pegasus_tak_terbatas.py
```

**Access:** http://127.0.0.1:80

---

## 🎯 5 New Features (v2.0)

### 1️⃣ Export Chat 📤
```bash
# Export to JSON
curl -X POST http://127.0.0.1:80/export_chat \
  -b "user_hash=YOUR_HASH" \
  -H "Content-Type: application/json" \
  -d '{"chat_id":"CHAT_ID","format":"json"}'

# Export to TXT
curl -X POST http://127.0.0.1:80/export_chat \
  -b "user_hash=YOUR_HASH" \
  -H "Content-Type: application/json" \
  -d '{"chat_id":"CHAT_ID","format":"txt"}'
```

### 2️⃣ Search Messages 🔍
```bash
# Search all chats
curl -X POST http://127.0.0.1:80/search_messages \
  -b "user_hash=YOUR_HASH" \
  -H "Content-Type: application/json" \
  -d '{"query":"keyword"}'

# Search specific chat
curl -X POST http://127.0.0.1:80/search_messages \
  -b "user_hash=YOUR_HASH" \
  -H "Content-Type: application/json" \
  -d '{"query":"keyword","chat_id":"CHAT_ID"}'
```

### 3️⃣ Statistics Dashboard 📊
```bash
curl -X GET http://127.0.0.1:80/get_statistics \
  -b "user_hash=YOUR_HASH"
```

**Returns:**
- Total chats, messages, projects
- Model usage breakdown
- Last 7 days activity

### 4️⃣ Database Backup 💾
```bash
# Create backup
curl -X POST http://127.0.0.1:80/backup_database \
  -b "user_hash=YOUR_HASH"

# List backups
curl -X GET http://127.0.0.1:80/list_backups \
  -b "user_hash=YOUR_HASH"
```

**Backup Location:** `backups/pegasus_backup_YYYYMMDD_HHMMSS.db`

### 5️⃣ Code Templates 📝
```bash
# Get predefined templates
curl -X GET http://127.0.0.1:80/get_templates

# Add custom template
curl -X POST http://127.0.0.1:80/add_custom_template \
  -b "user_hash=YOUR_HASH" \
  -H "Content-Type: application/json" \
  -d '{
    "name":"My Script",
    "code":"nmap -sV target.com",
    "description":"Port scan",
    "category":"recon"
  }'

# Get your custom templates
curl -X GET http://127.0.0.1:80/get_custom_templates \
  -b "user_hash=YOUR_HASH"
```

---

## 🎨 ASCII Art Banner

On server startup, you'll see:
```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                   🦅 Pegasus Tak Terbatas AI System 🦅                       ║
║         Designed & Developed by dr. Sobri (Muhammad Sobri Maulana)          ║
║              CEH | OSCP | OSCE | S.Kom | Cybersecurity Expert               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

---

## 📝 Code Templates Available

### Cybersecurity:
1. **Port Scan** - `nmap -sV -sC -p- -oN scan_results.txt [target_ip]`
2. **Web Enum** - `gobuster dir -u http://[target] -w wordlist.txt`
3. **SQL Injection** - `sqlmap -u 'http://[target]?id=1' --batch --dbs`
4. **Reverse Shell** - Python one-liner
5. **PrivEsc Check** - SUID, sudo, cron enumeration

### Python:
1. **HTTP Request** - requests library example
2. **File Operations** - Read/write examples

### Web:
1. **XSS Payload** - `<script>alert('XSS by dr.Sobri')</script>`
2. **CSRF POC** - Form auto-submit example

---

## 🧪 Testing

```bash
# Run automated tests
python3 test_new_features.py

# Manual API test
curl -X GET http://127.0.0.1:80/get_statistics \
  -b "user_hash=YOUR_HASH" | jq
```

---

## 📁 File Structure

```
pegasus-tak-terbatas/
├── pegasus_tak_terbatas.py   # Main application
├── updater.py                  # Auto-updater
├── requirements.txt            # Dependencies
├── README.md                   # Full documentation
├── FEATURES.md                 # Feature docs
├── API_DOCUMENTATION.md        # API reference
├── IMAGES_GUIDE.md             # Image management
├── CHANGELOG.md                # Version history
├── QUICK_START.md              # This file
├── test_new_features.py        # Test suite
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── templates/
│   └── index.html
├── backups/                    # Auto-created
└── uploads/                    # Auto-created
```

---

## 🖼️ Required Images

Create these images in `static/images/`:

1. **logo.png** (512x512) - Main logo
2. **dr.Sobri_logo.png** (200x200) - Author logo

**Quick placeholder:**
```bash
cd static/images/
wget https://via.placeholder.com/512x512.png?text=Pegasus -O logo.png
wget https://via.placeholder.com/200x200.png?text=dr.Sobri -O dr.Sobri_logo.png
```

---

## 🔑 Get Your User Hash

```javascript
// In browser console (after login):
document.cookie
  .split('; ')
  .find(row => row.startsWith('user_hash='))
  .split('=')[1]
```

Or use Python:
```python
import requests
session = requests.Session()
response = session.post('http://127.0.0.1:80/login', 
                       json={'username': 'your_username'})
print(session.cookies.get('user_hash'))
```

---

## 💡 Pro Tips

### Export All Chats:
```bash
# Get all chat IDs
CHATS=$(curl -s http://127.0.0.1:80/get_chats -b "user_hash=HASH" | jq -r '.chats[].chat_id')

# Export each
for chat_id in $CHATS; do
  curl -X POST http://127.0.0.1:80/export_chat \
    -b "user_hash=HASH" \
    -H "Content-Type: application/json" \
    -d "{\"chat_id\":\"$chat_id\",\"format\":\"json\"}" \
    -o "chat_${chat_id}.json"
done
```

### Daily Backup Script:
```bash
#!/bin/bash
# backup.sh
curl -X POST http://127.0.0.1:80/backup_database \
  -b "user_hash=$(cat ~/.pegasus_hash)"
```

### Search Multiple Terms:
```bash
for term in "vulnerability" "exploit" "payload"; do
  echo "=== Searching: $term ==="
  curl -X POST http://127.0.0.1:80/search_messages \
    -b "user_hash=HASH" \
    -H "Content-Type: application/json" \
    -d "{\"query\":\"$term\"}" | jq
done
```

---

## 🔧 Troubleshooting

### Issue: Can't connect
```bash
# Check if running
ps aux | grep pegasus

# Check port
netstat -tlnp | grep :80

# Restart server
pkill -f pegasus_tak_terbatas.py
python3 pegasus_tak_terbatas.py
```

### Issue: Module not found
```bash
pip install -r requirements.txt
```

### Issue: Images not showing
```bash
# Check images exist
ls -lh static/images/

# Set permissions
chmod 644 static/images/*.png
```

### Issue: Database locked
```bash
# Check for processes
lsof chat_database.db

# Restart server
pkill -f pegasus_tak_terbatas.py
python3 pegasus_tak_terbatas.py
```

---

## 📊 Quick Stats Check

```bash
curl -s http://127.0.0.1:80/get_statistics \
  -b "user_hash=YOUR_HASH" | jq '{
    chats: .statistics.total_chats,
    messages: .statistics.total_messages,
    projects: .statistics.total_projects
  }'
```

---

## 🎓 Learning Resources

### Documentation Files:
1. **README.md** - Full project overview
2. **FEATURES.md** - Detailed feature guide
3. **API_DOCUMENTATION.md** - Complete API reference
4. **IMAGES_GUIDE.md** - Image setup guide
5. **CHANGELOG.md** - What's new

### External Resources:
- Ollama: https://ollama.com
- Nmap: https://nmap.org
- OWASP: https://owasp.org
- dr. Sobri: https://github.com/sobri3195

---

## 📞 Support

**Author:** dr. Sobri (Muhammad Sobri Maulana)  
**Email:** muhammadsobrimaulana31@gmail.com  
**GitHub:** https://github.com/sobri3195  
**Issues:** https://github.com/sobri3195/pegasus-tak-terbatas/issues

---

## ⚡ One-Line Commands

```bash
# Complete setup
git clone https://github.com/sobri3195/pegasus-tak-terbatas.git && cd pegasus-tak-terbatas && pip install -r requirements.txt && python3 pegasus_tak_terbatas.py

# Backup now
curl -X POST http://127.0.0.1:80/backup_database -b "user_hash=$(cat ~/.pegasus_hash)"

# View stats
curl -s http://127.0.0.1:80/get_statistics -b "user_hash=HASH" | jq .statistics

# Get templates
curl -s http://127.0.0.1:80/get_templates | jq .templates.cybersecurity

# Test everything
python3 test_new_features.py
```

---

**🦅 Pegasus Tak Terbatas v2.0**  
**Built for Ethical Hackers. Powered by Intelligence.**  
**Created with ❤️ by dr. Sobri**
