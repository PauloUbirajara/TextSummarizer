class ISummarizerAdapter:
    def summarize(self, text: str, sentence_count: int, language: str) -> list[str]:
        ...