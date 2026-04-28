class VectorStore:
    def __init__(self):
        self.index = []

    def ingest(self, text: str, metadata: dict):
        self.index.append({'text': text, 'metadata': metadata})

    def query(self, query_text: str, top_k: int = 5):
        results = sorted(self.index, key=lambda item: query_text in item['text'], reverse=True)
        return results[:top_k]
