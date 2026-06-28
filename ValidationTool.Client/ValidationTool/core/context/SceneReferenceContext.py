from dataclasses import dataclass
from typing import List

from core.context.baseContext import BaseContext


@dataclass
class SceneReferenceContext(BaseContext):
    references: List[str]
    broken_references: List[str]
    unloaded_references: List[str]