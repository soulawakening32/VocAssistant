class LocalEmotionDummyProvider:
    def load(self) -> None:
        return

    def detect(self, text: str) -> dict:
        return {
            "label": "neutral",
            "score": 1.0,
            "provider": "local_emotion_dummy",
        }