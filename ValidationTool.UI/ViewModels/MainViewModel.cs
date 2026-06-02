using System.Collections.ObjectModel;
using System.Linq;
using System.Security.Authentication;
using ValidationTool.UI.Services;
using ValidationTool.UI.Services.Config;
using ValidationTool.UI.ViewModels;

public class MainViewModel {
    public ObservableCollection<AssetViewModel> Assets { get; set; }
        = new ObservableCollection<AssetViewModel>();

    public void LoadReport(string path) {
        ValidationTreeViewModel myValidationTreeViewModel = new ValidationTreeViewModel();
        myValidationTreeViewModel.LoadReport(path, Assets);
    }
}