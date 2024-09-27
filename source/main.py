from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def ping():
    if request.json["type"] == 1:
        return jsonify({
            "type": 1
        })
    
@app.route('/', methods=['GET'])
def hello():
    return "Hello, World!"
    
def getEnv() -> dict:
    from os import getenv
    debugMode = bool(getenv("DEBUG_MODE")) if getenv("DEBUG_MODE") != None else False
    listenIP = getenv("LISTEN_IP") if getenv("LISTEN_IP") != None else "0.0.0.0"
    port = int(getenv("port")) if getenv("port") != None else 80

    settings = dict()
    settings["debugMode"] = debugMode
    settings["listenIP"] = listenIP
    settings["port"] = port

    return settings

if __name__ == '__main__':
    settings = getEnv()
    app.run(host=settings["listenIP"], debug=settings["debugMode"], port=settings["port"])