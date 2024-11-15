from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/scan/<uid>', methods=['POST'])
def monitor_uid(uid):
    if uid == "c4:17:bf:e2":
        # Actie voor pasje 1
        action_message = "Welkom! 19200 uw kluisje word geopend."
        print(f"*** {action_message} ***")
        return jsonify({"message": action_message}), 200
    elif uid == "16:9b:51:39":
        action_message = "Uw documenten worden nu geprint."
        print(f"*** {action_message} ***")
        return jsonify({"message": action_message}), 200
    else:
        action_message = f"Wij konden die actie niet vinden."
        print(f"*** {action_message} ***")
        return jsonify({"message": action_message}), 404

if __name__ == '__main__':
    import logging
    log = logging.getLogger('werkzeug')
    log.disabled = True

    app.run(host='0.0.0.0', port=5000)