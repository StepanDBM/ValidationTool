using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Input;
using ValidationTool.Services.Notifications;
using ValidationTool.UI.Models.DTOs;
using ValidationTool.UI.ViewModels.ValidationView_Models;

namespace ValidationTool.UI.ViewModels {
    public class UC_ArtistListViewModel {
        private readonly ObservableCollection<IssueViewModel> _issues;
        private readonly SelectionContext _selection;
        public ObservableCollection<ArtistStatsViewModel> ArtistList { get; set; } = new ObservableCollection<ArtistStatsViewModel>();

        private NotificationService mNotService = new NotificationService(new NotificationMessageBuilder());
        public ICommand SendReportCommand { get; }

        public UC_ArtistListViewModel(ObservableCollection<IssueViewModel> issues, SelectionContext selection) {
            SendReportCommand = new AsyncRelayCommand<ArtistStatsViewModel>(SendReport);
            _issues = issues;
            _selection = selection;
            _selection.PropertyChanged += OnSelectionChanged;
        }
        private void OnSelectionChanged(object sender, PropertyChangedEventArgs e) {
            if (e.PropertyName == nameof(_selection.SelectedTeam)) {
                FilterArtists();
            }
        }

        private ArtistStatsViewModel _selectedArtistVM;
        public ArtistStatsViewModel SelectedArtistVM {
            get => _selectedArtistVM;
            set {
                _selectedArtistVM = value;

                if (value != null) {
                    _selection.SelectedArtist = value.ArtistName;
                }
            }
        }
        private void FilterArtists() {
            ArtistList.Clear();

            var filtered = _issues
                .Where(i => i.Artist?.ArtistTeam == _selection.SelectedTeam)
                .GroupBy(i => i.Artist.ArtistName);

            foreach (var g in filtered) {
                var artist = g.First().Artist;

                int errors = g.Count(i => i.Severity == "ERROR");
                int warnings = g.Count(i => i.Severity == "WARNING");
                int infos = g.Count(i => i.Severity == "INFO");

                ArtistList.Add(new ArtistStatsViewModel {
                    ArtistName = artist?.ArtistName,
                    ArtistGmail = artist?.ArtistGmail,
                    ArtistID = artist?.ArtistID,
                    ArtistLv = artist?.ArtistLevel,

                    Errors = errors,
                    Warnings = warnings,
                    Issues = errors + warnings + infos
                });
            }
        }


        private async Task SendReport(ArtistStatsViewModel artist) {
            try {
                if (artist == null) return;

                var artistIssues = new ObservableCollection<IssueViewModel>(
                    _issues.Where(i => 
                    i.Artist?.ArtistName == artist.ArtistName &&
                    i.Artist?.ArtistTeam == _selection.SelectedTeam
                        )
                );

                await mNotService.SendErrorReportAsync(artistIssues);
            } catch (Exception ex) {
                System.Diagnostics.Debug.WriteLine($"[ERROR] {ex.Message}");
            }

        }
    }
}
