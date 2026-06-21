using ValidationTool.UI.Models.DTOs.BudgetConfig;

namespace ValidationTool.UI.ViewModels.BudgetsView_Models {
    public class AnimationBudgetsViewModel : BudgetSectionViewModelBase {
        public override string Title => "Animation Budgets";

        public AnimationBudgetDto Animation { get; }

        public AnimationBudgetsViewModel(AnimationBudgetDto animation) {
            Animation = animation ?? new AnimationBudgetDto();
        }
    }
}