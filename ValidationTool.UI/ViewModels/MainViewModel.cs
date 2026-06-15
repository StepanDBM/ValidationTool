using System.Collections.ObjectModel;
using System.IO;
using ValidationTool.UI.Services.External;
using ValidationTool.UI.Services.Config;
using ValidationTool.UI.Models.DTOs;

namespace ValidationTool.UI.ViewModels {
    public class MainViewModel {
        public ObservableCollection<IssueViewModel> Assets { get; set; } = new ObservableCollection<IssueViewModel>();
        public string someText { get; set; }
    }
}