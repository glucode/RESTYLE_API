from flask import Flask, request, send_file
from flask import jsonify
import os
from flask_marshmallow import Marshmallow
import requests
from external_Files import generator 
from external_Files import clasification
from external_Files import transcoder
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# # Firebase init
# cred = credentials.Certificate("path/to/serviceAccountKey.json")
# firebase_admin.initialize_app(cred)
# firebase_db = firestore.client()



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
    # image = request.files['image']
    category = request.form['category']
    output = generator.Generator.start_genertation(category)
    return output,200

@app.route('/generate_userimage', methods=['GET'])
def generate_with_image():
    image = request.files['image']
    category = request.form['category']
    output = generator.Generator.generate_with_image(category,image)
    return output,200

@app.route('/generate_html_list',methods=['GET'])
def generate_html_list():
    name = request.args.get('name')
    output = generator.Generator.start_genertation_html(name)
    return output,200

@app.route('/remove_background',methods=['POST'])
def remove_background():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['image']

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Save the uploaded image to a temporary file
        upload_folder = "uploads"
        os.makedirs(upload_folder, exist_ok=True)
        temp_image_path = os.path.join(upload_folder, file.filename)
        file.save(temp_image_path)

        # Call the segment_image function with the saved file path
        segmented_image = transcoder.segment_image(temp_image_path)

        # Optionally, you can delete the temporary file if you no longer need it
        os.remove(temp_image_path)

        return jsonify({'segmented_image': "success"}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
   

@app.route('/not_found')
def not_fount():
    return jsonify(message="That response was not found"), 404 


if __name__ == '__main__':
    app.run(debug=True,port=8001)
    
