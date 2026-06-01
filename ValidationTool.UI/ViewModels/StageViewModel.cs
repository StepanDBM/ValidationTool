using System.Collections.ObjectModel;
using ValidationTool.UI.ViewModels;

public class StageViewModel {
    public string StageName { get; set; }
    public ObservableCollection<IssueViewModel> Issues { get; set; }
        = new ObservableCollection<IssueViewModel>();
}