import asyncio
import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))  # noqa: E402

from agents import (  # noqa: E402
    BrdAgent,
    FigmaAgent,
    SolutionAgent,
    StoryAgent,
)

from agents.figma_agent import FigmaClient  # noqa: E402
from agents.story_agent import JiraClient  # noqa: E402
from schemas import ArtefactType, UploadPayload  # noqa: E402


class DummyFigma(FigmaClient):
    async def create_project(self, payload: UploadPayload):
        return "file", "prototype"


class DummyJira(JiraClient):
    async def create_stories(self, yaml_path: Path):
        return None


@pytest.mark.asyncio
async def test_agents(tmp_path: Path):
    payload = UploadPayload(
        project_name="Test",
        description="Desc",
        output_dir=tmp_path,
    )
    figma = FigmaAgent(DummyFigma())
    jira = StoryAgent(DummyJira())
    agents = [BrdAgent(), SolutionAgent(), figma, jira]
    results = await asyncio.gather(*(a.execute(payload) for a in agents))
    types = {r.artefact_type for r in results}
    expected = {
        ArtefactType.BRD,
        ArtefactType.SOLUTION,
        ArtefactType.FIGMA,
        ArtefactType.BACKLOG,
    }
    assert types == expected
    for r in results:
        assert r.path.exists()
