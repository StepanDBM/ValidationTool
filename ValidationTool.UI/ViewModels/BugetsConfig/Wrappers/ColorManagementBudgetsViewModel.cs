using ValidationTool.UI.Models.DTOs.BudgetConfig;

namespace ValidationTool.UI.ViewModels.BudgetsView_Models {
    public class ColorManagementBudgetsViewModel : BudgetSectionViewModelBase {
        public override string Title => "Color Management Budgets";

        public ColorManagementBudgetDto ColorManagement { get; }

        public ColorManagementBudgetsViewModel(ColorManagementBudgetDto colorManagement) {
            ColorManagement = colorManagement ?? new ColorManagementBudgetDto();
        }
    }
}