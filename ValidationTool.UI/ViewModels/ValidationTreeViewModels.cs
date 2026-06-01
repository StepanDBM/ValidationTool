using System.Collections.ObjectModel;

namespace ValidationTool.UI.ViewModels {
    public class AssetNodeViewModel {
        public string AssetName { get; set; }
        public ObservableCollection<StageNodeViewModel> Stages { get; set; }
            = new ObservableCollection<StageNodeViewModel>();
    }

    public class StageNodeViewModel {
        public string StageName { get; set; }
        public ObservableCollection<IssueViewModel> Issues { get; set; }
            = new ObservableCollection<IssueViewModel>();
    }
}