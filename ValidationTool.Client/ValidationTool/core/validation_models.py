from dataclasses import dataclass, field
from typing import List, Dict
from datetime import datetime

from core.validation_system import ValidationIssue


@dataclass
class StageResult:
    stage: str
    issues: List[ValidationIssue]
    has_errors: bool
    execution_time: float


@dataclass
class AssetValidationResult:
    asset_name: str
    stages: List[StageResult]
    total_issues: int
    has_errors: bool


@dataclass
class PipelineSummary:
    total_assets: int
    total_issues: int
    errors: int
    warnings: int
    infos: int


@dataclass
class ValidationRun:
    run_id: str
    timestamp: datetime
    dcc: str
    assets: List[AssetValidationResult]
    summary: PipelineSummary