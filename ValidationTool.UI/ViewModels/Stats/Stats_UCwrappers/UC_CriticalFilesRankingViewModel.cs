using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Globalization;
using System.Linq;
using ValidationTool.UI.Models.Stats;
using ValidationTool.UI.ViewModels.General;

namespace ValidationTool.UI.ViewModels.StatsView_Models {
    public class UC_CriticalFilesRankingViewModel : ViewModelBase {
        public ObservableCollection<CriticalFileRankingItemViewModel> Items { get; } =
            new ObservableCollection<CriticalFileRankingItemViewModel>();

        private string _subtitle = "No critical file information loaded.";
        public string Subtitle {
            get => _subtitle;
            set => SetProperty(ref _subtitle, value);
        }

        private int _displayedFileCount;
        public int DisplayedFileCount {
            get => _displayedFileCount;
            set => SetProperty(ref _displayedFileCount, value);
        }

        private int _totalDisplayedIssues;
        public int TotalDisplayedIssues {
            get => _totalDisplayedIssues;
            set => SetProperty(ref _totalDisplayedIssues, value);
        }

        public void Apply(IEnumerable<StatsCriticalFileItem> items) {
            Items.Clear();

            if (items == null) {
                DisplayedFileCount = 0;
                TotalDisplayedIssues = 0;
                Subtitle = "No critical file information loaded.";
                return;
            }

            var list = items
                .Where(x => x != null)
                .OrderByDescending(x => x.SeverityScore)
                .ThenByDescending(x => x.Errors)
                .ThenByDescending(x => x.TotalIssues)
                .ToList();

            DisplayedFileCount = list.Count;
            TotalDisplayedIssues = list.Sum(x => x.TotalIssues);

            foreach (var item in list) {
                Items.Add(new CriticalFileRankingItemViewModel {
                    File = item.File,
                    Team = item.Team,
                    Artist = item.Artist,
                    Dcc = item.Dcc,

                    TotalIssues = item.TotalIssues,
                    TotalIssuesDisplay = item.TotalIssues.ToString("N0", CultureInfo.InvariantCulture),

                    Errors = item.Errors,
                    ErrorsDisplay = item.Errors.ToString("N0", CultureInfo.InvariantCulture),

                    Warnings = item.Warnings,
                    WarningsDisplay = item.Warnings.ToString("N0", CultureInfo.InvariantCulture),

                    Info = item.Info,
                    InfoDisplay = item.Info.ToString("N0", CultureInfo.InvariantCulture),

                    Hard = item.Hard,
                    HardDisplay = item.Hard.ToString("N0", CultureInfo.InvariantCulture),

                    AutoFixableIssues = item.AutoFixableIssues,
                    AutoFixableIssuesDisplay = item.AutoFixableIssues.ToString("N0", CultureInfo.InvariantCulture),

                    AutoFixablePercent = item.AutoFixablePercent,
                    AutoFixablePercentDisplay = item.AutoFixablePercent.ToString("0.0", CultureInfo.InvariantCulture) + "%",

                    TopStage = item.TopStage,
                    TopCheck = item.TopCheck,

                    SeverityScore = item.SeverityScore,
                    SeverityScoreDisplay = item.SeverityScore.ToString("N0", CultureInfo.InvariantCulture)
                });
            }

            Subtitle = DisplayedFileCount > 0
                ? $"Top {DisplayedFileCount.ToString("N0", CultureInfo.InvariantCulture)} critical files ranked by weighted severity."
                : "No critical file information loaded.";
        }
    }

    public class CriticalFileRankingItemViewModel : ViewModelBase {
        private string _file;
        public string File {
            get => _file;
            set => SetProperty(ref _file, value);
        }

        private string _team;
        public string Team {
            get => _team;
            set => SetProperty(ref _team, value);
        }

        private string _artist;
        public string Artist {
            get => _artist;
            set => SetProperty(ref _artist, value);
        }

        private string _dcc;
        public string Dcc {
            get => _dcc;
            set => SetProperty(ref _dcc, value);
        }

        private int _totalIssues;
        public int TotalIssues {
            get => _totalIssues;
            set => SetProperty(ref _totalIssues, value);
        }

        private string _totalIssuesDisplay;
        public string TotalIssuesDisplay {
            get => _totalIssuesDisplay;
            set => SetProperty(ref _totalIssuesDisplay, value);
        }

        private int _errors;
        public int Errors {
            get => _errors;
            set => SetProperty(ref _errors, value);
        }

        private string _errorsDisplay;
        public string ErrorsDisplay {
            get => _errorsDisplay;
            set => SetProperty(ref _errorsDisplay, value);
        }

        private int _warnings;
        public int Warnings {
            get => _warnings;
            set => SetProperty(ref _warnings, value);
        }

        private string _warningsDisplay;
        public string WarningsDisplay {
            get => _warningsDisplay;
            set => SetProperty(ref _warningsDisplay, value);
        }

        private int _info;
        public int Info {
            get => _info;
            set => SetProperty(ref _info, value);
        }

        private string _infoDisplay;
        public string InfoDisplay {
            get => _infoDisplay;
            set => SetProperty(ref _infoDisplay, value);
        }

        private int _hard;
        public int Hard {
            get => _hard;
            set => SetProperty(ref _hard, value);
        }

        private string _hardDisplay;
        public string HardDisplay {
            get => _hardDisplay;
            set => SetProperty(ref _hardDisplay, value);
        }

        private int _autoFixableIssues;
        public int AutoFixableIssues {
            get => _autoFixableIssues;
            set => SetProperty(ref _autoFixableIssues, value);
        }

        private string _autoFixableIssuesDisplay;
        public string AutoFixableIssuesDisplay {
            get => _autoFixableIssuesDisplay;
            set => SetProperty(ref _autoFixableIssuesDisplay, value);
        }

        private double _autoFixablePercent;
        public double AutoFixablePercent {
            get => _autoFixablePercent;
            set => SetProperty(ref _autoFixablePercent, value);
        }

        private string _autoFixablePercentDisplay;
        public string AutoFixablePercentDisplay {
            get => _autoFixablePercentDisplay;
            set => SetProperty(ref _autoFixablePercentDisplay, value);
        }

        private string _topStage;
        public string TopStage {
            get => _topStage;
            set => SetProperty(ref _topStage, value);
        }

        private string _topCheck;
        public string TopCheck {
            get => _topCheck;
            set => SetProperty(ref _topCheck, value);
        }

        private int _severityScore;
        public int SeverityScore {
            get => _severityScore;
            set => SetProperty(ref _severityScore, value);
        }

        private string _severityScoreDisplay;
        public string SeverityScoreDisplay {
            get => _severityScoreDisplay;
            set => SetProperty(ref _severityScoreDisplay, value);
        }
    }
}