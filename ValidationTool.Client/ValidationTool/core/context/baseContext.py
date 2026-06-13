from dataclasses import dataclass
from core.validation_system import ObjectType

@dataclass
class BaseContext:
    name: str
    object_type: ObjectType

    path: str
    parent: str