import logging
from typing import Dict

from fastapi import APIRouter

from enums.summarizer_enum import SummarizerEnum
from models.get_summarizers_response import (GetSummarizersResponse,
                                             SummarizerOption)
from models.post_summarizer_text_request import PostSummarizerTextRequest
from models.post_summarizer_text_response import PostSummarizerTextResponse
from routers.base import IAPIRouter
from usecases.summarizer_adapter.base import ISummarizerAdapter


class SummarizerRouter(IAPIRouter):
    supported_summarizers: Dict[SummarizerEnum, ISummarizerAdapter]
    logger: logging.Logger

    def __init__(
        self,
        supported_summarizers: Dict[SummarizerEnum, ISummarizerAdapter],
        logger: logging.Logger
    ):
        self.supported_summarizers = supported_summarizers
        self.logger = logger

    def create(self) -> APIRouter:
        router = APIRouter(prefix="/summarizers")

        @router.get('')
        def get_summarizers() -> GetSummarizersResponse:
            summarizers = [
                SummarizerOption(name=str(summ), code=key)
                for key, summ in self.supported_summarizers.items()
            ]
            self.logger.info({"summarizers": summarizers})
            return GetSummarizersResponse(
                summarizers=summarizers
            )

        @router.post('/text')
        def summarize_text(body: PostSummarizerTextRequest) -> PostSummarizerTextResponse:
            summarizer = self.supported_summarizers.get(body.summarizer)
            self.logger.info({
                "summarizer": summarizer,
                "body": body.model_dump_json()
            })

            if summarizer is None:
                # Could not find implemented summarizers through request summarizer code
                self.logger.error({
                    "summarizer": body.summarizer,
                    "supported_summarizers": self.supported_summarizers
                })
                raise KeyError("Summarizer not supported")

            summary = summarizer.summarize(
                text=body.content,
                sentence_count=body.rows,
                language=body.language
            )
            return PostSummarizerTextResponse(summary=summary)

        return router
