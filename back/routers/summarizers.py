from time import sleep
from typing import Dict

from enums.summarizer_enum import SummarizerEnum
from fastapi import APIRouter
from models.get_summarizers_response import (GetSummarizersResponse,
                                             SummarizerOption)
from models.post_summarizer_text_request import PostSummarizerTextRequest
from models.post_summarizer_text_response import PostSummarizerTextResponse
from routers.base import IAPIRouter
from usecases.summarizer_adapter.base import ISummarizerAdapter


class SummarizerRouter(IAPIRouter):
    supported_summarizers: Dict[SummarizerEnum, ISummarizerAdapter]

    def __init__(self, supported_summarizers: Dict[SummarizerEnum, ISummarizerAdapter]):
        self.supported_summarizers = supported_summarizers

    def create(self) -> APIRouter:
        router = APIRouter(prefix="/summarizers")

        @router.get('/')
        def get_summarizers() -> GetSummarizersResponse:
            sleep(1)
            return GetSummarizersResponse(
                summarizers=[
                    SummarizerOption(name=str(summ), code=key)
                    for key, summ in self.supported_summarizers.items()
                ]
            )

        @router.post('/text')
        def summarize_text(body: PostSummarizerTextRequest) -> PostSummarizerTextResponse:
            summarizer = self.supported_summarizers.get(body.summarizer)

            if summarizer is None:
                # Could not find implemented summarizers through request summarizer code
                raise KeyError("Summarizer not supported")

            summary = summarizer.summarize(
                text=body.content,
                sentence_count=body.rows
            )
            return PostSummarizerTextResponse(summary=summary)

        return router
