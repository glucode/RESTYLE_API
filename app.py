from flask import Flask, request, send_file
from flask import jsonify
import os
from flask_marshmallow import Marshmallow
import requests
from external_Files import generator 
from external_Files import clasification
import torch

app = Flask(__name__)
# Model
model = torch.load('pytorch_model.bin', map_location=torch.device('cpu'))

@app.route('/')
def default_hi():
    print("Hi, there!")
    return {"message": "Aloha"}


@app.route('/classify', methods=['POST'])
def classify():
    image=request.files['image']
    output = clasification.ClothingIdentifier.identify(image)
    return output,200

@app.route('/generate', methods=['GET'])
def generate():
    name = request.args.get('name')
    output = generator.Generator.start_genertation(name)
    return output,200

@app.route('/generate_html_list',methods=['GET'])
def generate_html_list():
    name = request.args.get('name')
    output = generator.Generator.start_genertation_html(name)
    return output,200


@app.route('/not_found')
def not_fount():
    return jsonify(message="That response was not found"), 404 


if __name__ == '__main__':
    app.run(debug=True,port=8001)
    
