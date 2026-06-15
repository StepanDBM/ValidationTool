
using System;
using System.Collections.ObjectModel;
using System.IO;
using System.Linq;
using System.Windows;
using System.Windows.Data;
using ValidationTool.UI.ViewModels.ValidationView_Models;
using ValidationTool.UI.Models.DTOs;

namespace ValidationTool.UI.ViewModels {
    public class UC_TeamListViewModel {
        private readonly ObservableCollection<IssueViewModel> _issues;
        private readonly SelectionContext _selection;
        public ObservableCollection<TeamStatsViewModel> TeamList { get; set; } = new ObservableCollection<TeamStatsViewModel>();
        public UC_TeamListViewModel(ObservableCollection<IssueViewModel> issues, SelectionContext selection) {//MVVM injection
            _issues = issues;
            _selection = selection;
        }


        private TeamStatsViewModel _selectedTeamVM;
        public TeamStatsViewModel SelectedTeamVM {
            get => _selectedTeamVM;
            set {
                _selectedTeamVM = value;

                if (value != null) {
                    _selection.SelectedTeam = value.TeamName;
                }
            }
        }

        public void AggregateAll() {
            var grouped = _issues
                .GroupBy(i => i.Artist?.ArtistTeam ?? "Unknown");

            TeamList.Clear();

            foreach (var g in grouped) {
                int errors = g.Count(i => i.Severity == "ERROR");
                int warnings = g.Count(i => i.Severity == "WARNING");
                int infos = g.Count(i => i.Severity == "INFO");

                TeamList.Add(new TeamStatsViewModel {
                    TeamName = g.Key,
                    ArtistsCount = g.Select(i => i.Artist?.ArtistName).Distinct().Count(),
                    Errors = errors,
                    Warnings = warnings,
                    Issues = errors + warnings + infos
                });
            }
        }

    }
}