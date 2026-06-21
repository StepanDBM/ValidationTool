using ValidationTool.UI.Models.DTOs.BudgetConfig;

namespace ValidationTool.UI.ViewModels.BudgetsView_Models {
    public class TextureBudgetsViewModel : BudgetSectionViewModelBase {
        public override string Title => "Texture Budgets";

        public TextureBudgetDto Textures { get; }

        public TextureBudgetsViewModel(TextureBudgetDto textures) {
            Textures = textures ?? new TextureBudgetDto();
        }
    }
}