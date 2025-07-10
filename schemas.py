from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field


class ArtefactType(str, Enum):
    BRD = "BRD"
    SOLUTION = "SOLUTION"
    FIGMA = "FIGMA"
    BACKLOG = "BACKLOG"


class UploadPayload(BaseModel):
    project_name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    output_dir: Optional[Path] = None


class AgentResult(BaseModel):
    artefact_type: ArtefactType
    path: Path

    class Config:
        json_encoders = {Path: str}
