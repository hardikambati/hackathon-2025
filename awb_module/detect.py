import requests
import easyocr
import re
from PIL import Image
from io import BytesIO


class PODHelper:

    def __init__(self, url, model):
        response = requests.get(url)
        if response.status_code != 200:
            print("❌ Failed to download the image.")
           
        # Convert the image to RGB format
        image = Image.open(BytesIO(response.content)).convert("RGB")

        self.results = model.readtext(url, detail=0)
        print("OCR Results:", self.results)

    def clean_text_awb(self,text):
        # Remove spaces from the text
        cleaned_text = text.replace(" ", "")
        if not cleaned_text:
            return ""
        # Check if first and last characters are not a number or alphabet
        # print(cleaned_text)
        if not cleaned_text[0].isalnum():  # If the first character is not alphanumeric, remove it
            cleaned_text = cleaned_text[1:]
        if not cleaned_text:
            return ""
        if not cleaned_text[-1].isalnum():  # If the last character is not alphanumeric, remove it
            cleaned_text = cleaned_text[:-1]
        
        return cleaned_text

    def is_awb_present(self,awb_number):

        for text in self.results:
            cleaned_text = self.clean_text_awb(text)  
            if awb_number.lower() == cleaned_text:
                print(f"✅ Found matching sequence: {text}")
                return True
        return False
    
    def is_phone_number_present(self, phone_number):
        for text in self.results:
            cleaned_text = self.clean_text_awb(text)  
            if phone_number.lower() == cleaned_text:
                print(f"✅ Found matching sequence: {text}")
                return True
        return False
    
    def is_consignee_name_present(self, consignee_name):
        for text in self.results:
            cleaned_text = self.clean_text_awb(text)  
            if consignee_name.lower() == cleaned_text:
                print(f"✅ Found matching sequence: {text}")
                return True
        return False
    
    def is_address_present(self, address):
        final_result = []
        for addr_txt in address:
            for text in self.results:
                cleaned_text = self.clean_text_awb(text)  
                if addr_txt.lower() == cleaned_text:
                    print(f"✅ Found matching sequence: {text}")
                    final_result.append(True)
                else:
                    final_result.append(False)
        if len(final_result) < 0.6 * len(address):  # Check if `final_result` is less than 60% of `address`
            return False
        return True