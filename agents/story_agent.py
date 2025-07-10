from __future__ import annotations

from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader

from schemas import AgentResult, ArtefactType, UploadPayload

from .base import BaseAgent


class JiraClient:
    async def create_stories(self, yaml_path: Path) -> None:
        return None


class StoryAgent(BaseAgent):
    name = "story"

    def __init__(self, jira: JiraClient | None = None) -> None:
        self.jira = jira or JiraClient()

    async def run(self, payload: UploadPayload) -> AgentResult:
        output_dir = payload.output_dir or Path("output")
        output_dir.mkdir(parents=True, exist_ok=True)
        loader = FileSystemLoader(Path(__file__).parent.parent / "prompts")
        env = Environment(loader=loader)
        template = env.get_template("story_prompt.jinja2")
        content = template.render(
            project_name=payload.project_name,
            description=payload.description,
        )
        path = output_dir / "epics_userstories.yaml"
        yaml_data = yaml.safe_load(content)
        path.write_text(yaml.safe_dump(yaml_data))
        await self.jira.create_stories(path)
        return AgentResult(artefact_type=ArtefactType.BACKLOG, path=path)
