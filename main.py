import logging
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
from usecases.summarizer_adapter.sum_basic import SumBasicSummarizerAdapter
from usecases.summarizer_adapter.text_rank import TextRankSummarizerAdapter

logger = logging.Logger('summarizer')
handler = logging.FileHandler(filename='summarizer.log')
formatter = logging.Formatter(fmt="[%(asctime)s] %(levelname)s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

supported_summarizers: Dict[SummarizerEnum, ISummarizerAdapter] = {
    SummarizerEnum.LEX_RANK: LexRankSummarizerAdapter(),
    SummarizerEnum.LSA: LSASummarizerAdapter(),
    SummarizerEnum.KL: KLSummarizerAdapter(),
    SummarizerEnum.TEXT_RANK: TextRankSummarizerAdapter(),
    SummarizerEnum.SUM_BASIC: SumBasicSummarizerAdapter(),
}

app = FastAPI(debug=True)


app.include_router(
    prefix="/api",
    tags=["summarizer"],
    router=SummarizerRouter(
        supported_summarizers=supported_summarizers,
        logger=logger
    )
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
