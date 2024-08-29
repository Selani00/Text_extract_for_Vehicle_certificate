from flask import Flask, request, jsonify
import cv2
import easyocr
import numpy as np


app = Flask(__name__)

boxes = [
    (20, 105, 170,30),   #  Registration No
    (450, 105, 250,30),  #  Chassis No
    (20, 190, 600, 55),  #  Current Owner and Address
    (25, 265, 150, 40),  #  Special Notes
    (20, 510, 400, 55),  # Absolute Owner
    (15, 583, 250, 20),  # Engine No.
    (460,583, 250, 20),  # Cylinder Capacity.
    (15, 623, 250, 20),  # Class of Vehicle
    (460, 623, 250, 20),  # Taxation class
    (15, 659, 250, 20),  # Status when Registered
    (460, 658, 250, 20),  # Fuel Type
    (15, 695, 250, 20),  # Make
    (460, 695, 250, 20),  # Country of Origin
    (15, 733, 250, 20),  # Model
    (460,  733, 250, 20),  # Manufacture Description
    (15, 773, 250, 20),  # Wheel Base
    (460, 773, 250, 20),  # Over Hang
    (15, 813, 250, 20),  # Type of Body
    (460, 813, 250, 20),  # Year of Manufacture
    (15, 850, 250, 20),  # Color
    (460, 850, 400, 350),  # Previous Owners
    (15, 882, 250, 20),  # seatingCapacity
    (200, 923, 100, 20),  # unladenWeight
    (270, 923, 100, 20),  # grossWeight
    (200, 970, 250, 20),  # Tyre Size   
    (15, 1050, 250, 20),  # provincialCouncil
    (15, 1090, 250, 20),  # dateOfFirstRegistration
    (15, 1125, 250, 20),  # taxesPayable    
]

labels= [
    'Registration No',
    'Chassis No',
    'Current Owner and Address',
    'Special Notes',
    'Absolute Owner',
    'Engine No.',
    'Cylinder Capacity',
    'Class of Vehicle',
    'Taxation class',
    'Status when Registered',
    'Fuel Type',
    'Make',
    'Country of Origin',
    'Model',
    'Manufacture Description',
    'Wheel Base',
    'Over Hang',
    'Type of Body',
    'Year of Manufacture',
    'Color',
    'Previous Owners',
    'seatingCapacity',
    'unladenWeight',
    'grossWeight',
    'Tyre Size',
    'provincialCouncil',
    'dateOfFirstRegistration',
    'taxesPayable']

@app.route('/extract_text', methods=['POST'])
def extract_text():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files['image']
    image = np.fromstring(image_file.read(), np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    detected_texts = {}

    for i, (x, y, w, h) in enumerate(boxes):
        roi = image[y:y + h, x:x + w]
        reader = easyocr.Reader(['en'], gpu=False)
        text = reader.readtext(roi)
        text = " ".join([result[1] for result in text])
        detected_texts[labels[i]] = text

    return jsonify(detected_texts)

if __name__ == '__main__':
    app.run(debug=True)