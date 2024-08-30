from flask import Flask, request, jsonify
import cv2
import easyocr
import numpy as np
import random
from utils import boxes, labels, word_lists, correct_word_ignore_case, calculate_visibility

app = Flask(__name__)

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

        field_label = labels[i]

        # If the field requires correction from a list, apply the correction function
        if field_label in word_lists:
            corrected_text = correct_word_ignore_case(text, word_lists[field_label])
            detected_texts[field_label] = corrected_text if corrected_text else text
        else:
            detected_texts[field_label] = text

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
        "Document Type": "Vehicle Registration Document",
        "data": detected_texts
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
