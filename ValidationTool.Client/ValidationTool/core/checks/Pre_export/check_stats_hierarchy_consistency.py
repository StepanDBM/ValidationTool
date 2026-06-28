from core.context.baseContext import BaseContext
from core.validation_system import ValidationIssue, ValidationSeverity

from core.context.SceneStatsContext import SceneStatsContext

from core.checks.validation_check_ids import CHECK_STATS_HIERARCHY_CONSISTENCY

def check_stats_hierarchy_consistency(obj: BaseContext, runtime_ctx):
    """
    Requires runtime_ctx to provide reference to hierarchy context.
    """
    if not isinstance(obj, SceneStatsContext):
        return None

    hierarchy_ctx = getattr(runtime_ctx, "scene_hierarchy", None)

    if not hierarchy_ctx:
        return None

    if obj.total_transforms != len(hierarchy_ctx.all_transforms):
        return ValidationIssue(
            asset_name=obj.name,
            check_name=CHECK_STATS_HIERARCHY_CONSISTENCY,
            severity=ValidationSeverity.WARNING,
            message="Mismatch between stats transforms and hierarchy count.",
            suggestion="Recalculate or fix hierarchy inconsistencies."
        )