# checks/check_uvs.py

from typing import List

from core.validation_context import ValidationRuntimeContext
from core.validation_system import (
    ObjectContext,
    ValidationIssue,
    ValidationSeverity,
    CHECK_UV_SETS
)


MAX_UV_SETS = 2


def check_uv_sets(mesh: ObjectContext, runtime_ctx: ValidationRuntimeContext) -> List[ValidationIssue]:

    issues = []

    uv_sets = mesh.uv_sets or []

    # ----------------------------------------
    # Missing UV0
    # ----------------------------------------

    if not mesh.has_uv0:

        issues.append(
            ValidationIssue(
                asset_name=mesh.name,
                check_name=CHECK_UV_SETS,
                severity=ValidationSeverity.ERROR,
                message="Missing primary UV set (UV0).",
                suggestion="Create a valid UV layout."
            )
        )

    # ----------------------------------------
    # Missing UV1
    # Optional depending on pipeline
    # ----------------------------------------

    if not mesh.has_uv1:

        issues.append(
            ValidationIssue(
                asset_name=mesh.name,
                check_name=CHECK_UV_SETS,
                severity=ValidationSeverity.INFO,
                message="Missing secondary UV set (UV1).",
                suggestion="Add UV1 if required for lightmaps/baking."
            )
        )

    # ----------------------------------------
    # Too many UV sets
    # ----------------------------------------

    if len(uv_sets) > MAX_UV_SETS:

        issues.append(
            ValidationIssue(
                asset_name=mesh.name,
                check_name=CHECK_UV_SETS,
                severity=ValidationSeverity.WARNING,
                message=(
                    f"Mesh contains too many UV sets "
                    f"({len(uv_sets)}/{MAX_UV_SETS})."
                ),
                suggestion="Remove unused UV sets."
            )
        )

    # ----------------------------------------
    # Empty UV set names
    # ----------------------------------------

    for uv_set in uv_sets:

        if not uv_set.strip():

            issues.append(
                ValidationIssue(
                    asset_name=mesh.name,
                    check_name=CHECK_UV_SETS,
                    severity=ValidationSeverity.WARNING,
                    message="Mesh contains unnamed UV sets.",
                    suggestion="Rename UV sets properly."
                )
            )

    # ----------------------------------------
    # Duplicate UV set names
    # ----------------------------------------

    if len(set(uv_sets)) != len(uv_sets):

        issues.append(
            ValidationIssue(
                asset_name=mesh.name,
                check_name=CHECK_UV_SETS,
                severity=ValidationSeverity.WARNING,
                message="Mesh contains duplicate UV set names.",
                suggestion="Ensure UV set names are unique."
            )
        )

    return issues