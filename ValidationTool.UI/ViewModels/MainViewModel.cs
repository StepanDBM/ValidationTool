using System.Collections.ObjectModel;
using System.IO;
using ValidationTool.UI.Services.external;
using ValidationTool.UI.Services.Config;

namespace ValidationTool.UI.ViewModels {
    public class MainViewModel {
        public ObservableCollection<AssetViewModel> Assets { get; set; }
            = new ObservableCollection<AssetViewModel>();

        public void LoadReport() {
            ValidationTreeViewModel myValidationTreeViewModel = new ValidationTreeViewModel();
            myValidationTreeViewModel.LoadReport(Assets);
        }
        public void RunBlenderValidation() {
            BlenderRunner.Run(Path.Combine(Paths.HEADLESS, "run_blender_validation.py"));
        }

        public void RunMayaValidation() {
            MayaRunner.Run(Path.Combine(Paths.HEADLESS, "run_maya_validation.py"));
        }
    }
}