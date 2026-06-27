using System.Collections.ObjectModel;
using ValidationTool.UI.Models.DTOs;
using ValidationTool.UI.ViewModels.StatsView_Models;

namespace ValidationTool.UI.ViewModels {
    public class MainViewModel {
        public ObservableCollection<IssueViewModel> Issues { get; } =
            new ObservableCollection<IssueViewModel>();

        public ObservableCollection<ValidationRunDto> Runs { get; } =
            new ObservableCollection<ValidationRunDto>();

        public ValidationViewModel ValidationVM { get; }
        public StatsViewModel StatsVM { get; }

        public MainViewModel() {
            ValidationVM = new ValidationViewModel(Issues, Runs);
            StatsVM = new StatsViewModel(Issues, Runs);
        }
    }
}