using System;
using System.Collections.ObjectModel;
using ValidationTool.UI.Models.DTOs;

namespace ValidationTool.UI.ViewModels {
    public class StatsViewModel {
        private readonly ObservableCollection<IssueViewModel> _issues;
        private readonly ObservableCollection<ValidationRunDto> _runs;

        public StatsViewModel(
            ObservableCollection<IssueViewModel> issues,
            ObservableCollection<ValidationRunDto> runs) {
            _issues = issues;
            _runs = runs;
        }
    }
}