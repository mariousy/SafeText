# [SafeText](https://safetext.onrender.com)

This is a live chat room application built using Python, Flask, and SocketIO. Users can create or join chat rooms, send real-time messages, and view message history.

## Features
- Create or join chat rooms with unique room codes.
- Real-time messaging using WebSockets (SocketIO).
- Message history is preserved during the session.
- Multiple users can join the same room and chat simultaneously.

## Requirements

Before running the application, ensure that you have the following installed:

- Python 3.x (Tested with Python 3.11)
- Flask
- Flask-SocketIO

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/mariousy/SafeText.git
   ```

2. **Navigate to the project directory:**

   ```bash
   cd SafeText
   ```

3. **Create a virtual environment (optional but recommended):**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

4. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   If `requirements.txt` is not available, manually install the dependencies:

   ```bash
   pip install flask flask-socketio eventlet
   ```

## Running the Application

1. **Start the Flask server:**

   Run the following command in your terminal:

   ```bash
   python main.py
   ```

2. **Access the application:**

   Open your browser and go to:

   ```
   http://127.0.0.1:5000/
   ```

3. **Create or Join a Chat Room:**
   
   - On the homepage, you can either create a new chat room (which will generate a unique room code) or join an existing one by entering its code.
   
4. **Start chatting!**
   
   Once inside a room, you can send messages in real-time that other users in the same room will see instantly.

## Technologies Used

- **Flask:** A lightweight web framework for Python.
- **Flask-SocketIO:** Enables real-time bidirectional communication between clients and servers using WebSockets.
- **HTML/CSS/JavaScript:** Frontend technologies used to build user interfaces.
  
## Notes

- The app uses `SocketIO` for real-time communication between clients and the server.
- The server runs on `localhost` at port `5000` by default.
- You can modify the port or other configurations inside `main.py`.

## Troubleshooting

If you encounter any issues while running the app:

1. Ensure all dependencies are installed correctly by checking `pip list`.
2. If using a virtual environment, make sure it's activated before running any commands.
3. Check for any errors in your terminal where you're running `python main.py`.

For more information on Flask-SocketIO, visit [Flask-SocketIO Documentation](https://flask-socketio.readthedocs.io/en/latest/getting_started.html).
