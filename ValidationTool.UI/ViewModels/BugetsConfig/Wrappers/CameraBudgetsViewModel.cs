using ValidationTool.UI.Models.DTOs.BudgetConfig;

namespace ValidationTool.UI.ViewModels.BudgetsView_Models {
    public class CameraBudgetsViewModel : BudgetSectionViewModelBase {
        public override string Title => "Camera Budgets";

        public CameraBudgetDto Camera { get; }

        public CameraBudgetsViewModel(CameraBudgetDto camera) {
            Camera = camera ?? new CameraBudgetDto();
        }
    }
}