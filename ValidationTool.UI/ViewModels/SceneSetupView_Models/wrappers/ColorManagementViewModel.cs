using ValidationTool.UI.Models.DTOs.SceneSetup;

namespace ValidationTool.UI.ViewModels.SceneSetupView_Models {
    public class ColorManagementViewModel {
        public ColorManagementDto ColorManagement { get; }

        public ColorManagementViewModel(ColorManagementDto colorManagement) {
            ColorManagement = colorManagement;
        }
    }
}