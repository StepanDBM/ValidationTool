using System.Collections.ObjectModel;
using System.IO;
using System.Linq;
using ValidationTool.UI.Services;
using ValidationTool.UI.ViewModels;

/*
public class ValidationTreeViewModel {
    public ObservableCollection<AssetViewModel> Assets { get; set; }
        = new ObservableCollection<AssetViewModel>();

    public void LoadReport() {
        var myPath = JsonReportLoader.LoadLastRun();
        var dto = JsonReportLoader.Load(myPath);

        Assets.Clear();

        var grouped =
            dto.issues.GroupBy(i => i.AssetName)
            .Select(assetGroup => new AssetViewModel {
                AssetName = assetGroup.Key,
                Stages = new ObservableCollection<StageViewModel>(
                    assetGroup.GroupBy(i => i.Stage)
                    .Select(stageGroup => new StageViewModel {
                        StageName = stageGroup.Key,
                        Issues = new ObservableCollection<IssueViewModel>(
                            stageGroup.Select(issue => new IssueViewModel {
                                AssetName = issue.AssetName,
                                CheckName = issue.CheckName,
                                Severity = issue.Severity,
                                Message = issue.Message,
                                Suggestion = issue.Suggestion
                            })
                        )
                    })
                )
            });

        foreach (var asset in grouped)
            Assets.Add(asset);
    }
}*/