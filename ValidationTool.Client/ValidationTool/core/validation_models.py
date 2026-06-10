from dataclasses import dataclass
from typing import List
from datetime import datetime

from core.validation_system import ValidationSeverity

@dataclass
class AssetValidationResult:
    artist: str
    dcc: str
    originFile: str
    asset_name: str
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
    issues: List[AssetValidationResult]
    jsonPath: str
