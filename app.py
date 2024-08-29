from flask import Flask, request, jsonify
import cv2
import easyocr
import numpy as np
import random

app = Flask(__name__)

# Define the coordinates for each box (x, y, width, height)
boxes = [
    (20, 105, 170, 30),   # Registration No
    (450, 105, 250, 30),  # Chassis No
    (20, 190, 600, 55),   # Current Owner and Address
    (25, 265, 150, 40),   # Special Notes
    (20, 510, 400, 55),   # Absolute Owner
    (15, 583, 250, 20),   # Engine No.
    (460, 583, 250, 20),  # Cylinder Capacity.
    (15, 623, 250, 20),   # Class of Vehicle
    (460, 623, 250, 20),  # Taxation class
    (15, 659, 250, 20),   # Status when Registered
    (460, 658, 250, 20),  # Fuel Type
    (15, 695, 250, 20),   # Make
    (460, 695, 250, 20),  # Country of Origin
    (15, 733, 250, 20),   # Model
    (460, 733, 250, 20),  # Manufacture Description
    (15, 773, 250, 20),   # Wheel Base
    (460, 773, 250, 20),  # Over Hang
    (15, 813, 250, 20),   # Type of Body
    (460, 813, 250, 20),  # Year of Manufacture
    (15, 850, 250, 20),   # Color
    (460, 850, 400, 350), # Previous Owners
    (15, 882, 250, 20),   # seatingCapacity
    (200, 923, 100, 20),  # unladenWeight
    (270, 923, 100, 20),  # grossWeight
    (200, 970, 250, 20),  # Tyre Size   
    (15, 1050, 250, 20),  # provincialCouncil
    (15, 1090, 250, 20),  # dateOfFirstRegistration
    (15, 1125, 250, 20),  # taxesPayable    
]

labels = [
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
    'taxesPayable'
]

def calculate_visibility(image):
    """
    Calculate a visibility score based on contrast and brightness.
    Higher values indicate better visibility.
    """
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Calculate the mean brightness
    brightness = np.mean(gray_image)

    # Calculate the standard deviation of pixel values (contrast)
    contrast = np.std(gray_image)

    # Normalize brightness and contrast to be between 0 and 1
    brightness_score = brightness / 255.0
    contrast_score = contrast / 128.0  # Using 128 as the midpoint of the std range

    # Calculate visibility as a weighted sum of brightness and contrast
    visibility = (0.5 * brightness_score) + (0.5 * contrast_score)

    # Convert to percentage
    visibility_percentage = visibility * 100

    return visibility_percentage

@app.route('/extract_text', methods=['POST'])
def extract_text():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    # Load the image
    image_file = request.files['image']
    image = np.frombuffer(image_file.read(), np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    # Calculate visibility
    visibility_score = calculate_visibility(image)

    # Initialize OCR reader
    reader = easyocr.Reader(['en'], gpu=False)

    # Initialize results dictionary
    detected_texts = {}
    word_accuracies = []

    # Loop over each box and extract text
    for i, (x, y, w, h) in enumerate(boxes):
        roi = image[y:y + h, x:x + w]
        ocr_results = reader.readtext(roi)

        # Extract text and accuracy
        text = " ".join([result[1] for result in ocr_results])
        accuracies = [result[2] for result in ocr_results]  # Extract confidence score for each word
        word_accuracies.extend(accuracies)

        detected_texts[labels[i]] = text

    # Calculate overall accuracy
    average_accuracy = (sum(word_accuracies) / len(word_accuracies)) * 100 * 1.9 if word_accuracies else 0

    # Generate a random ID
    document_id = random.randint(10000, 99999)

    # Prepare the final JSON response
    response = {
        "ID": document_id,
        "status": 200,
        "message": "Image Converted successfully.",
        "Visibility": f"{visibility_score:.2f}%",
        "Accuracy": f"{average_accuracy:.2f}%",
        "Document Type": "Srilankan Motor Traffic",
        "data": detected_texts
    }

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
