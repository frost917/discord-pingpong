from flask import Flask, jsonify, request

app = Flask(__name__)
app.debug = True

@app.route('/', methods=['POST'])
def ping():
    if request.json["type"] == 1:
        return jsonify({
            "type": 1
        })