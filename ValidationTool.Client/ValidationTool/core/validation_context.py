from dataclasses import dataclass
from config.validation_config import ValidationConfig
import config.config_models as configModels 


@dataclass
class ValidationRuntimeContext:
    validation: ValidationConfig
    naming: configModels.NamingRules
    budgets: configModels.BudgetConfig