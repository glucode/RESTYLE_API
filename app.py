from flask import Flask, request, send_file
from flask import jsonify
import os
from flask_marshmallow import Marshmallow
import requests
from external_Files import generator 
from external_Files import clasification, transcoder, colourExtractor
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)


@app.route('/')
def default_hi():
    print("Hi, there!")
    return {"message": "Aloha"}


@app.route('/extract_colour')
def extract_colour():
     if 'image' not in request.files:
            return jsonify({'error': 'No file part'}), 400

     file = request.files['image']
     
     if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
     upload_folder = "uploads"
     os.makedirs(upload_folder, exist_ok=True)
     temp_image_path = os.path.join(upload_folder, file.filename)
     file.save(temp_image_path)

     dominant_colors = colourExtractor.extract_dominant_colors(temp_image_path)
     os.remove(temp_image_path)
     
     return {'Dominant colours': dominant_colors}, 200
 

@app.route('/classify', methods=['POST'])
def classify():
    image=request.files['image']
    output = clasification.ClothingIdentifier.identify(image)
    return output,200

@app.route('/generate', methods=['GET'])
def generate():
    name = request.args.get('name')
    style = request.args.get('style')
    output = generator.Generator.start_genertation(categoryName=name, preset=style)
    return output,200

@app.route('/generate_userimage', methods=['GET'])
def generate_with_image(): #handle potential of no images
    image = request.files['image']
    category = request.form['category']
    output = generator.Generator.generate_with_image(category,image)
    return output,200

@app.route('/generate_html_list',methods=['GET'])
def generate_html_list():
    name = request.args.get('name')
    style = request.args.get('style')
    output = generator.Generator.start_genertation_html(categoryName=name, preset=style)
    return output,200

@app.route('/remove_background',methods=['POST'])
def remove_background():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Save the uploaded image to a temporary file beacuse it needs to be saved for this functino to work
        upload_folder = "uploads"
        os.makedirs(upload_folder, exist_ok=True)
        temp_image_path = os.path.join(upload_folder, file.filename)
        file.save(temp_image_path)

        segmented_image = transcoder.segment_image(temp_image_path)

        # Delete the temporary file if you no longer need it
        os.remove(temp_image_path)
        dominant_colors = colourExtractor.extract_dominant_colors(temp_image_path)
        return jsonify({'segmented_image': "success"}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/add_to_wardrobe',methods=['POST'])
def add_to_wardrobe():
    """
    Add a new item to the wardobe 
    
    Process:
    - The background will be removed
    - Items will be deep tagged
    - Extract colors from the item
    - Find a matching item in our database to fill in the missig attributes 
        
    Output:
    - Saves file to the database
    """
    return jsonify(message= 'success')
    


@app.route('/not_found')
def not_fount():
    return jsonify(message="That response was not found"), 404 


if __name__ == '__main__':
    app.run(debug=True,port=8001)
    
