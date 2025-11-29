# 🦅 Pegasus Tak Terbatas - API Documentation

**Version:** 2.0  
**Author:** dr. Sobri (Muhammad Sobri Maulana)  
**Base URL:** `http://127.0.0.1:80`

---

## 📑 Table of Contents

1. [Authentication](#authentication)
2. [User Management](#user-management)
3. [Chat Operations](#chat-operations)
4. [Project Management](#project-management)
5. [File Operations](#file-operations)
6. [Command Execution](#command-execution)
7. [New Features API](#new-features-api)
   - [Export Chat](#export-chat)
   - [Search Messages](#search-messages)
   - [Statistics](#statistics)
   - [Database Backup](#database-backup)
   - [Code Templates](#code-templates)

---

## 🔐 Authentication

All authenticated endpoints require a `user_hash` cookie.

### Login
**POST** `/login`

**Request:**
```json
{
  "username": "string"
}
```

**Response:**
```json
{
  "success": true,
  "user_hash": "sha256_hash",
  "username": "string"
}
```

**Cookie Set:** `user_hash` (1 year expiry)

---

### Get User Info
**GET** `/get_user_info`

**Headers:** Cookie: `user_hash=<hash>`

**Response:**
```json
{
  "success": true,
  "username": "string"
}
```

---

## 💬 Chat Operations

### Get All Chats
**GET** `/get_chats?project_id=<optional>`

**Query Parameters:**
- `project_id` (optional): Filter chats by project

**Response:**
```json
{
  "success": true,
  "chats": [
    {
      "chat_id": "uuid",
      "title": "string",
      "model_name": "string"
    }
  ]
}
```

---

### Create New Chat
**POST** `/create_new_chat`

**Request:**
```json
{
  "model_name": "string",
  "project_id": "uuid" // optional
}
```

**Response:**
```json
{
  "success": true,
  "chat_id": "uuid",
  "title": "New Chat",
  "model_name": "string"
}
```

---

### Get Chat Messages
**POST** `/get_chat_messages`

**Request:**
```json
{
  "chat_id": "uuid"
}
```

**Response:**
```json
{
  "success": true,
  "messages": [
    {
      "sender": "user|ai",
      "text": "string",
      "file_path": "string|null",
      "file_name": "string|null"
    }
  ]
}
```

---

### Send Message (Stream)
**POST** `/chat_stream`

**Request:**
```json
{
  "message": "string",
  "chat_id": "uuid",
  "model_name": "string",
  "file_path": "string|null",
  "file_name": "string|null"
}
```

**Response:** Text stream (Server-Sent Events)

---

### Rename Chat
**POST** `/rename_chat`

**Request:**
```json
{
  "chat_id": "uuid",
  "new_title": "string"
}
```

**Response:**
```json
{
  "success": true
}
```

---

### Delete Chat
**POST** `/delete_chat`

**Request:**
```json
{
  "chat_id": "uuid"
}
```

**Response:**
```json
{
  "success": true
}
```

---

## 📁 Project Management

### Get All Projects
**GET** `/get_projects`

**Response:**
```json
{
  "success": true,
  "projects": [
    {
      "project_id": "uuid",
      "title": "string"
    }
  ]
}
```

---

### Create Project
**POST** `/create_new_project`

**Request:**
```json
{
  "project_name": "string"
}
```

**Response:**
```json
{
  "success": true,
  "project_id": "uuid",
  "title": "string"
}
```

---

### Rename Project
**POST** `/rename_project`

**Request:**
```json
{
  "project_id": "uuid",
  "new_title": "string"
}
```

**Response:**
```json
{
  "success": true
}
```

---

### Delete Project
**POST** `/delete_project`

**Request:**
```json
{
  "project_id": "uuid"
}
```

**Response:**
```json
{
  "success": true
}
```

---

## 📎 File Operations

### Upload File
**POST** `/upload_file`

**Form Data:**
- `file`: File binary
- `chat_id`: string

**Response:**
```json
{
  "success": true,
  "file_path": "/uploads/chat_id/filename",
  "file_name": "filename"
}
```

---

### Access Uploaded File
**GET** `/uploads/<chat_id>/<filename>`

**Response:** File binary

---

## ⚙️ Command Execution

### Execute Command (Stream)
**POST** `/execute_stream`

**Request:**
```json
{
  "command": "string",
  "chat_id": "uuid",
  "output_id": "uuid"
}
```

**Response:** Text stream of command output

---

### Get Command Output
**POST** `/get_command_output`

**Request:**
```json
{
  "output_id": "uuid"
}
```

**Response:**
```json
{
  "success": true,
  "command": "string",
  "output": "string"
}
```

---

## 🤖 Model Management

### Get Available Models
**GET** `/get_models`

**Response:**
```json
{
  "success": true,
  "models": ["model1", "model2"]
}
```

---

## 🆕 New Features API

### 📤 Export Chat

**POST** `/export_chat`

Export complete chat history to JSON or TXT format.

**Request:**
```json
{
  "chat_id": "uuid",
  "format": "json" | "txt"
}
```

**Response (JSON format):**
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

**Response (TXT format):**
```json
{
  "success": true,
  "data": "Plain text chat export...",
  "filename": "chat_uuid.txt"
}
```

**Example:**
```bash
curl -X POST http://127.0.0.1:80/export_chat \
  -H "Content-Type: application/json" \
  -b "user_hash=your-hash" \
  -d '{"chat_id":"123","format":"json"}'
```

---

### 🔍 Search Messages

**POST** `/search_messages`

Search across all messages with keyword matching.

**Request:**
```json
{
  "query": "string",
  "chat_id": "uuid" // optional - search specific chat
}
```

**Response:**
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

**Features:**
- Case-insensitive search
- Searches in message text
- Returns up to 50 results
- Ordered by most recent

**Example:**
```bash
curl -X POST http://127.0.0.1:80/search_messages \
  -H "Content-Type: application/json" \
  -b "user_hash=your-hash" \
  -d '{"query":"vulnerability"}'
```

---

### 📊 Statistics

**GET** `/get_statistics`

Get comprehensive user activity statistics.

**Response:**
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

**Metrics Included:**
- Total chats created
- Total messages sent/received
- Total projects
- AI model usage breakdown
- Last 7 days activity

**Example:**
```bash
curl -X GET http://127.0.0.1:80/get_statistics \
  -b "user_hash=your-hash"
```

---

### 💾 Database Backup

#### Create Backup
**POST** `/backup_database`

Create a timestamped backup of the entire database.

**Response:**
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

**Example:**
```bash
curl -X POST http://127.0.0.1:80/backup_database \
  -b "user_hash=your-hash"
```

---

#### List Backups
**GET** `/list_backups`

Get list of all available backups.

**Response:**
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

**Example:**
```bash
curl -X GET http://127.0.0.1:80/list_backups \
  -b "user_hash=your-hash"
```

---

### 📝 Code Templates

#### Get Predefined Templates
**GET** `/get_templates`

Get library of cybersecurity and coding templates.

**Response:**
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
    ],
    "python": [...],
    "web": [...]
  },
  "created_by": "dr. Sobri - Pegasus Tak Terbatas",
  "total_categories": 3,
  "total_templates": 9
}
```

**Categories:**
- `cybersecurity`: Port scanning, web enum, SQLi, reverse shells, privesc
- `python`: HTTP requests, file operations
- `web`: XSS, CSRF payloads

**Example:**
```bash
curl -X GET http://127.0.0.1:80/get_templates
```

---

#### Get Custom Templates
**GET** `/get_custom_templates`

Get user's custom saved templates.

**Response:**
```json
{
  "success": true,
  "templates": [
    {
      "template_id": "uuid",
      "name": "My Script",
      "code": "#!/bin/bash\necho 'test'",
      "description": "Test script",
      "category": "custom",
      "timestamp": "2024-01-01 12:00:00"
    }
  ]
}
```

**Example:**
```bash
curl -X GET http://127.0.0.1:80/get_custom_templates \
  -b "user_hash=your-hash"
```

---

#### Add Custom Template
**POST** `/add_custom_template`

Save a new custom template.

**Request:**
```json
{
  "name": "string",
  "code": "string",
  "description": "string", // optional
  "category": "string" // optional, default: "custom"
}
```

**Response:**
```json
{
  "success": true,
  "template_id": "uuid"
}
```

**Example:**
```bash
curl -X POST http://127.0.0.1:80/add_custom_template \
  -H "Content-Type: application/json" \
  -b "user_hash=your-hash" \
  -d '{
    "name": "My Payload",
    "code": "<?php system($_GET[\"cmd\"]); ?>",
    "description": "PHP webshell",
    "category": "exploitation"
  }'
```

---

## 📡 WebSocket/Streaming Endpoints

These endpoints use Server-Sent Events (SSE) or streaming responses:

1. `/chat_stream` - AI chat responses
2. `/execute_stream` - Command execution output

**Example (JavaScript):**
```javascript
const response = await fetch('/chat_stream', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    message: 'Hello',
    chat_id: 'uuid',
    model_name: 'llama3'
  })
});

const reader = response.body.getReader();
const decoder = new TextDecoder();

while (true) {
  const {value, done} = await reader.read();
  if (done) break;
  
  const chunk = decoder.decode(value);
  console.log(chunk);
}
```

---

## ⚠️ Error Responses

All endpoints return standard error format:

```json
{
  "success": false,
  "message": "Error description"
}
```

**Common HTTP Status Codes:**
- `200` - Success
- `400` - Bad Request (missing parameters)
- `401` - Unauthorized (missing/invalid user_hash)
- `404` - Not Found
- `500` - Internal Server Error

---

## 🔒 Security Notes

1. **Authentication:** All endpoints require valid `user_hash` cookie
2. **SQL Injection:** All queries use parameterized statements
3. **File Upload:** Filenames sanitized with `secure_filename()`
4. **CORS:** Configure as needed for production
5. **Rate Limiting:** Consider adding for production use

---

## 📊 Rate Limits (Recommended for Production)

Not implemented by default. Recommended limits:

- Chat messages: 60/minute
- File uploads: 10/minute
- Search: 30/minute
- Backups: 5/hour

---

## 🧪 Testing

### cURL Examples

**Login:**
```bash
curl -X POST http://127.0.0.1:80/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test_user"}' \
  -c cookies.txt
```

**Create Chat:**
```bash
curl -X POST http://127.0.0.1:80/create_new_chat \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"model_name":"llama3"}'
```

**Export Chat:**
```bash
curl -X POST http://127.0.0.1:80/export_chat \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"chat_id":"your-id","format":"json"}' \
  -o chat_export.json
```

**Get Statistics:**
```bash
curl -X GET http://127.0.0.1:80/get_statistics \
  -b cookies.txt
```

---

### Python Examples

```python
import requests

# Login
session = requests.Session()
login_response = session.post('http://127.0.0.1:80/login', 
                              json={'username': 'test_user'})
print(login_response.json())

# Create chat
chat_response = session.post('http://127.0.0.1:80/create_new_chat',
                            json={'model_name': 'llama3'})
chat_id = chat_response.json()['chat_id']

# Export chat
export_response = session.post('http://127.0.0.1:80/export_chat',
                               json={'chat_id': chat_id, 'format': 'json'})
print(export_response.json())

# Get statistics
stats_response = session.get('http://127.0.0.1:80/get_statistics')
print(stats_response.json())

# Search messages
search_response = session.post('http://127.0.0.1:80/search_messages',
                              json={'query': 'test'})
print(search_response.json())

# Backup database
backup_response = session.post('http://127.0.0.1:80/backup_database')
print(backup_response.json())

# Get templates
templates_response = session.get('http://127.0.0.1:80/get_templates')
print(templates_response.json())
```

---

## 🔄 API Versioning

Current version: **v2.0**

Future versions will be indicated in:
- Response headers: `X-API-Version: 2.0`
- URL prefix: `/api/v2/...` (if implemented)

---

## 📞 Support & Contact

**Author:** Lettu Kes dr. Muhammad Sobri Maulana, S.Kom, CEH, OSCP, OSCE  
**Email:** muhammadsobrimaulana31@gmail.com  
**GitHub:** [github.com/sobri3195](https://github.com/sobri3195)  
**Website:** [muhammadsobrimaulana.netlify.app](https://muhammadsobrimaulana.netlify.app)

---

## 📄 License

MIT License - See LICENSE file for details

---

**🦅 Pegasus Tak Terbatas API Documentation**  
**Created by dr. Sobri - Built for Ethical Hackers**

**#PegasusTakTerbatas #API #Documentation #CyberSecurity**
