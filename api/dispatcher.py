from __future__ import annotations

import asyncio
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, FastAPI

from agents import BrdAgent, FigmaAgent, SolutionAgent, StoryAgent
from schemas import AgentResult, UploadPayload

router = APIRouter()
app = FastAPI()
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
    results = await asyncio.gather(*(a.execute(payload) for a in agents))
    github = GitHubClient()
    await github.create_pr(out_dir)
    return results


class GitHubClient:
    async def create_pr(self, path: Path) -> str:
        return "https://github.com/example/pr"
