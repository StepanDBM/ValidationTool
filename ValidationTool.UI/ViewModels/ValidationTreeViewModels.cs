using System.Collections.ObjectModel;
using System.IO;
using ValidationTool.UI.Services;

namespace ValidationTool.UI.ViewModels {

    public class ValidationTreeViewModel {

        public void LoadReport(ObservableCollection<AssetViewModel> myAssets) {
            var myPath = JsonReportLoader.LoadLastRun();
            myAssets.Clear();
            System.Diagnostics.Debug.WriteLine(JsonReportLoader.Load(myPath));


            var dto = JsonReportLoader.Load(myPath);

            foreach (var asset in dto.Assets) {
                var assetVm = new AssetViewModel {
                    AssetName = asset.AssetName
                };

                foreach (var stage in asset.Stages) {
                    var stageVm = new StageViewModel {
                        StageName = stage.StageName
                    };

                    foreach (var issue in stage.Issues) {
                        stageVm.Issues.Add(new IssueViewModel {
                            AssetName = issue.AssetName,
                            CheckName = issue.CheckName,
                            Severity = issue.Severity,
                            Message = issue.Message,
                            Suggestion = issue.Suggestion
                        });
                    }

                    assetVm.Stages.Add(stageVm);
                }

                myAssets.Add(assetVm);
            }
        }
    }
}