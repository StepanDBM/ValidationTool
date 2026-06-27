using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Globalization;
using System.Linq;
using ValidationTool.UI.Models.Stats;
using ValidationTool.UI.ViewModels.General;

namespace ValidationTool.UI.ViewModels.StatsView_Models {
    public class UC_TopOffendingChecksViewModel : ViewModelBase {
        public ObservableCollection<TopOffendingCheckItemViewModel> Items { get; } =
            new ObservableCollection<TopOffendingCheckItemViewModel>();

        private int _totalDisplayedIssues;
        public int TotalDisplayedIssues {
            get => _totalDisplayedIssues;
            set => SetProperty(ref _totalDisplayedIssues, value);
        }

        private int _maxCount;
        public int MaxCount {
            get => _maxCount;
            set => SetProperty(ref _maxCount, value);
        }

        private string _subtitle = "No check information loaded.";
        public string Subtitle {
            get => _subtitle;
            set => SetProperty(ref _subtitle, value);
        }

        public void Apply(IEnumerable<StatsCheckItem> items) {
            Items.Clear();

            if (items == null) {
                TotalDisplayedIssues = 0;
                MaxCount = 0;
                Subtitle = "No check information loaded.";
                return;
            }

            var list = items
                .Where(x => x != null)
                .OrderByDescending(x => x.Count)
                .ThenByDescending(x => x.SeverityScore)
                .ThenBy(x => x.CheckName)
                .ToList();

            TotalDisplayedIssues = list.Sum(x => x.Count);
            MaxCount = list.Count > 0 ? list.Max(x => x.Count) : 0;

            foreach (var item in list) {
                double barPercent = MaxCount > 0
                    ? (double)item.Count / MaxCount * 100.0
                    : 0.0;

                Items.Add(new TopOffendingCheckItemViewModel {
                    CheckName = item.CheckName,
                    Count = item.Count,
                    CountDisplay = item.Count.ToString("N0", CultureInfo.InvariantCulture),

                    Errors = item.Errors,
                    ErrorsDisplay = item.Errors.ToString("N0", CultureInfo.InvariantCulture),

                    Warnings = item.Warnings,
                    WarningsDisplay = item.Warnings.ToString("N0", CultureInfo.InvariantCulture),

                    Info = item.Info,
                    InfoDisplay = item.Info.ToString("N0", CultureInfo.InvariantCulture),

                    Hard = item.Hard,
                    HardDisplay = item.Hard.ToString("N0", CultureInfo.InvariantCulture),

                    TopStage = item.TopStage,
                    SeverityScore = item.SeverityScore,
                    SeverityScoreDisplay = item.SeverityScore.ToString("N0", CultureInfo.InvariantCulture),

                    BarPercent = barPercent
                });
            }

            Subtitle = list.Count > 0
                ? $"Top {list.Count} most frequent validation checks."
                : "No check information loaded.";
        }
    }

    public class TopOffendingCheckItemViewModel : ViewModelBase {
        private string _checkName;
        public string CheckName {
            get => _checkName;
            set => SetProperty(ref _checkName, value);
        }

        private int _count;
        public int Count {
            get => _count;
            set => SetProperty(ref _count, value);
        }

        private string _countDisplay;
        public string CountDisplay {
            get => _countDisplay;
            set => SetProperty(ref _countDisplay, value);
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

        private string _topStage;
        public string TopStage {
            get => _topStage;
            set => SetProperty(ref _topStage, value);
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

        private double _barPercent;
        public double BarPercent {
            get => _barPercent;
            set => SetProperty(ref _barPercent, value);
        }
    }
}