from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/',methods=['POST'])
def chat():
    temp = request.get_json()
    print(temp)
    resp = {
        "version":"2.0",
        "template":{
            "outputs":[
                {
                    "simpleText":{
                        "text":"Responce"
                    }
                }
            ]
        }
    }
    resp['template']['outputs'][0]['simpleText']['text']=str(temp)
    return jsonify(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)
