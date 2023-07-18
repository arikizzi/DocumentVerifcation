from flask import Flask, request, jsonify
from flask_cors import CORS
import easyocr
from PIL import Image, ImageOps
import re
import json
import numpy as np

app = Flask(__name__)
CORS(app)

@app.route('/extract_aadhar', methods=['POST'])
def extract_aadhar():
    print("Route /extract_aadhar")
    image_file = request.files['aadhar']
    image = Image.open(image_file)
    text = extract_aadhar_details(image)
    json_data = json.dumps(text)
    return json_data


@app.route('/extract_pan', methods=['POST'])
def extract_pan():
    print("Route /extract_pan")
    image_file = request.files['pan']
    image = Image.open(image_file)
    text = extract_pan_details(image)
    json_data = json.dumps(text)
    return json_data


@app.route('/extract_cheque', methods=['POST'])
def extract_cheque():
    print("Route /extract_cheque")
    image_file = request.files["cheque"]
    image = Image.open(image_file)

    text = extract_cheque_details(image)
    json_data = json.dumps(text)
    print(json_data)
    return json_data


def extract_aadhar_details(image):
    # Initialize the EasyOCR reader
    reader = easyocr.Reader(['en'])

    #Loading the image as an array
    image_np = np.asarray(image)

    # Perform OCR
    results = reader.readtext(image_np)

    data = {
    "name": "none",
    "dob": "none",
    "gender": "none",
    "aadhar_number":"none"
    }
    

    text_list = [entry[1] for entry in results]
    if len(text_list) == 0:
        return data
    print(text_list)


    aadhar_regex = r'\d{4} \d{4} \d{4}'
    name_regex = r"^(?:(?=\b[A-Z][a-z]{2,}\b)[A-Z][a-z]*\s?)+$"
    dob_regex = r'\b\d{2}/\d{2}/\d{4}\b'
    gender_regex = r'\b(?:MALE|FEMALE|Male|Female)\b'

    for text in text_list:
        if re.match(name_regex, text):
            data["name"] = text
            break

    for text in text_list:
        if re.search(dob_regex, text):
            data["dob"] = re.search(dob_regex, text).group()
            
        if re.search(gender_regex, text):
            data["gender"] = re.search(gender_regex, text).group()
            
        if re.match(aadhar_regex, text):
            data["aadhar_number"] = text

    return data


def extract_pan_details(image):
    # Initialize the EasyOCR reader
    reader = easyocr.Reader(['en'])

    #Loading the image as an array
    image_np = np.asarray(image)

    # Perform OCR
    results = reader.readtext(image_np)

    data = {
    "name": "none",
    "dob": "none",
    "pan_number":"none"
    }

    text_list = [entry[1] for entry in results]
    if len(text_list) == 0:
        return data
    print(text_list)

    

    name_regex = r'(?<!\w)(?!.*\bincome tax\b)[A-Z][A-Z\s](?:[A-Z][A-Z\s])*(?!\w)'
    dob_regex = r'\b\d{2}[-/]\d{2}[-/]\d{4}\b'
    pan_regex = r'\b[A-Z]{5}\d{4}[A-Z]\b'

    # name = "none"
    dob = "none"
    pan_number = "none"

    names = []

    for text in text_list:
        if re.match(name_regex, text):
            names.append(text)
        if re.search(dob_regex, text):
            dob = re.search(dob_regex, text).group()
        if re.match(pan_regex, text):
            pan_number = text

    data["name"] = names[-2]
    data["dob"] = dob
    data["pan_number"] = pan_number
    
    return data


def extract_cheque_details(image):
    # Initialize the EasyOCR reader
    reader = easyocr.Reader(['en'])

    #Loading the image as an array
    image_np = np.asarray(image)

    # Perform OCR
    results = reader.readtext(image_np)

    data = {
    "ifsc": "none",
    "acc_no": "none"
    }

    text_list = [entry[1] for entry in results]
    if len(text_list) == 0:
        return data
    print(text_list)

    

    ifsc_regex = r"^[A-Z]{4}[A-Z0-9]{7}$"
    acc_no_regex = r"^\d{10,16}$"

    for text in text_list:
        if re.match(ifsc_regex, text):
            data["ifsc"] = text
       
        if re.match(acc_no_regex, text):
            data["acc_no"] = text

    return data


if __name__ == '__main__':
    app.run(
        host = "0.0.0.0", 
        port = 8000)