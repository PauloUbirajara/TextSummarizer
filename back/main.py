from typing import Dict

from enums.summarizer_enum import SummarizerEnum
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.summarizers import SummarizerRouter
from usecases.summarizer_adapter.base import ISummarizerAdapter
from usecases.summarizer_adapter.lex_rank import LexRankSummarizerAdapter

supported_summarizers: Dict[SummarizerEnum, ISummarizerAdapter] = {
    SummarizerEnum.LEX_RANK: LexRankSummarizerAdapter()
}

app = FastAPI()
app.include_router(
    SummarizerRouter(supported_summarizers=supported_summarizers)
    .create()
)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_origins=['*'],
    allow_headers=["*"],
)
