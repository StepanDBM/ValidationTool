from core.context.baseContext import BaseContext
from core.validation_system import ValidationIssue, ValidationSeverity

from core.context.SceneStatsContext import SceneStatsContext

from core.checks.validation_check_ids import CHECK_SCENE_COMPLEXITY_SCORE

def check_scene_complexity_score(obj: BaseContext, runtime_ctx):
    if not isinstance(obj, SceneStatsContext):
        return None

    score = obj.total_meshes + obj.total_transforms + obj.total_references
    limit = getattr(runtime_ctx.budgets, "complexity_limit", 5000)

    if score > limit:
        return ValidationIssue(
            asset_name=obj.name,
            check_name=CHECK_SCENE_COMPLEXITY_SCORE,
            severity=ValidationSeverity.WARNING,
            message=f"High complexity score: {score}",
            suggestion="Optimize the scene."
        )