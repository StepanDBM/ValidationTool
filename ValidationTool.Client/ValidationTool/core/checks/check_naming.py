# checks/check_naming.py
import re
from typing import List

from core.validation_context import ValidationRuntimeContext
from core.validation_system import (
    ObjectContext,
    ValidationIssue,
    ValidationSeverity,
    CHECK_NAMING
)

VALID_PREFIXES = [
    "CH",
    "HERO",
    "WP",
    "WPN",
    "PRP",
    "PROP",
    "ENV",
    "MOD"
]

DEFAULT_MAYA_NAMES = [
    "pCube",
    "pSphere",
    "pCylinder",
    "pPlane",
    "pTorus",
    "polySurface"
]

NAME_PATTERN = re.compile(
    r"^[A-Z]+_[A-Za-z0-9_]+$"
)


def check_naming(mesh: ObjectContext, runtime_ctx: ValidationRuntimeContext) -> List[ValidationIssue]:
    issues = []
    name = mesh.name

    upper_name = name.upper()

    # ----------------------------------------
    # Default Maya primitive naming
    # ----------------------------------------

    for default_name in runtime_ctx.naming_rules.default_maya_names:

        if name.startswith(default_name):

            issues.append(
                ValidationIssue(
                    asset_name=name,
                    check_name=CHECK_NAMING,
                    severity=ValidationSeverity.WARNING,
                    message=(
                        f"Mesh uses default Maya naming: {name}"
                    ),
                    suggestion="Rename mesh using studio naming conventions."
                )
            )
            return issues

    # ----------------------------------------
    # Prefix validation
    # ----------------------------------------

    has_valid_prefix = False

    for prefix in runtime_ctx.naming_rules.valid_prefixes:

        if upper_name.startswith(prefix + "_"):
            has_valid_prefix = True
            break
    if not has_valid_prefix:
        issues.append(
            ValidationIssue(
                asset_name=name,
                check_name=CHECK_NAMING,
                severity=ValidationSeverity.WARNING,
                message=(
                    "Mesh missing valid asset prefix."
                ),
                suggestion=(
                    "Use prefixes like CH_, ENV_, PRP_, WPN_, etc."
                )
            )
        )

    # ----------------------------------------
    # Regex naming convention validation
    # ----------------------------------------

    if not runtime_ctx.naming_rules.name_pattern.match(name):

        issues.append(
            ValidationIssue(
                asset_name=name,
                check_name=CHECK_NAMING,
                severity=ValidationSeverity.WARNING,
                message=(
                    f"Mesh name does not follow naming convention: {name}"
                ),
                suggestion=(
                    "Use format PREFIX_AssetName"
                )
            )
        )
    # ----------------------------------------
    # Double underscores
    # ----------------------------------------

    if "__" in name:

        issues.append(
            ValidationIssue(
                asset_name=name,
                check_name=CHECK_NAMING,
                severity=ValidationSeverity.WARNING,
                message="Mesh name contains double underscores.",
                suggestion="Avoid redundant separators."
            )
        )
    # ----------------------------------------
    # Spaces
    # ----------------------------------------

    if " " in name or "." in name:

        issues.append(
            ValidationIssue(
                asset_name=name,
                check_name=CHECK_NAMING,
                severity=ValidationSeverity.ERROR,
                message="Mesh name contains spaces or dots.",
                suggestion="Use underscores instead of spaces or other invalid characters."
            )
        )

    return issues