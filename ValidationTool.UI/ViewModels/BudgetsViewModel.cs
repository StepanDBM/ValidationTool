using ValidationTool.UI.Models.Config;
using ValidationTool.UI.Services.Config;

namespace ValidationTool.UI.ViewModels {
    public class BudgetsViewModel {
        private readonly BudgetsConfigService _service = new BudgetsConfigService();

        public BudgetsConfigModel Config { get; set; }

        public BudgetsViewModel() {
            Load();
        }

        public void Load() {
            Config = _service.Load();
        }

        public void Save() {
            _service.Save(Config);
        }
    }
}