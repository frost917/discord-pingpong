from flask import Flask, jsonify, request, abort
from functools import wraps

def getEnv() -> dict:
    from os import getenv
    debugMode = bool(getenv("DEBUG_MODE")) if getenv("DEBUG_MODE") != None else False
    listenIP = getenv("LISTEN_IP") if getenv("LISTEN_IP") != None else "0.0.0.0"
    port = int(getenv("PORT")) if getenv("PORT") != None else 80
    pubkey = bytes.fromhex(getenv("BOT_PUBKEY")) if getenv("BOT_PUBKEY") != None else Exception("NO_BOT_PBKEY_EXCPTION")

    settings = dict()
    settings["debugMode"] = debugMode
    settings["listenIP"] = listenIP
    settings["port"] = port
    settings["pubkey"] = pubkey

    return settings

app = Flask(__name__)
settings = getEnv()

def keyVerify(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from nacl.signing import VerifyKey
        from nacl.exceptions import BadSignatureError

        keyBox = VerifyKey(settings["pubkey"])

        timestamp = request.headers["X-Signature-Timestamp"]
        signature = request.headers["X-Signature-Ed25519"]
        body = request.data.decode('utf-8')

        try:
            keyBox.verify(f'{timestamp}{body}'.encode(), signature=bytes.fromhex(signature))
            
            if settings["debugMode"] :
                print("signature verify successed!")
        except BadSignatureError:
            abort(401, 'Invalid Signature Error')

        return f(*args, **kwargs)
    return decorated_function


@app.route('/', methods=['POST'])
@keyVerify
def interactions():
    app.logger.debug("DEBUG: request header")
    app.logger.debug(request.headers)
    app.logger.debug("DEBUG: request data")
    app.logger.debug(request.data)

    if request.json["type"] == 1:
        return jsonify({
            "type": 1
        })

    elif request.json["type"] == 2:
        if request.json["data"]["name"] == "ping":
            app.logger.info(f"command ping requested")
            return jsonify({
                "type": 4,
                "data": {
                    "content": "pong!"
                }
            })
        
    else:
        app.logger.warning(f"unregistered command requested")
        return jsonify({
            "type": 4,
            "data": {
                # send lorem ipsum
                "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
            }
        })

    
@app.route('/', methods=['GET'])
def hello():
    return "Hello, World!"

if __name__ == '__main__':
    print("discord pingpong machine has been started!")
    app.run(host=settings["listenIP"], debug=settings["debugMode"], port=settings["port"])