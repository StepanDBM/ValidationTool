using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Globalization;
using System.Linq;
using ValidationTool.UI.Models.Stats;
using ValidationTool.UI.ViewModels.General;

namespace ValidationTool.UI.ViewModels.StatsView_Models {
    public class UC_SeverityMixViewModel : ViewModelBase {
        public ObservableCollection<SeverityMixItemViewModel> Items { get; } =
            new ObservableCollection<SeverityMixItemViewModel>();

        private string _subtitle = "No severity information loaded.";
        public string Subtitle {
            get => _subtitle;
            set => SetProperty(ref _subtitle, value);
        }

        private int _totalIssues;
        public int TotalIssues {
            get => _totalIssues;
            set => SetProperty(ref _totalIssues, value);
        }

        private int _maxCount;
        public int MaxCount {
            get => _maxCount;
            set => SetProperty(ref _maxCount, value);
        }

        public void Apply(IEnumerable<StatsSeverityItem> items) {
            Items.Clear();

            if (items == null) {
                TotalIssues = 0;
                MaxCount = 0;
                Subtitle = "No severity information loaded.";
                return;
            }

            var list = items
                .Where(x => x != null)
                .OrderBy(x => GetSeverityOrder(x.Severity))
                .ToList();

            TotalIssues = list.Sum(x => x.Count);
            MaxCount = list.Count > 0 ? list.Max(x => x.Count) : 0;

            foreach (var item in list) {
                double barPercent = MaxCount > 0
                    ? (double)item.Count / MaxCount * 100.0
                    : 0.0;

                Items.Add(new SeverityMixItemViewModel {
                    Severity = item.Severity,
                    Count = item.Count,
                    CountDisplay = item.Count.ToString("N0", CultureInfo.InvariantCulture),
                    PercentOfTotal = item.PercentOfTotal,
                    PercentOfTotalDisplay = item.PercentOfTotal.ToString("0.0", CultureInfo.InvariantCulture) + "%",
                    Weight = item.Weight,
                    WeightDisplay = item.Weight.ToString("N0", CultureInfo.InvariantCulture),
                    BarPercent = barPercent
                });
            }

            Subtitle = TotalIssues > 0
                ? $"Grouped from {TotalIssues.ToString("N0", CultureInfo.InvariantCulture)} loaded issues."
                : "No severity information loaded.";
        }

        private static int GetSeverityOrder(string severity) {
            var normalized = Normalize(severity);

            switch (normalized) {
                case "HARD":
                case "HARDS":
                    return 0;

                case "ERROR":
                case "ERRORS":
                    return 1;

                case "WARNING":
                case "WARNINGS":
                    return 2;

                case "INFO":
                case "INFOS":
                    return 3;

                default:
                    return 99;
            }
        }

        private static string Normalize(string value) {
            if (string.IsNullOrWhiteSpace(value))
                return "";

            return value
                .Trim()
                .ToUpperInvariant()
                .Replace(" ", "")
                .Replace("_", "")
                .Replace("-", "");
        }
    }

    public class SeverityMixItemViewModel : ViewModelBase {
        private string _severity;
        public string Severity {
            get => _severity;
            set => SetProperty(ref _severity, value);
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

        private double _percentOfTotal;
        public double PercentOfTotal {
            get => _percentOfTotal;
            set => SetProperty(ref _percentOfTotal, value);
        }

        private string _percentOfTotalDisplay;
        public string PercentOfTotalDisplay {
            get => _percentOfTotalDisplay;
            set => SetProperty(ref _percentOfTotalDisplay, value);
        }

        private int _weight;
        public int Weight {
            get => _weight;
            set => SetProperty(ref _weight, value);
        }

        private string _weightDisplay;
        public string WeightDisplay {
            get => _weightDisplay;
            set => SetProperty(ref _weightDisplay, value);
        }

        private double _barPercent;
        public double BarPercent {
            get => _barPercent;
            set => SetProperty(ref _barPercent, value);
        }
    }
}