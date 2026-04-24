class LocalWebDummyProvider:
    def load(self) -> None:
        return

    def search(self, query: str) -> dict:
        return {
            "query": query,
            "results": [],
            "provider": "local_web_dummy",
        }