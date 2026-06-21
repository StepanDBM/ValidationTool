using ValidationTool.UI.Models.DTOs.BudgetConfig;


namespace ValidationTool.UI.ViewModels.BudgetsView_Models {
    public class GeometryBudgetsViewModel : BudgetSectionViewModelBase {
        public override string Title => "Geometry Budgets";

        public GeometryBudgetDto Geometry { get; }

        public GeometryBudgetsViewModel(GeometryBudgetDto geometry) {
            Geometry = geometry ?? new GeometryBudgetDto();
        }
    }
}