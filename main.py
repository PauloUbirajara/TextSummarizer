from typing import Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from enums.summarizer_enum import SummarizerEnum
from routers.summarizers import SummarizerRouter
from usecases.summarizer_adapter.base import ISummarizerAdapter
from usecases.summarizer_adapter.lex_rank import LexRankSummarizerAdapter
from usecases.summarizer_adapter.lsa import LSASummarizerAdapter

supported_summarizers: Dict[SummarizerEnum, ISummarizerAdapter] = {
    SummarizerEnum.LEX_RANK: LexRankSummarizerAdapter(),
    SummarizerEnum.LSA: LSASummarizerAdapter(),
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

app.mount('/', StaticFiles(directory="static", html=True), name="static")
