# 🦅 Pegasus Tak Terbatas - New Features Documentation

**Created by: dr. Sobri (Muhammad Sobri Maulana)**  
**Version: 2.0**  
**Date: 2024**

---

## 📋 Table of Contents

1. [ASCII Art Banner](#ascii-art-banner)
2. [Image Management](#image-management)
3. [New Features](#new-features)
   - [Feature 1: Export Chat History](#feature-1-export-chat-history)
   - [Feature 2: Search in Messages](#feature-2-search-in-messages)
   - [Feature 3: Statistics Dashboard](#feature-3-statistics-dashboard)
   - [Feature 4: Database Backup & Restore](#feature-4-database-backup--restore)
   - [Feature 5: Code Templates Library](#feature-5-code-templates-library)

---

## 🎨 ASCII Art Banner

A custom ASCII art banner has been added featuring **"PEGASUS TAK TERBATAS"** with full attribution to **dr. Sobri**.

### Implementation:
- Displays on server startup
- Shows author credentials: dr. Muhammad Sobri Maulana (CEH, OSCP, OSCE, S.Kom)
- Professional banner with Unicode box-drawing characters
- Includes contact information and project motto

### Location:
- `pegasus_tak_terbatas.py` - Lines 23-59
- Displayed in terminal on application start

---

## 🖼️ Image Management

### Current Image Structure:
```
static/
└── images/
    ├── 1764390579.png (existing)
    ├── 1764390625.png (existing)
    ├── logo.png (referenced in HTML)
    └── dr.Sobri_logo.png (referenced in HTML)
```

### Image References in Application:
1. **Logo Image** - `static/images/logo.png`
   - Used in: Header logo, favicon, processing overlay
   - Lines in index.html: 8, 33, 67

2. **dr.Sobri Logo** - `static/images/dr.Sobri_logo.png`
   - Used in: Settings/About modal
   - Line in index.html: 92

### Image Hyperlinks:
All images are properly linked using Flask's `url_for()` function:
```html
<img src="{{ url_for('static', filename='images/logo.png') }}" alt="Logo">
<img src="{{ url_for('static', filename='images/dr.Sobri_logo.png') }}" alt="dr.Sobri Logo">
```

### Image Upload Feature:
- Users can upload files per chat session
- Files stored in: `uploads/<chat_id>/<filename>`
- Accessible via route: `/uploads/<chat_id>/<filename>`
- Secure filename handling with `werkzeug.utils.secure_filename`

---

## 🚀 New Features

### Feature 1: Export Chat History

**Endpoint:** `POST /export_chat`

#### Description:
Export complete chat conversations to JSON or TXT format with full metadata.

#### Parameters:
```json
{
  "chat_id": "string",
  "format": "json" | "txt"
}
```

#### Response Example (JSON):
```json
{
  "success": true,
  "data": {
    "title": "Chat Title",
    "model": "llama3",
    "exported_at": "2024-01-01T12:00:00",
    "exported_by": "dr. Sobri - Pegasus Tak Terbatas",
    "messages": [
      {
        "sender": "user",
        "text": "Hello",
        "timestamp": "2024-01-01 12:00:00"
      }
    ]
  },
  "filename": "chat_uuid.json"
}
```

#### Usage:
```javascript
fetch('/export_chat', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    chat_id: 'your-chat-id',
    format: 'json'
  })
});
```

---

### Feature 2: Search in Messages

**Endpoint:** `POST /search_messages`

#### Description:
Search through all messages across chats or within a specific chat with keyword matching.

#### Parameters:
```json
{
  "query": "search term",
  "chat_id": "optional-chat-id"
}
```

#### Response:
```json
{
  "success": true,
  "results": [
    {
      "message_id": 1,
      "chat_id": "uuid",
      "sender": "user",
      "text": "message containing search term",
      "timestamp": "2024-01-01 12:00:00",
      "chat_title": "Chat Name"
    }
  ],
  "count": 5
}
```

#### Features:
- Search across all user's chats
- Search within specific chat
- Returns up to 50 results
- Ordered by most recent first

---

### Feature 3: Statistics Dashboard

**Endpoint:** `GET /get_statistics`

#### Description:
Comprehensive analytics dashboard showing user activity, model usage, and trends.

#### Response:
```json
{
  "success": true,
  "statistics": {
    "total_chats": 10,
    "total_messages": 150,
    "total_projects": 3,
    "model_usage": [
      {"model": "llama3", "count": 7},
      {"model": "drana-infinity", "count": 3}
    ],
    "daily_activity": [
      {"date": "2024-01-01", "count": 25},
      {"date": "2024-01-02", "count": 30}
    ],
    "generated_by": "dr. Sobri - Pegasus Tak Terbatas"
  }
}
```

#### Metrics:
- Total chats created
- Total messages sent/received
- Total projects
- Model usage breakdown
- 7-day activity history

---

### Feature 4: Database Backup & Restore

**Endpoints:**
- `POST /backup_database` - Create backup
- `GET /list_backups` - List all backups

#### Description:
Complete database backup system with timestamped snapshots for data protection.

#### Backup Response:
```json
{
  "success": true,
  "message": "Database backed up successfully!",
  "filename": "pegasus_backup_20240101_120000.db",
  "path": "backups/pegasus_backup_20240101_120000.db",
  "timestamp": "20240101_120000",
  "created_by": "dr. Sobri - Pegasus Tak Terbatas"
}
```

#### List Backups Response:
```json
{
  "success": true,
  "backups": [
    {
      "filename": "pegasus_backup_20240101_120000.db",
      "size": 1048576,
      "created": "2024-01-01T12:00:00"
    }
  ]
}
```

#### Storage:
- Backups stored in: `backups/` directory
- Filename format: `pegasus_backup_YYYYMMDD_HHMMSS.db`
- Automatic timestamp generation

---

### Feature 5: Code Templates Library

**Endpoints:**
- `GET /get_templates` - Get predefined templates
- `GET /get_custom_templates` - Get user's custom templates
- `POST /add_custom_template` - Add new custom template

#### Description:
Comprehensive library of cybersecurity, Python, and web testing code snippets.

#### Categories:
1. **Cybersecurity**
   - Port Scanning (nmap)
   - Web Enumeration (gobuster)
   - SQL Injection Testing (sqlmap)
   - Reverse Shells
   - Privilege Escalation

2. **Python**
   - HTTP Requests
   - File Operations

3. **Web Security**
   - XSS Payloads
   - CSRF POC

#### Get Templates Response:
```json
{
  "success": true,
  "templates": {
    "cybersecurity": [
      {
        "name": "Port Scan",
        "description": "Basic nmap port scanning",
        "code": "nmap -sV -sC -p- -oN scan_results.txt [target_ip]",
        "category": "reconnaissance"
      }
    ]
  },
  "created_by": "dr. Sobri - Pegasus Tak Terbatas",
  "total_categories": 3,
  "total_templates": 9
}
```

#### Add Custom Template:
```json
{
  "name": "My Custom Script",
  "code": "#!/bin/bash\necho 'Hello World'",
  "description": "Custom description",
  "category": "custom"
}
```

#### Database Schema:
```sql
CREATE TABLE custom_templates (
    template_id TEXT PRIMARY KEY,
    user_hash TEXT NOT NULL,
    name TEXT NOT NULL,
    code TEXT NOT NULL,
    description TEXT,
    category TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_hash) REFERENCES users(user_hash) ON DELETE CASCADE
)
```

---

## 🔧 Technical Implementation

### Dependencies Added:
```python
from datetime import datetime
import shutil
```

### Database Changes:
- New table: `custom_templates`
- Foreign key relationships maintained
- Cascade delete on user removal

### Security Features:
- User hash authentication on all endpoints
- Secure file handling
- SQL injection prevention with parameterized queries
- Input validation

---

## 📊 API Usage Examples

### Export Chat:
```bash
curl -X POST http://127.0.0.1:80/export_chat \
  -H "Content-Type: application/json" \
  -b "user_hash=your-hash" \
  -d '{"chat_id":"chat-uuid","format":"json"}'
```

### Search Messages:
```bash
curl -X POST http://127.0.0.1:80/search_messages \
  -H "Content-Type: application/json" \
  -b "user_hash=your-hash" \
  -d '{"query":"search term"}'
```

### Get Statistics:
```bash
curl -X GET http://127.0.0.1:80/get_statistics \
  -b "user_hash=your-hash"
```

### Backup Database:
```bash
curl -X POST http://127.0.0.1:80/backup_database \
  -b "user_hash=your-hash"
```

### Get Templates:
```bash
curl -X GET http://127.0.0.1:80/get_templates
```

---

## 🎯 Integration Guide

### Frontend Integration:
Add these buttons/features to the UI:

1. **Chat Export Button** - In chat menu
2. **Search Bar** - In header/sidebar
3. **Statistics Dashboard** - New page/modal
4. **Backup Button** - In settings
5. **Templates Library** - New page/modal with categories

### Example JavaScript:
```javascript
// Export Chat
async function exportChat(chatId, format) {
  const response = await fetch('/export_chat', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({chat_id: chatId, format: format})
  });
  const data = await response.json();
  if (data.success) {
    // Download file
    const blob = new Blob([JSON.stringify(data.data)], 
                          {type: 'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = data.filename;
    a.click();
  }
}

// Search Messages
async function searchMessages(query, chatId = null) {
  const response = await fetch('/search_messages', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({query: query, chat_id: chatId})
  });
  const data = await response.json();
  return data.results;
}

// Get Statistics
async function loadStatistics() {
  const response = await fetch('/get_statistics');
  const data = await response.json();
  displayStatistics(data.statistics);
}

// Backup Database
async function backupDatabase() {
  const response = await fetch('/backup_database', {method: 'POST'});
  const data = await response.json();
  alert(data.message);
}

// Load Templates
async function loadTemplates() {
  const response = await fetch('/get_templates');
  const data = await response.json();
  displayTemplates(data.templates);
}
```

---

## 🌟 Benefits

### For Users:
- **Data Portability**: Export chats for backup or sharing
- **Efficient Search**: Quickly find past conversations
- **Insights**: Understand usage patterns with statistics
- **Data Protection**: Regular backups prevent data loss
- **Productivity**: Quick access to code templates

### For Developers:
- **API-First Design**: All features accessible via REST API
- **Extensible**: Easy to add more templates or export formats
- **Documented**: Clear examples and response schemas
- **Secure**: Authentication and validation on all endpoints

---

## 📝 Version History

### v2.0 - Current Release
- ✅ ASCII Art Banner with dr. Sobri attribution
- ✅ Export Chat History (JSON/TXT)
- ✅ Message Search Functionality
- ✅ Statistics Dashboard
- ✅ Database Backup System
- ✅ Code Templates Library
- ✅ Image management documentation
- ✅ Comprehensive API documentation

### v1.0 - Initial Release
- Basic chat functionality
- Project management
- File uploads
- Command execution

---

## 📧 Support & Contact

**Author:** Lettu Kes dr. Muhammad Sobri Maulana, S.Kom, CEH, OSCP, OSCE  
**Email:** muhammadsobrimaulana31@gmail.com  
**GitHub:** [github.com/sobri3195](https://github.com/sobri3195)  
**Website:** [muhammadsobrimaulana.netlify.app](https://muhammadsobrimaulana.netlify.app)

---

## ⚖️ License

MIT License - See LICENSE file for details

---

**Made with ❤️ by dr. Sobri**

**#PegasusTakTerbatas #CyberSecurity #EthicalHacking #AI**
