from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def hello_world():  # główny endpoint
    return 'Hello World!'


@app.route('/health', methods=['GET'])
def health_check():
    # Endpoint health zwraca status 200 oraz opcjonalnie dane o stanie
    return jsonify({"status": "ok"}), 200


if __name__ == '__main__':
    app.run()
