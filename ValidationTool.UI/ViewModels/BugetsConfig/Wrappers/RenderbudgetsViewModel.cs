using ValidationTool.UI.Models.DTOs.BudgetConfig;

namespace ValidationTool.UI.ViewModels.BudgetsView_Models {
    public class RenderBudgetsViewModel : BudgetSectionViewModelBase {
        public override string Title => "Render Budgets";

        public RenderBudgetDto Render { get; }

        public RenderBudgetsViewModel(RenderBudgetDto render) {
            Render = render ?? new RenderBudgetDto();
        }
    }
}