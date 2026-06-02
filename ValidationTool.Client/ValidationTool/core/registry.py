from typing import List, Callable, Optional
from dataclasses import dataclass, field
import config.exec_stages as excS
from core.validation_system import MeshContext, ValidationIssue

from config.validation_profile import ValidationProfile

<<<<<<< HEAD
from core.validation_context import ValidationRuntimeContext

MeshCheckFunction = Callable[[MeshContext, ValidationRuntimeContext], List[ValidationIssue]]
=======
MeshCheckFunction = Callable[[MeshContext], List[ValidationIssue]]
>>>>>>> 468b7944f2988c013412ee180b8655c75792e8d7

@dataclass
class StageResult:
    stage: str
    issues: List[ValidationIssue]
    has_errors: bool

@dataclass(frozen=True)
class CheckDefinition:
    func: MeshCheckFunction
    id: str
    category: str = "uncategorized"
    stage: str = "geometry"
    tags: List[str] = field(default_factory=list)
    enabled: bool = True

class MeshValidatorRegistry:
    def __init__(self):
        self.by_id: dict[str, CheckDefinition] = {}
        self.by_category: dict[str, list[CheckDefinition]] = {}
        self.by_stage: dict[str, list[CheckDefinition]] = {}

    def register(
        self,
        check: MeshCheckFunction,
        check_id: str = None,
        category: str = "uncategorized",
        stage: str = "geometry",
        tags: Optional[List[str]] = None
    ):
        definition = CheckDefinition(
            func=check,
            id=check_id or check.__name__,
            category=category,
            stage=stage,
            tags=tags or []
        )

        self.by_id[definition.id] = definition

        if definition.category not in self.by_category:
            self.by_category[definition.category] = []
        self.by_category[definition.category].append(definition)

        if stage not in self.by_stage:
            self.by_stage[stage] = []

        self.by_stage[stage].append(definition)

    def get_all(self) -> list[CheckDefinition]:
        return list(self.by_id.values())
    
    def resolve(self, profile: ValidationProfile) -> list[CheckDefinition]:
        if not profile.enabled_categories:
            return self.get_all()

        checks = []
        for cat in profile.enabled_categories:
            checks.extend(self.by_category.get(cat, []))

        return checks
    
    def resolveByProfileStage(self, profile):

        ordered_checks = []

        for stage in excS.EXECUTION_STAGES:

            stage_checks = self.by_stage.get(stage, [])
            for check in stage_checks:
                if profile.allows_category(check.category):
                    ordered_checks.append(check)

        return ordered_checks