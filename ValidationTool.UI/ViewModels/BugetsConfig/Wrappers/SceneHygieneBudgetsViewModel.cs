using ValidationTool.UI.Models.DTOs.BudgetConfig;

namespace ValidationTool.UI.ViewModels.BudgetsView_Models {
    public class SceneHygieneBudgetsViewModel : BudgetSectionViewModelBase {
        public override string Title => "Scene Hygiene Budgets";

        public SceneHygieneBudgetDto SceneHygiene { get; }

        public SceneHygieneBudgetsViewModel(SceneHygieneBudgetDto sceneHygiene) {
            SceneHygiene = sceneHygiene ?? new SceneHygieneBudgetDto();
        }
    }
}