from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO
from flask_socketio import join_room, leave_room, send, SocketIO
import random
from string import ascii_uppercase
import os
import socket

basedir = os.path.abspath(os.path.dirname(__file__))
templates_dir = os.path.join(basedir, 'templates')
static_dir = os.path.join(basedir, 'static')

app=Flask(__name__, template_folder=templates_dir, static_folder=static_dir)
app.config["SECRET_KEY"] =  "testing"
socketio = SocketIO(app)

#socketIO "listens" for actions (mainly sending/receiving messages)
# from user, javascript "data" is created (the message)
# data from JS is then sent to the app server
# server then checks our functionality to see what action to perform (updates the template of each user in room)
#app gives html pages certain socket/http capabilities, such as POST or GET

rooms = {} #keep track of used room nums

def generate_unique_code(length): #generates unique room code that is not being used
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        if code not in rooms:
            break

    return code

# Home route to display the main page
@app.route("/", methods=["GET"])
def home():
    session.clear()  # Clear the session to reset any room data
    return render_template("home.html")


# Route for joining an existing room
@app.route("/joinroom", methods=["POST", "GET"])
def join_room_page():
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")

        # Validate name and room code
        if not name:
            return render_template("joinroom.html", error="Please enter a name.")
        if not code:
            return render_template("joinroom.html", error="Please enter a room code.")
        
        # Check if room exists
        if code not in rooms:
            return render_template("joinroom.html", error="Room does not exist.")

        # Store room and name in the session
        session["room"] = code
        session["name"] = name
        return redirect(url_for("room"))

    return render_template("joinroom.html")

# Route for creating a new room
@app.route("/createroom", methods=["POST", "GET"])
def create_room_page():
    if request.method == "POST":
        name = request.form.get("name")

        # Validate name
        if not name:
            return render_template("createroom.html", error="Please enter a name.")

        # Generate a unique room code and initialize the room
        room = generate_unique_code(4)
        rooms[room] = {"members": 0, "messages": []}

        # Store room and name in the session
        session["room"] = room
        session["name"] = name
        return redirect(url_for("room"))

    return render_template("createroom.html")

# Route for displaying the chat room page
@app.route("/room", methods=["GET"])
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("home"))

    return render_template("room.html", room=room, messages = rooms[room]["messages"])


@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return

    content = {
        "name": session.get("name"),
        "message": data["data"]
    }

    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']}")

@socketio.on("connect")
def connect(auth):
    room = session.get("room")  # Making sure they have a room and name
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:  # Seeing if room does not exist
        leave_room(room)  # Leaves if accidentally joined an invalid room
        return

    join_room(room)  # If room exists, join it
    send({"name": name, "message": "Has entered the room"}, to=room)
    rooms[room]["members"] += 1  # Keep track of members currently in room
    app.logger.info(f"{name} has joined the room {room}")  # Logging user joining the room
    userIP = request.remote_addr  # Get the user's IP address
    app.logger.info(f"User {name} IP: {userIP}")  # Logging user's IP address

@socketio.on("disconnect")
def disconnect():
    room = session.get("room")  # Making sure they have a room and name
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]  # Delete room and its code if empty
    send({"name": name, "message": "Has left the room"}, to=room)
    app.logger.info(f"{name} has left the room {room}")  # Logging user leaving the room




import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    server_ip = socket.gethostbyname(socket.gethostname())
    logger.info(f"Server is running on IP: {server_ip}")
    socketio.run(app, host="0.0.0.0", port=port)

