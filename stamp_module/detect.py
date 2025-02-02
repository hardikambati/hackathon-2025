

def detect_stamp(url: str, model):
    try:
        # add extract image logic

        result = model.predict(url, confidence=40, overlap=30).json()
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
