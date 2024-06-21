from enums.summarizer_enum import SummarizerEnum
from pydantic import BaseModel


class PostSummarizerTextRequest(BaseModel):
    rows: int
    content: str
    summarizer: SummarizerEnum
    language: str
