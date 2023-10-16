from flask import Flask, request, send_file
from flask import jsonify
import os
from flask_marshmallow import Marshmallow

app = Flask(__name__)

@app.route('/')
def default_hi():
    print("Hi, there!")
    return {"message": "Aloha"}


@app.route('/not_found')
def not_fount():
    return jsonify(message="That response was not found"), 404 

if __name__ == '__main__':
    app.run(debug=True)
