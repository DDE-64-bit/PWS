from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('nfc_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nfc_tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uid TEXT NOT NULL UNIQUE,
            value INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/receive_uid', methods=['POST'])
def receive_uid():
    try:
        data = request.get_json()

        if 'uid' in data:
            uid = data['uid']
            print(f"Received UID: {uid}")

            conn = sqlite3.connect('nfc_data.db')
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM nfc_tags WHERE uid = ?", (uid,))
            row = cursor.fetchone()

            if row:
                value = row[0]
                message = f"UID Bestaat met waarde: {value}"
            else:
                cursor.execute("INSERT INTO nfc_tags (uid, value) VALUES (?, ?)", (uid, 0))
                conn.commit()
                value = 0
                message = "Nieuwe UID toegevoegd met standaart waarde 0" 

            conn.close()
            return jsonify({"status": "success", "uid_received": uid, "value": value, "message": message}), 200

        else:
            return jsonify({"status": "error", "message": "No UID provided"}), 400

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/get_value', methods=['POST'])
def get_value():
    try:
        data = request.get_json()
        uid = data.get('uid')

        if not uid:
            return jsonify({"status": "error", "message": "No UID provided"}), 400

        conn = sqlite3.connect('nfc_data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM nfc_tags WHERE uid = ?", (uid,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return jsonify({"status": "success", "uid": uid, "value": row[0]}), 200
        else:
            return jsonify({"status": "error", "message": "UID not found"}), 404

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/update_value', methods=['POST'])
def update_value():
    try:
        data = request.get_json()
        uid = data.get('uid')
        amount = data.get('amount')

        if not uid or amount is None:
            return jsonify({"status": "error", "message": "UID and amount are required"}), 400

        conn = sqlite3.connect('nfc_data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM nfc_tags WHERE uid = ?", (uid,))
        row = cursor.fetchone()

        if row:
            new_value = row[0] + amount
            cursor.execute("UPDATE nfc_tags SET value = ? WHERE uid = ?", (new_value, uid))
            conn.commit()
            conn.close()
            return jsonify({"status": "success", "uid": uid, "new_value": new_value}), 200
        else:
            conn.close()
            return jsonify({"status": "error", "message": "UID not found"}), 404

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)