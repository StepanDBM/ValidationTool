using ValidationTool.UI.Models.DTOs.BudgetConfig;

namespace ValidationTool.UI.ViewModels.BudgetsView_Models {
    public class LightingBudgetsViewModel : BudgetSectionViewModelBase {
        public override string Title => "Lighting Budgets";

        public LightingBudgetDto Lighting { get; }

        public LightingBudgetsViewModel(LightingBudgetDto lighting) {
            Lighting = lighting ?? new LightingBudgetDto();
        }
    }
}