from dataclasses import dataclass
from typing import List

from core.context.baseContext import BaseContext


@dataclass
class SceneHierarchyContext(BaseContext):
    root_objects: List[str]
    all_transforms: List[str]

    empty_transforms: List[str]
    groups: List[str]

    max_depth: int