using ValidationTool.UI.Models.DTOs.SceneSetup;

namespace ValidationTool.UI.ViewModels.SceneSetupView_Models {
    public class SamplingSettingsViewModel {
        public SamplingSettingsDto SamplingSettings { get; }

        public SamplingSettingsViewModel(SamplingSettingsDto samplingSettings) {
            SamplingSettings = samplingSettings;
        }
    }
}