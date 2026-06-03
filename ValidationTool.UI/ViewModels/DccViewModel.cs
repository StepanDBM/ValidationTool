using System.Collections.ObjectModel;

public class DccViewModel {
    public string DccName { get; set; }
    public ObservableCollection<AssetViewModel> Runs { get; set; }
        = new ObservableCollection<AssetViewModel>();
}