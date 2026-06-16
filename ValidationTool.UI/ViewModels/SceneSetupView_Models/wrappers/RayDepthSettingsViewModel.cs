using ValidationTool.UI.Models.DTOs.SceneSetup;

namespace ValidationTool.UI.ViewModels.SceneSetupView_Models {
    public class RayDepthSettingsViewModel {
        public RayDepthSettingsDto RayDepthSettings { get; }

        public RayDepthSettingsViewModel(RayDepthSettingsDto rayDepthSettings) {
            RayDepthSettings = rayDepthSettings;
        }
    }
}