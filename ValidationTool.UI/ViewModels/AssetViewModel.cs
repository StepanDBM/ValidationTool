using System.Collections.ObjectModel;

public class AssetViewModel {
    public string AssetName { get; set; }
    public ObservableCollection<StageViewModel> Stages { get; set; }
        = new ObservableCollection<StageViewModel>();
}