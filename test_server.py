from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import sqlite3

app = Flask(__name__)

# Helper function to calculate expiration date based on subscription type
def calculate_expiration(tier):
    start_date = datetime.now()
    if tier == "daily":
        return (start_date + timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
    elif tier == "weekly":
        return (start_date + timedelta(weeks=1)).strftime('%Y-%m-%d %H:%M:%S')
    elif tier == "monthly":
        return (start_date + timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
    elif tier == "yearly":
        return (start_date + timedelta(days=365)).strftime('%Y-%m-%d %H:%M:%S')
    return None

@app.route('/echomimic_register', methods=['POST'])
def register():
    data = request.json
    user_uuid = data.get("uuid")
    username = data.get("username")
    password = data.get("password")  # No hashing, plain-text password
    device_fingerprint = data.get("device_fingerprint")

    # Connect to the database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Check if the UUID is valid and issued in subscription_uuids table
    cursor.execute("SELECT tier, issued FROM subscription_uuids WHERE uuid = ?", (user_uuid,))
    uuid_record = cursor.fetchone()

    if not uuid_record:
        conn.close()
        return jsonify({"status": "failed", "message": "Invalid UUID."}), 400

    tier, issued = uuid_record
    if issued == 0:
        conn.close()
        return jsonify({"status": "failed", "message": "UUID has not been issued."}), 400

    # Check if username is already registered
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return jsonify({"status": "failed", "message": "Username already exists."}), 400

    # Calculate expiration date based on tier
    expiration_date = calculate_expiration(tier)

    # Register the user by inserting into users table
    cursor.execute('''
    INSERT INTO users (uuid, username, password, device_fingerprint, subscription_type, expiration_date)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_uuid, username, password, device_fingerprint, tier, expiration_date))  # Storing plain-text password

    # Commit and close the connection
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "message": "Registration successful.", "expiration_date": expiration_date}), 200

# Endpoint to handle login
@app.route('/echomimic_login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    device_fingerprint = data.get("device_fingerprint")

    # Connect to the database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Check if username exists, password matches, and device fingerprint is correct
    cursor.execute("SELECT password, expiration_date, device_fingerprint FROM users WHERE username = ?", (username,))
    user_record = cursor.fetchone()

    if not user_record:
        conn.close()
        return jsonify({"status": "failed", "message": "Invalid credentials."}), 401

    stored_password, expiration_date, stored_fingerprint = user_record
    if stored_password != password:  # Compare plain-text password
        conn.close()
        return jsonify({"status": "failed", "message": "Invalid credentials."}), 401

    if stored_fingerprint != device_fingerprint:
        conn.close()
        return jsonify({"status": "failed", "message": "Unrecognized device."}), 401

    # Close connection and return success with expiration date
    conn.close()
    return jsonify({"status": "success", "expiration_date": expiration_date}), 200

if __name__ == '__main__':
    app.run(port=5000)
