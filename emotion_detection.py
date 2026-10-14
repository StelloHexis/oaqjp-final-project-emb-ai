import requests
import json

def emotion_detector(text_to_analyze):
    response = requests.post(
        url = (
        "https://sn-watson-emotion.labs.skills.network/"
        "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"),
        json={"rawDocument": {"text": text_to_analyze}},
        headers={"content-type": "application/json"}
    )

    if response.status_code == 400:
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None
        }
    

    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
    }

    input_json = {
        "raw_document": {
            "text": text_to_analyze
        }
    }

    response = requests.post(
        url,
        headers=headers,
        json=input_json
    )

    response_data = json.loads(response.text)

    emotion_scores = response_data["emotionPredictions"][0]["emotion"]

    emotions = {
        "anger": emotion_scores["anger"],
        "disgust": emotion_scores["disgust"],
        "fear": emotion_scores["fear"],
        "joy": emotion_scores["joy"],
        "sadness": emotion_scores["sadness"]
    }

    # Find the emotion with the highest score
    emotions["dominant_emotion"] = max(
        emotions,
        key=emotions.get
    )
    return emotions