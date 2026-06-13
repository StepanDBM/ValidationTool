from dataclasses import dataclass


@dataclass
class AovContext:
    name: str = ""
    enabled: bool = False

    data_type: str = ""          # RGB / RGBA / FLOAT / VECTOR / etc.
    source_type: str = ""        # BUILTIN / CUSTOM / LIGHT_GROUP / CRYPTOMATTE / etc.

    driver: str = ""             # exr / deepexr / png / display / etc.
    filter: str = ""             # gaussian / box / closest / variance / etc.

    light_group: str = ""
    is_builtin: bool = False

    output_path: str = ""
    output_prefix: str = ""

    has_valid_name: bool = True
    is_required: bool = False