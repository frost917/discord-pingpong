from flask import Flask, jsonify, request

app = Flask(__name__)
app.debug = True

@app.route('/', methods=['POST'])
def ping():
    if request.json["type"] == 1:
        return jsonify({
            "type": 1
        })
    
@app.route('/', methods=['GET'])
def hello():
    return "Hello, World!"
    

if __name__ == '__main__'
    app.run()