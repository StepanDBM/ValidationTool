using System.Collections.ObjectModel;
using ValidationTool.UI.Services;

namespace ValidationTool.UI.ViewModels {
    public class ValidationViewModel{

        public ObservableCollection<IssueViewModel> mIssues { get; set; }
            = new ObservableCollection<IssueViewModel>();


        public void LoadReport() {

            var myPath = JsonReportLoader.LoadLastRun();
            var dto = JsonReportLoader.Load(myPath);

            foreach (var issue in dto.issues) {
                mIssues.Add(new IssueViewModel {
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