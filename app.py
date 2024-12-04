from flask import Flask, render_template, request, jsonify, send_from_directory
import hashlib
import os
import json

app = Flask(__name__)

# File paths
USERS_FILE = "users.txt"
ROOMS_FILE = "rooms.txt"
MESSAGES_DIR = "messages"

# Ensure necessary files and directories exist
if not os.path.exists(USERS_FILE):
    open(USERS_FILE, "w").close()

if not os.path.exists(ROOMS_FILE):
    open(ROOMS_FILE, "w").close()

if not os.path.exists(MESSAGES_DIR):
    os.makedirs(MESSAGES_DIR)

# Helper function to hash passwords
def encrypt_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Helper function to generate unique room IDs
def generate_room_id():
    return os.urandom(4).hex()

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        encrypted_password = encrypt_password(password)
        
        # Check if user exists
        with open(USERS_FILE, "r+") as f:
            users = f.readlines()
            for user in users:
                stored_user, stored_password = user.strip().split(":")
                if stored_user == username:
                    if stored_password == encrypted_password:
                        return redirect(f"/chat/{username}")
                    else:
                        return "Invalid password!"
        
        # Register new user
        with open(USERS_FILE, "a") as f:
            f.write(f"{username}:{encrypted_password}\n")
        return redirect(f"/chat/{username}")
    
    return render_template("login.html")

@app.route("/chat/<username>")
def chat(username):
    return render_template("chat.html", username=username)

@app.route("/create_room", methods=["POST"])
def create_room():
    room_id = generate_room_id()
    with open(ROOMS_FILE, "a") as f:
        f.write(f"{room_id}\n")
    # Create a file for room messages
    open(os.path.join(MESSAGES_DIR, f"{room_id}.txt"), "w").close()
    return jsonify({"room_id": room_id})

@app.route("/join_room", methods=["POST"])
def join_room():
    room_id = request.json["room_id"]
    with open(ROOMS_FILE, "r") as f:
        rooms = f.readlines()
    if f"{room_id}\n" in rooms:
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "error", "message": "Room not found."})

@app.route("/send_message", methods=["POST"])
def send_message():
    room_id = request.json["room_id"]
    username = request.json["username"]
    message = request.json["message"]
    
    # Save message to the room file
    room_file = os.path.join(MESSAGES_DIR, f"{room_id}.txt")
    if os.path.exists(room_file):
        with open(room_file, "a") as f:
            f.write(f"{username}: {message}\n")
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "error", "message": "Room not found."})

@app.route("/get_messages", methods=["POST"])
def get_messages():
    room_id = request.json["room_id"]
    room_file = os.path.join(MESSAGES_DIR, f"{room_id}.txt")
    
    if os.path.exists(room_file):
        with open(room_file, "r") as f:
            messages = f.readlines()
        return jsonify({"messages": messages})
    else:
        return jsonify({"status": "error", "message": "Room not found."})

if __name__ == "__main__":
    app.run(debug=True)
