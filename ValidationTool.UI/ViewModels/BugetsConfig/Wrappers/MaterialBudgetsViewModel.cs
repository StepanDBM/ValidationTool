using ValidationTool.UI.Models.DTOs.BudgetConfig;

namespace ValidationTool.UI.ViewModels.BudgetsView_Models {
    public class MaterialBudgetsViewModel : BudgetSectionViewModelBase {
        public override string Title => "Material Budgets";

        public MaterialBudgetDto Materials { get; }

        public MaterialBudgetsViewModel(MaterialBudgetDto materials) {
            Materials = materials ?? new MaterialBudgetDto();
        }
    }
}