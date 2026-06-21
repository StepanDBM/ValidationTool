using ValidationTool.UI.Models.DTOs.BudgetConfig;

namespace ValidationTool.UI.ViewModels.BudgetsView_Models {
    public class RiggingBudgetsViewModel : BudgetSectionViewModelBase {
        public override string Title => "Rigging Budgets";

        public RiggingBudgetDto Rigging { get; }

        public RiggingBudgetsViewModel(RiggingBudgetDto rigging) {
            Rigging = rigging ?? new RiggingBudgetDto();
        }
    }
}