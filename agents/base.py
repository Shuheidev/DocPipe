from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
from functools import wraps
from typing import Callable, TypeVar

from schemas import AgentResult, UploadPayload

F = TypeVar("F", bound=Callable)


def retry(max_attempts: int = 3, base_delay: float = 0.5) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            attempt = 0
            delay = base_delay
            while True:
                try:
                    return await func(*args, **kwargs)
                except Exception:
                    attempt += 1
                    if attempt >= max_attempts:
                        raise
                    await asyncio.sleep(delay)
                    delay *= 2
        return wrapper  # type: ignore

    return decorator


class BaseAgent(ABC):
    name: str

    @abstractmethod
    async def run(self, payload: UploadPayload) -> AgentResult:
        ...

    async def execute(self, payload: UploadPayload) -> AgentResult:
        @retry()
        async def _run() -> AgentResult:
            return await self.run(payload)

        return await _run()
