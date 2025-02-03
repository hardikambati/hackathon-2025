import os
import time
import requests


def download_image_locally(url: str):
    timestamp = int(time.time())
    local_file_path = f"image_{timestamp}.jpeg"

    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(local_file_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Image downloaded successfully: {local_file_path}")
        return True, local_file_path
    return False, "Couldn't download image locally"


def delete_image_locally(local_file_path: str):
    try:
        os.remove(local_file_path)
        print(f"File delete successfully")
    except Exception as e:
        print(f"Failed to delete image due to : {e}")


def detect_stamp(url: str, model):
    local_file_path = None
    try:
        status, local_file_path = download_image_locally(url)
        if not status:
            return False, "Image couldn't be downloaded. Please check format."
        result = model.predict(local_file_path, confidence=40, overlap=30).json()
        predictions = result.get("predictions")

        if predictions:
            confidence_list = []
            for instance in predictions:
                confidence_list.append(instance.get("confidence", 0))

            # TODO handle conditions where max_confidence is
            # below certain threshold
            max_confidence = max(confidence_list)

            return True, "Stamp Recognized"
        else:
            return False, "Stamp Not Recognized"
    except Exception as e:
        return False, str(e)
    finally:
        delete_image_locally(local_file_path)