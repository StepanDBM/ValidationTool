# checks/check_transforms.py

from typing import List

from core.validation_system import (
    MeshContext,
    ValidationIssue,
    ValidationSeverity,
    CHECK_TRANSFORMS
)

MAX_SCALE = 1000.0


def check_transforms(mesh: MeshContext) -> List[ValidationIssue]:
    issues = []
    fucked_up = False
    # ----------------------------------------
    # Negative scale
    # ----------------------------------------

    if mesh.has_negative_scale:

        issues.append(
            ValidationIssue(
                asset_name=mesh.name,
                check_name=CHECK_TRANSFORMS,
                severity=ValidationSeverity.ERROR,
                message="Negative scale detected.",
                suggestion="Freeze transforms (scale)."
            )
        )
        fucked_up = True

    # ----------------------------------------
    # Non-uniform scale (optional but common issue)
    # ----------------------------------------

    if hasattr(mesh, "scale"):

        sx, sy, sz = mesh.scale

        if not (abs(sx - sy) < 1e-5 and abs(sy - sz) < 1e-5):

            issues.append(
                ValidationIssue(
                    asset_name=mesh.name,
                    check_name=CHECK_TRANSFORMS,
                    severity=ValidationSeverity.WARNING,
                    message=f"Non-uniform scale detected ({sx}, {sy}, {sz}).",
                    suggestion="Apply freeze transforms."
                )
            )
            fucked_up = True
    # ----------------------------------------
    # Zero scale (invalid transform state)
    # ----------------------------------------

    if hasattr(mesh, "scale"):

        sx, sy, sz = mesh.scale

        if sx == 0 or sy == 0 or sz == 0:

            issues.append(
                ValidationIssue(
                    asset_name=mesh.name,
                    check_name=CHECK_TRANSFORMS,
                    severity=ValidationSeverity.ERROR,
                    message="Zero scale detected on one or more axes.",
                    suggestion="Reset scale to 1,1,1 before freezing."
                )
            )
            fucked_up = True

    # ----------------------------------------
    # Extreme scale values (scene instability)
    # ----------------------------------------

    if hasattr(mesh, "scale"):

        sx, sy, sz = mesh.scale


        if abs(sx) > MAX_SCALE or abs(sy) > MAX_SCALE or abs(sz) > MAX_SCALE:

            issues.append(
                ValidationIssue(
                    asset_name=mesh.name,
                    check_name=CHECK_TRANSFORMS,
                    severity=ValidationSeverity.WARNING,
                    message=f"Extreme scale detected ({sx}, {sy}, {sz}).",
                    suggestion="Check asset scaling consistency."
                )
            )
            fucked_up = True
    
    if not fucked_up:
        issues.append(
                ValidationIssue(
                    asset_name=mesh.name,
                    check_name=CHECK_TRANSFORMS,
                    severity=ValidationSeverity.INFO,
                    message=f"All transforms are correcty",
                    suggestion="Call your family, you did great."
                )
            )
    
    return issues