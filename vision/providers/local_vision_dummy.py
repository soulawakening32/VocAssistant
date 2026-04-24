class LocalVisionDummyProvider:
    def load(self) -> None:
        return

    def analyze(self, image_path: str) -> dict:
        return {
            "image_path": image_path,
            "result": None,
            "provider": "local_vision_dummy",
        }