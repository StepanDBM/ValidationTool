using System.Collections.ObjectModel;
using ValidationTool.UI.Models;
using ValidationTool.UI.Models.Dto;
using ValidationTool.UI.Services;

namespace ValidationTool.UI.ViewModels {
    public class MainViewModel {
        public ObservableCollection<IssueViewModel> Issues { get; set; }
            = new ObservableCollection<IssueViewModel>();

        public void Validate(string path) {
            ValidationViewModel myModel = new ValidationViewModel();
            myModel.LoadReport(path, Issues);
        }
    }
}