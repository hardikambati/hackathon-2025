import requests
import easyocr
import re
from PIL import Image
from io import BytesIO

# def clean_text(text):
#     return ''.join(filter(str.isdigit, text))  #

# General regex to match digits with spaces in between
def detect_awb(url, awb_number, model):
    # General regex to match the sequence of digits with optional spaces
    # pattern = r"^" + r"\s*".join([re.escape(c) for c in awb_number]) + r"\s*$"

    # Download the image from S3
    response = requests.get(url)
    if response.status_code != 200:
        print("❌ Failed to download the image.")
        return False
    
    # Convert the image to RGB format
    # image = Image.open(BytesIO(response.content)).convert("RGB")

    results = model.readtext(url, detail=0)
    print("OCR Results:", results)
    def clean_text(text):
        # Remove spaces from the text
        cleaned_text = text.replace(" ", "")
        
        # Check if first and last characters are not a number or alphabet
        if not cleaned_text[0].isalnum():  # If the first character is not alphanumeric, remove it
            cleaned_text = cleaned_text[1:]
        
        if not cleaned_text[-1].isalnum():  # If the last character is not alphanumeric, remove it
            cleaned_text = cleaned_text[:-1]
        
        return cleaned_text

    # Check if any detected text matches the regex pattern
    for text in results:
        # \cleaned_text = text.replace(" ", "")
        cleaned_text = clean_text(text)  
        print(cleaned_text)
        if awb_number.lower() == cleaned_text:
            print(f"✅ Found matching sequence: {text}")
            return True, "AWB number matched"

    print("❌ No matching sequence found.")
    return False, "AWB number not matching"

# url = "https://pyck-res-bucket.s3.ap-southeast-1.amazonaws.com/shipment_pods/281921/2025-01-27/298976/1301649202.jpeg"
# awb_number = "1301649202"