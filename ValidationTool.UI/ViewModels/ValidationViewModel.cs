using System.Collections.ObjectModel;
using ValidationTool.UI.Models.Dto;
using ValidationTool.UI.Services;

namespace ValidationTool.UI.ViewModels {
    public class ValidationViewModel {
        public ObservableCollection<IssueViewModel> Issues { get; set; }
            = new ObservableCollection<IssueViewModel>();

        public void LoadReport(string path, ObservableCollection<IssueViewModel> issues) {
            issues.Clear();

            ValidationRunDto dto = JsonReportLoader.Load(path);

            foreach (var asset in dto.Assets)
                foreach (var stage in asset.Stages)
                    foreach (var issue in stage.Issues) {
                        issues.Add(new IssueViewModel {
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