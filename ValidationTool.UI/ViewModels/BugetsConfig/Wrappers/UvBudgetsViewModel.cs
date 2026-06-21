using ValidationTool.UI.Models.DTOs.BudgetConfig;

namespace ValidationTool.UI.ViewModels.BudgetsView_Models {
    public class UvBudgetsViewModel : BudgetSectionViewModelBase {
        public override string Title => "UV Budgets";

        public UvBudgetDto Uv { get; }

        public UvBudgetsViewModel(UvBudgetDto uv) {
            Uv = uv ?? new UvBudgetDto();
        }
    }
}