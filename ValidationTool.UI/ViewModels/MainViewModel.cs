using System.Collections.ObjectModel;
using ValidationTool.UI.ViewModels;
using ValidationTool.UI.Services.external;

namespace ValidationTool.UI.ViewModels {
    public class MainViewModel {
        public ObservableCollection<AssetViewModel> Assets { get; set; }
            = new ObservableCollection<AssetViewModel>();

        public void LoadReport(string path) {
            ValidationTreeViewModel myValidationTreeViewModel = new ValidationTreeViewModel();
            myValidationTreeViewModel.LoadReport(path, Assets);
        }
        public void RunBlenderValidation() {
            BlenderRunner.Run(
                @"C:\Users\StyopaDBM\source\repos\ValidationTool\ValidationTool.Client\ValidationTool\misc_tools\headless\run_blender_validation.py"
            );
        }

        public void RunMayaValidation() {
            MayaRunner.Run(
                @"C:\Users\StyopaDBM\source\repos\ValidationTool\ValidationTool.Client\ValidationTool\misc_tools\headless\run_maya_validation.py"
            );
        }
    }
}