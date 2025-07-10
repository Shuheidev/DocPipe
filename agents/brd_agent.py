from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from schemas import AgentResult, ArtefactType, UploadPayload

from .base import BaseAgent


class BrdAgent(BaseAgent):
    name = "brd"

    async def run(self, payload: UploadPayload) -> AgentResult:
        output_dir = payload.output_dir or Path("output")
        output_dir.mkdir(parents=True, exist_ok=True)
        loader = FileSystemLoader(Path(__file__).parent.parent / "prompts")
        env = Environment(loader=loader)
        template = env.get_template("brd_prompt.jinja2")
        content = template.render(
            project_name=payload.project_name,
            description=payload.description,
        )
        path = output_dir / "BRD.md"
        path.write_text(content)
        return AgentResult(artefact_type=ArtefactType.BRD, path=path)
