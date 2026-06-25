from dataclasses import dataclass
from config.validation_config import ValidationConfig
import config.config_models as configModels 


@dataclass
class ValidationRuntimeContext:
    validation_config: ValidationConfig
    naming_rules: configModels.NamingRules
    budgets: configModels.BudgetConfig