using ValidationTool.UI.Models.DTOs.BudgetConfig;

namespace ValidationTool.UI.ViewModels.BudgetsView_Models {
    public class ExportBudgetsViewModel : BudgetSectionViewModelBase {
        public override string Title => "Export Budgets";

        public ExportBudgetDto Export { get; }

        public ExportBudgetsViewModel(ExportBudgetDto exportDto) {
            Export = exportDto ?? new ExportBudgetDto();
        }
    }
}