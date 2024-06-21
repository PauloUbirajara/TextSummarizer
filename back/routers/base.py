from fastapi import APIRouter


class IAPIRouter:
    def create(self) -> APIRouter:
        ...
