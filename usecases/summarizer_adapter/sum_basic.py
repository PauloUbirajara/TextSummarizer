from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.sum_basic import SumBasicSummarizer

from usecases.summarizer_adapter.base import ISummarizerAdapter


class SumBasicSummarizerAdapter(ISummarizerAdapter):
    def summarize(self, text: str, sentence_count: int, language: str) -> list[str]:
        parser = PlaintextParser(
            text=text,
            tokenizer=Tokenizer(language=language)
        )
        summarizer = SumBasicSummarizer()
        summary = summarizer(
            document=parser.document,
            sentences_count=sentence_count
        )
        return [str(row) for row in summary]

    def __str__(self) -> str:
        return "SumBasic"
