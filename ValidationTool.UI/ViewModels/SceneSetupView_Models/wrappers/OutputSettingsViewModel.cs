using ValidationTool.UI.Models.DTOs.SceneSetup;

namespace ValidationTool.UI.ViewModels.SceneSetupView_Models {
    public class OutputSettingsViewModel {
        public OutputSettingsDto OutputSettings { get; }

        public OutputSettingsViewModel(OutputSettingsDto outputSettings) {
            OutputSettings = outputSettings;
        }
    }
}