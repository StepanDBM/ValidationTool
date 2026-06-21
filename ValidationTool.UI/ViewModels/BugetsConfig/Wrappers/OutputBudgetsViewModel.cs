using ValidationTool.UI.Models.DTOs.BudgetConfig;

namespace ValidationTool.UI.ViewModels.BudgetsView_Models {
    public class OutputBudgetsViewModel : BudgetSectionViewModelBase {
        public override string Title => "Output Budgets";

        public OutputBudgetDto Output { get; }

        public OutputBudgetsViewModel(OutputBudgetDto output) {
            Output = output ?? new OutputBudgetDto();
        }
    }
}