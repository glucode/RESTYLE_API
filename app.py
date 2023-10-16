from flask import Flask, request, send_file
from flask import jsonify
import os
from flask_marshmallow import Marshmallow
import requests
from external_Files import generator

app = Flask(__name__)

# Classifier API
API_KEY = os.environ.get('BEARER_KEY')
API_URL = "https://api-inference.huggingface.co/models/timm/mobilenetv3_large_100.ra_in1k"
headers = {"Authorization": "Bearer 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"}

def query(filename):
    response = requests.post(API_URL, headers=headers, data=filename)
    return response.json()


@app.route('/')
def default_hi():
    print("Hi, there!")
    return {"message": "Aloha"}


@app.route('/classify', methods=['POST'])
def classify():
    mage=request.files['image']
    output = query(mage)
    return output,200

@app.route('/generate', methods=['GET'])
def generate():
    name = request.args.get('name')
    generated_result = generator.Generator.start_genertation(name)
    return generated_result


@app.route('/not_found')
def not_fount():
    return jsonify(message="That response was not found"), 404 


if __name__ == '__main__':
    app.run(debug=True,port=8001)
    
