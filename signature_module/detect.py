# sample images

# image_path = "https://static.vecteezy.com/system/resources/previews/000/537/670/non_2x/manual-signature-for-documents-on-white-background-hand-drawn-calligraphy-lettering-vector-illustration.jpg"
# image_path = "https://pyck-res-bucket.s3.ap-southeast-1.amazonaws.com/shipment_pods/281921/2025-01-28/298976/1301649055.jpeg"
# image_path = "https://pyck-res-bucket.s3.ap-southeast-1.amazonaws.com/shipment_pods/281921/2025-01-27/298976/1301649202.jpeg"


def detect_signature(url: str, model):
    try:
        results = model(url)
        if results and len(results[0].boxes) > 0:
            confidences = results[0].boxes.conf.tolist()
            max_confidence = max(confidences)
            print(f"Signature detected with confidence: {max_confidence:.2f}")
            return True, "Signature detected"
        return False, "No signature detected"
    except Exception as e:
        return False, str(e)
