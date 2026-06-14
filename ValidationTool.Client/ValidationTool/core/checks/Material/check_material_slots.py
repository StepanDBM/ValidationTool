from core.validation_context import ValidationRuntimeContext
from core.context.mesh_context import MeshContext
from core.validation_system import (
    ValidationIssue,
    ValidationSeverity
)

from core.checks.validation_check_ids import CHECK_MATERIAL_SLOTS, CHECK_MATERIAL_SLOTS_EXIST


def check_lamina_faces(mesh: MeshContext, runtime_ctx: ValidationRuntimeContext) -> ValidationIssue:
    if len(mesh.materials) == 0:
        return ValidationIssue(
            asset_name=mesh.name,
            check_name=CHECK_MATERIAL_SLOTS_EXIST,
            severity=ValidationSeverity.ERROR,
            message=f"Mesh has ZERO material slots, which will break in engine.",
            suggestion="Fill the slots with at least ONE material slot."
        )
    elif len(mesh.materials) > 3:
        return ValidationIssue(
            asset_name=mesh.name,
            check_name=CHECK_MATERIAL_SLOTS,
            severity=ValidationSeverity.WARNING,
            message=f"Mesh has {mesh.material_slot_count} material slots which may exceed engine limits.",
            suggestion="Reduce the number of material slots used by the mesh."
        )
    return None