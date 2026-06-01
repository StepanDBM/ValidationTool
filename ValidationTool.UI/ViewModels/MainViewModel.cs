using System.Collections.ObjectModel;
using ValidationTool.UI.Models;
using ValidationTool.UI.Services;

namespace ValidationTool.UI.ViewModels {
    public class MainViewModel {
        public ObservableCollection<IssueViewModel> Issues { get; set; }
            = new ObservableCollection<IssueViewModel>();

        public void LoadReport(string path) {
            Issues.Clear();

            var run = JsonReportLoader.Load(path);

            foreach (var asset in run.Assets)
                foreach (var stage in asset.Stages)
                    foreach (var issue in stage.Issues) {
                        Issues.Add(new IssueViewModel {
                            AssetName = issue.AssetName,
                            CheckName = issue.CheckName,
                            Severity = issue.Severity,
                            Message = issue.Message,
                            Suggestion = issue.Suggestion
                        });
                    }
        }
    }
}