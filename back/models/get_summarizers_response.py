from typing import List

from enums.summarizer_enum import SummarizerEnum
from pydantic import BaseModel


class SummarizerOption(BaseModel):
    name: str
    code: SummarizerEnum


class GetSummarizersResponse(BaseModel):
    summarizers: List[SummarizerOption]
