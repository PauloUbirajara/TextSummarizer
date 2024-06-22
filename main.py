from typing import Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from enums.summarizer_enum import SummarizerEnum
from routers.summarizers import SummarizerRouter
from usecases.summarizer_adapter.base import ISummarizerAdapter
from usecases.summarizer_adapter.kl import KLSummarizerAdapter
from usecases.summarizer_adapter.lex_rank import LexRankSummarizerAdapter
from usecases.summarizer_adapter.lsa import LSASummarizerAdapter
from usecases.summarizer_adapter.text_rank import TextRankSummarizerAdapter

supported_summarizers: Dict[SummarizerEnum, ISummarizerAdapter] = {
    SummarizerEnum.LEX_RANK: LexRankSummarizerAdapter(),
    SummarizerEnum.LSA: LSASummarizerAdapter(),
    SummarizerEnum.KL: KLSummarizerAdapter(),
    SummarizerEnum.TEXT_RANK: TextRankSummarizerAdapter(),
}

app = FastAPI()
app.include_router(
    prefix="/api",
    tags=["summarizer"],
    router=SummarizerRouter(supported_summarizers=supported_summarizers)
    .create()
)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_origins=['*'],
    allow_headers=["*"],
)
app.mount(
    path='/',
    app=StaticFiles(directory="static", html=True),
    name="static"
)
