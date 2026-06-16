using ValidationTool.UI.Models.DTOs;

namespace ValidationTool.UI.ViewModels.SceneSetupView_Models {
    public class SceneSetupGeneralViewModel {
        public SceneSetupDto SceneSetup { get; }

        public SceneSetupGeneralViewModel(SceneSetupDto sceneSetup) {
            SceneSetup = sceneSetup;
        }
    }
}
