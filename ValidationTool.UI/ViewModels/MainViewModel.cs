using System.Collections.ObjectModel;
using System.IO;
using ValidationTool.UI.Services.external;
using ValidationTool.UI.Services.Config;
using ValidationTool.UI.Models.DTOs;

namespace ValidationTool.UI.ViewModels {
    public class MainViewModel {
        public ObservableCollection<IssueViewModel> Assets { get; set; }
            = new ObservableCollection<IssueViewModel>();
    }
}