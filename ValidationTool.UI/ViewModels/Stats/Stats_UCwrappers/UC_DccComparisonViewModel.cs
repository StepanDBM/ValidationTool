using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Globalization;
using System.Linq;
using ValidationTool.UI.Models.Stats;
using ValidationTool.UI.ViewModels.General;

namespace ValidationTool.UI.ViewModels.StatsView_Models {
    public class UC_DccComparisonViewModel : ViewModelBase {
        public ObservableCollection<DccComparisonItemViewModel> Items { get; } =
            new ObservableCollection<DccComparisonItemViewModel>();

        private int _totalIssues;
        public int TotalIssues {
            get => _totalIssues;
            set => SetProperty(ref _totalIssues, value);
        }

        private int _maxIssueCount;
        public int MaxIssueCount {
            get => _maxIssueCount;
            set => SetProperty(ref _maxIssueCount, value);
        }

        private string _subtitle = "No DCC information loaded.";
        public string Subtitle {
            get => _subtitle;
            set => SetProperty(ref _subtitle, value);
        }

        public void Apply(IEnumerable<StatsDccItem> items) {
            Items.Clear();

            if (items == null) {
                TotalIssues = 0;
                MaxIssueCount = 0;
                Subtitle = "No DCC information loaded.";
                return;
            }

            var list = items
                .Where(x => x != null)
                .OrderByDescending(x => x.TotalIssues)
                .ToList();

            TotalIssues = list.Sum(x => x.TotalIssues);
            MaxIssueCount = list.Count > 0 ? list.Max(x => x.TotalIssues) : 0;

            foreach (var item in list) {
                double issueBarPercent = MaxIssueCount > 0
                    ? (double)item.TotalIssues / MaxIssueCount * 100.0
                    : 0.0;

                double errorRatio = item.TotalIssues > 0
                    ? (double)item.Errors / item.TotalIssues * 100.0
                    : 0.0;

                double warningRatio = item.TotalIssues > 0
                    ? (double)item.Warnings / item.TotalIssues * 100.0
                    : 0.0;

                Items.Add(new DccComparisonItemViewModel {
                    Dcc = item.Dcc,
                    TotalIssues = item.TotalIssues,
                    TotalIssuesDisplay = item.TotalIssues.ToString("N0", CultureInfo.InvariantCulture),

                    Errors = item.Errors,
                    ErrorsDisplay = item.Errors.ToString("N0", CultureInfo.InvariantCulture),

                    Warnings = item.Warnings,
                    WarningsDisplay = item.Warnings.ToString("N0", CultureInfo.InvariantCulture),

                    Info = item.Info,
                    Hard = item.Hard,

                    FileCount = item.FileCount,
                    FileCountDisplay = item.FileCount.ToString("N0", CultureInfo.InvariantCulture),

                    AverageErrorsPerFile = item.AverageErrorsPerFile,
                    AverageErrorsPerFileDisplay = item.AverageErrorsPerFile.ToString("0.0", CultureInfo.InvariantCulture),

                    AverageIssuesPerFile = item.AverageIssuesPerFile,
                    AverageIssuesPerFileDisplay = item.AverageIssuesPerFile.ToString("0.0", CultureInfo.InvariantCulture),

                    SeverityScore = item.SeverityScore,

                    IssueBarPercent = issueBarPercent,
                    ErrorRatioPercent = errorRatio,
                    WarningRatioPercent = warningRatio,

                    ErrorRatioDisplay = errorRatio.ToString("0.0", CultureInfo.InvariantCulture) + "%",
                    WarningRatioDisplay = warningRatio.ToString("0.0", CultureInfo.InvariantCulture) + "%"
                });
            }

            Subtitle = TotalIssues > 0
                ? $"Grouped from {TotalIssues.ToString("N0", CultureInfo.InvariantCulture)} loaded issues."
                : "No DCC information loaded.";
        }
    }

    public class DccComparisonItemViewModel : ViewModelBase {
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

        private int _hard;
        public int Hard {
            get => _hard;
            set => SetProperty(ref _hard, value);
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

        private int _severityScore;
        public int SeverityScore {
            get => _severityScore;
            set => SetProperty(ref _severityScore, value);
        }

        private double _issueBarPercent;
        public double IssueBarPercent {
            get => _issueBarPercent;
            set => SetProperty(ref _issueBarPercent, value);
        }

        private double _errorRatioPercent;
        public double ErrorRatioPercent {
            get => _errorRatioPercent;
            set => SetProperty(ref _errorRatioPercent, value);
        }

        private double _warningRatioPercent;
        public double WarningRatioPercent {
            get => _warningRatioPercent;
            set => SetProperty(ref _warningRatioPercent, value);
        }

        private string _errorRatioDisplay;
        public string ErrorRatioDisplay {
            get => _errorRatioDisplay;
            set => SetProperty(ref _errorRatioDisplay, value);
        }

        private string _warningRatioDisplay;
        public string WarningRatioDisplay {
            get => _warningRatioDisplay;
            set => SetProperty(ref _warningRatioDisplay, value);
        }
    }
}