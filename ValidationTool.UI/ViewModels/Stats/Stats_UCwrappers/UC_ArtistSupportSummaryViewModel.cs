using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Globalization;
using System.Linq;
using ValidationTool.UI.Models.Stats;
using ValidationTool.UI.ViewModels.General;

namespace ValidationTool.UI.ViewModels.StatsView_Models {
    public class UC_ArtistSupportSummaryViewModel : ViewModelBase {
        public ObservableCollection<ArtistSupportSummaryItemViewModel> Items { get; } =
            new ObservableCollection<ArtistSupportSummaryItemViewModel>();

        private string _subtitle = "No artist support information loaded.";
        public string Subtitle {
            get => _subtitle;
            set => SetProperty(ref _subtitle, value);
        }

        private int _displayedArtistCount;
        public int DisplayedArtistCount {
            get => _displayedArtistCount;
            set => SetProperty(ref _displayedArtistCount, value);
        }

        private int _maxSeverityScore;
        public int MaxSeverityScore {
            get => _maxSeverityScore;
            set => SetProperty(ref _maxSeverityScore, value);
        }

        private int _totalIssues;
        public int TotalIssues {
            get => _totalIssues;
            set => SetProperty(ref _totalIssues, value);
        }

        public void Apply(IEnumerable<StatsArtistSupportItem> items) {
            Items.Clear();

            if (items == null) {
                DisplayedArtistCount = 0;
                MaxSeverityScore = 0;
                TotalIssues = 0;
                Subtitle = "No artist support information loaded.";
                return;
            }

            var list = items
                .Where(x => x != null)
                .OrderByDescending(x => x.SeverityScore)
                .ThenByDescending(x => x.Errors)
                .ThenByDescending(x => x.TotalIssues)
                .ToList();

            DisplayedArtistCount = list.Count;
            MaxSeverityScore = list.Count > 0 ? list.Max(x => x.SeverityScore) : 0;
            TotalIssues = list.Sum(x => x.TotalIssues);

            foreach (var item in list) {
                double barPercent = MaxSeverityScore > 0
                    ? (double)item.SeverityScore / MaxSeverityScore * 100.0
                    : 0.0;

                Items.Add(new ArtistSupportSummaryItemViewModel {
                    Artist = item.Artist,
                    Team = item.Team,

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

                    FileCount = item.FileCount,
                    FileCountDisplay = item.FileCount.ToString("N0", CultureInfo.InvariantCulture),

                    AverageIssuesPerFile = item.AverageIssuesPerFile,
                    AverageIssuesPerFileDisplay = item.AverageIssuesPerFile.ToString("0.0", CultureInfo.InvariantCulture),

                    AverageErrorsPerFile = item.AverageErrorsPerFile,
                    AverageErrorsPerFileDisplay = item.AverageErrorsPerFile.ToString("0.0", CultureInfo.InvariantCulture),

                    TopStage = item.TopStage,
                    TopCheck = item.TopCheck,

                    SeverityScore = item.SeverityScore,
                    SeverityScoreDisplay = item.SeverityScore.ToString("N0", CultureInfo.InvariantCulture),

                    SupportLevel = item.SupportLevel,
                    BarPercent = barPercent
                });
            }

            Subtitle = DisplayedArtistCount > 0
                ? $"Top {DisplayedArtistCount.ToString("N0", CultureInfo.InvariantCulture)} artists ranked by weighted severity."
                : "No artist support information loaded.";
        }
    }

    public class ArtistSupportSummaryItemViewModel : ViewModelBase {
        private string _artist;
        public string Artist {
            get => _artist;
            set => SetProperty(ref _artist, value);
        }

        private string _team;
        public string Team {
            get => _team;
            set => SetProperty(ref _team, value);
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

        private int _fileCount;
        public int FileCount {
            get => _fileCount;
            set => SetProperty(ref _fileCount, value);
        }

        private string _fileCountDisplay;
        public string FileCountDisplay {
            get => _fileCountDisplay;
            set => SetProperty(ref _fileCountDisplay, value);
        }

        private double _averageIssuesPerFile;
        public double AverageIssuesPerFile {
            get => _averageIssuesPerFile;
            set => SetProperty(ref _averageIssuesPerFile, value);
        }

        private string _averageIssuesPerFileDisplay;
        public string AverageIssuesPerFileDisplay {
            get => _averageIssuesPerFileDisplay;
            set => SetProperty(ref _averageIssuesPerFileDisplay, value);
        }

        private double _averageErrorsPerFile;
        public double AverageErrorsPerFile {
            get => _averageErrorsPerFile;
            set => SetProperty(ref _averageErrorsPerFile, value);
        }

        private string _averageErrorsPerFileDisplay;
        public string AverageErrorsPerFileDisplay {
            get => _averageErrorsPerFileDisplay;
            set => SetProperty(ref _averageErrorsPerFileDisplay, value);
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

        private string _supportLevel;
        public string SupportLevel {
            get => _supportLevel;
            set => SetProperty(ref _supportLevel, value);
        }

        private double _barPercent;
        public double BarPercent {
            get => _barPercent;
            set => SetProperty(ref _barPercent, value);
        }
    }
}