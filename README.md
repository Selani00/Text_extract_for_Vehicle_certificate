# Flask OCR API

This project provides a Flask-based API for Optical Character Recognition (OCR) that extracts text from specific regions of an image. 
It uses EasyOCR and OpenCV for image processing and text extraction. 
The API takes an image as input and returns the extracted text in JSON format.

## Setup Instructions

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash 
https://github.com/Selani00/Text_extract_for_Vehicle_certificate.git
cd Text_extract_for_Vehicle_certificate
```

### 2. Create a Virtual Environment

```git 
python -m venv venv
```
### 3. Activate the Virtual Environment

```git
venv\Scripts\activate
```
### 4. Install Dependencies

```git
pip install -r requirements.txt
```
### 5. Run the Flask API

```bash
python app.py
```

### 6. Test the App

 - Go to the Postman and open the POST request. 
 - Set the URL to http://127.0.0.1:5000/extract_text.

```bash
http://127.0.0.1:5000/extract_text
```

 - Under the Body tab, select form-data.
 - Add a key named 'image', set its type to File, and upload your image file.
 - Send the request.






