from __future__ import annotations

import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import cast

from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from agents import BrdAgent, FigmaAgent, SolutionAgent, StoryAgent
from schemas import AgentResult, UploadPayload

logger = logging.getLogger(__name__)

router = APIRouter()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)


def timestamp_dir() -> Path:
    ts = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    out = Path("output") / ts
    out.mkdir(parents=True, exist_ok=True)
    return out


@router.post("/generate")
async def generate(payload: UploadPayload) -> list[AgentResult]:
    out_dir = timestamp_dir()
    payload.output_dir = out_dir
    agents = [BrdAgent(), SolutionAgent(), FigmaAgent(), StoryAgent()]
    tasks = [a.execute(payload) for a in agents]
    raw_results: list[AgentResult | BaseException] = await asyncio.gather(
        *tasks, return_exceptions=True
    )
    results: list[AgentResult] = []
    for agent, res in zip(agents, raw_results):
        if isinstance(res, BaseException):
            logger.exception("Agent %s failed", agent.name, exc_info=res)
            raise HTTPException(
                status_code=500,
                detail=f"Agent {agent.name} failed: {res}",
            )
        results.append(cast(AgentResult, res))
    github = GitHubClient()
    await github.create_pr(out_dir)
    return results


class GitHubClient:
    async def create_pr(self, path: Path) -> str:
        return "https://github.com/example/pr"
