from flask import Flask, request, render_template, send_from_directory, jsonify
import os
import psutil

app = Flask(__name__)

# Configurations
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/file-management')
def file_management():
    return render_template('file_management.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file provided", 400
    file = request.files['file']
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return "File uploaded successfully", 200

@app.route('/download', methods=['GET'])
def download_file():
    filename = request.args.get('filename')
    if not filename:
        return "No filename provided", 400
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    except FileNotFoundError:
        return "File not found", 404

@app.route('/delete', methods=['POST'])
def delete_file():
    filename = request.form.get('filename')
    if not filename:
        return "No filename provided", 400
    try:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return "File deleted successfully", 200
    except FileNotFoundError:
        return "File not found", 404

@app.route('/user-management')
def user_management():
    return render_template('user_management.html')

@app.route('/add-user', methods=['POST'])
def add_user():
    username = request.form.get('username')
    password = request.form.get('password')
    role = request.form.get('role')
    # Add logic to save user to the database
    return f"User {username} added with role {role}"

@app.route('/monitor')
def monitor():
    return jsonify({
        "cpu_usage": psutil.cpu_percent(interval=1),
        "disk_usage": psutil.disk_usage('/').percent,
        "memory_usage": psutil.virtual_memory().percent
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
