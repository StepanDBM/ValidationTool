using System.Collections.ObjectModel;
using ValidationTool.UI.Services;
using ValidationTool.UI.Services.Config;
using ValidationTool.UI.Services.external;
using System.IO;

namespace ValidationTool.UI.ViewModels {
    public class ValidationViewModel{

        public ObservableCollection<IssueViewModel> mIssues { get; set; }
            = new ObservableCollection<IssueViewModel>();


        public void LoadReport() {
            var dtos = JsonReportLoader.Load();
            foreach (var dcc in dtos) {
                foreach (var issue in dcc.issues) {
                    mIssues.Add(new IssueViewModel {
                        dcc = issue.Dcc,
                        timestamp = issue.Timestamp.ToString(),
                        asset_name = issue.AssetName,
                        check_name = issue.CheckName,
                        severity = issue.Severity,
                        message = issue.Message,
                        suggestion = issue.Suggestion,
                        stage = issue.Stage
                    });
                }
            }
        }

        public void RunMayaValidation() {
            MayaRunner.Run(Path.Combine(Paths.HEADLESS, "run_maya_validation.py"));
        }
        public void RunBlenderValidation() {
            BlenderRunner.Run(Path.Combine(Paths.HEADLESS, "run_blender_validation.py"));
        }
    }
}