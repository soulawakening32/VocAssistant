class LocalFilesDummyProvider:
    def load(self) -> None:
        return

    def analyze(self, file_path: str) -> dict:
        return {
            "file_path": file_path,
            "result": None,
            "provider": "local_files_dummy",
        }