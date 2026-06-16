using ValidationTool.UI.Models.DTOs.SceneSetup;

namespace ValidationTool.UI.ViewModels.SceneSetupView_Models {
    public class RenderSettingsViewModel {
        public RenderSettingsDto RenderSettings { get; }

        public RenderSettingsViewModel(RenderSettingsDto renderSettings) {
            RenderSettings = renderSettings;
        }
    }
}