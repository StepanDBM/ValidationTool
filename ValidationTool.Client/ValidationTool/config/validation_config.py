from dataclasses import dataclass

@dataclass
class ValidationConfig:
    strict_mode: bool = True

    fail_on_first_error: bool = False
    auto_fix_enabled: bool = False

    include_info: bool = True
    include_warnings: bool = True

    debug_mode: bool = False