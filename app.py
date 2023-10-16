from flask import Flask, request, send_file
from flask import jsonify
import os
from flask_marshmallow import Marshmallow
import requests

app = Flask(__name__)

# Classifier API
API_URL = "https://api-inference.huggingface.co/models/timm/mobilenetv3_large_100.ra_in1k"
headers = {"Authorization": "Bearer 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"}


@app.route('/')
def default_hi():
    print("Hi, there!")
    return {"message": "Aloha"}

@app.route('/classify')
def classify(request):
    data=request.FILES['image']
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json(), 200

@app.route('/not_found')
def not_fount():
    return jsonify(message="That response was not found"), 404 

if __name__ == '__main__':
    app.run(debug=True)