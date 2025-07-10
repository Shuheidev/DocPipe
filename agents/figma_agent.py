from __future__ import annotations

from pathlib import Path
from typing import Tuple

from schemas import AgentResult, ArtefactType, UploadPayload

from .base import BaseAgent


class FigmaClient:
    async def create_project(self, payload: UploadPayload) -> Tuple[str, str]:
        return "https://figma.example/file", "https://figma.example/prototype"


class FigmaAgent(BaseAgent):
    name = "figma"

    def __init__(self, client: FigmaClient | None = None) -> None:
        self.client = client or FigmaClient()

    async def run(self, payload: UploadPayload) -> AgentResult:
        output_dir = payload.output_dir or Path("output")
        output_dir.mkdir(parents=True, exist_ok=True)
        file_url, prototype_url = await self.client.create_project(payload)
        data = {"file_url": file_url, "prototype_url": prototype_url}
        path = output_dir / "figma.json"
        path.write_text(str(data))
        return AgentResult(artefact_type=ArtefactType.FIGMA, path=path)
