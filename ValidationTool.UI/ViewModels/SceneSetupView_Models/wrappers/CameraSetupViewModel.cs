using ValidationTool.UI.Models.DTOs.SceneSetup;

namespace ValidationTool.UI.ViewModels.SceneSetupView_Models {
    public class CameraSetupViewModel {
        public CameraSetupDto CameraSetup { get; }

        public CameraSetupViewModel(CameraSetupDto cameraSetup) {
            CameraSetup = cameraSetup;
        }
    }
}