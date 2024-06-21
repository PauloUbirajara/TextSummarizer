from pydantic import BaseModel


class PostSummarizerTextResponse(BaseModel):
    summary: list[str]
