using ValidationTool.UI.Models.DTOs.BudgetConfig;

namespace ValidationTool.UI.ViewModels.BudgetsView_Models {
    public class PerformanceBudgetsViewModel : BudgetSectionViewModelBase {
        public override string Title => "Performance Budgets";

        public PerformanceBudgetDto Performance { get; }

        public PerformanceBudgetsViewModel(PerformanceBudgetDto performance) {
            Performance = performance ?? new PerformanceBudgetDto();
        }
    }
}