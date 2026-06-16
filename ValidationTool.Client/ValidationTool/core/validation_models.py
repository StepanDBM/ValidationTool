from dataclasses import dataclass
from typing import List
from datetime import datetime

from core.validation_system import ValidationSeverity
from core.context.SceneContext.SceneSetupContext import SceneSetupContext

class ArtistDto:
    name: str
    id: str
    level: str
    lead: str
    team: str
    project: str
    slack_id: str
    teams_id: str
    gmail: str

@dataclass
class ValidationResult:
    artist: ArtistDto
    dcc: str
    origin_file: str
    object_name: str
    check_name: str
    stage: str
    timestamp: datetime
    severity: ValidationSeverity
    message: str
    suggestion: str = ""


@dataclass
class RunSummary:
    run_id: str
    timestamp: datetime
    dcc: str
    total_objects: int
    total_issues: int
    errors: int
    warnings: int
    infos: int


@dataclass
class ValidationRun:
    summary: RunSummary
    scene_setup: SceneSetupContext
    issues: List[ValidationResult]
    jsonPath: str
