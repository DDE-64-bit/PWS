from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = "nfc_database.db"

# Functie om de database in te stellen
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nfc_tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uid TEXT NOT NULL UNIQUE,
            geld REAL DEFAULT 10.0,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/scan/<uid>', methods=['POST'])
def scan_nfc(uid):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Controleer of het UID al bestaat
        cursor.execute('SELECT id, uid, geld, timestamp FROM nfc_tags WHERE uid = ?', (uid,))
        record = cursor.fetchone()
        
        if record:
            # Retourneer gegevens als het UID al bestaat
            conn.close()
            return jsonify({
                "id": record[0],
                "uid": record[1],
                "geld": record[2],
                "timestamp": record[3],
                "message": "UID already exists, data retrieved."
            }), 200
        else:
            # Voeg een nieuw record toe als het UID niet bestaat
            cursor.execute('''
                INSERT INTO nfc_tags (uid, geld)
                VALUES (?, 10.0)
            ''', (uid,))
            conn.commit()
            conn.close()
            return jsonify({
                "message": f"UID {uid} saved successfully!",
                "geld": 10.0
            }), 201
    except Exception as e:
        # Foutafhandeling
        return jsonify({"error": str(e)}), 500

@app.route('/uids', methods=['GET'])
def get_uids():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, uid, geld, timestamp FROM nfc_tags')
    rows = cursor.fetchall()
    conn.close()

    return jsonify([
        {"id": row[0], "uid": row[1], "geld": row[2], "timestamp": row[3]}
        for row in rows
    ])

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
