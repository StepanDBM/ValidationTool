using System.Collections.ObjectModel;
using System.IO;
using ValidationTool.UI.Services.external;
using ValidationTool.UI.Services.Config;
using ValidationTool.UI.Models.DTOs;

namespace ValidationTool.UI.ViewModels {
    public class MainViewModel {
        public ObservableCollection<IssueViewModel> Assets { get; set; }
            = new ObservableCollection<IssueViewModel>();
        public ValidationViewModel ValViewModel { get; } = new ValidationViewModel();
        public void LoadReport() {
            ValidationViewModel myValidationTreeViewModel = new ValidationViewModel();
            myValidationTreeViewModel.LoadReport();

        }
        public void RunMayaValidation() {
            MayaRunner.Run(Path.Combine(Paths.HEADLESS, "run_maya_validation.py"));
        }
        public void RunBlenderValidation() {
            BlenderRunner.Run(Path.Combine(Paths.HEADLESS, "run_blender_validation.py"));
        }

    }
}