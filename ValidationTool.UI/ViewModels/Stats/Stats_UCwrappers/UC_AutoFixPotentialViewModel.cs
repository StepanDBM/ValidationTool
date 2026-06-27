using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Globalization;
using System.Linq;
using ValidationTool.UI.Models.Stats;
using ValidationTool.UI.ViewModels.General;

namespace ValidationTool.UI.ViewModels.StatsView_Models {
    public class UC_AutoFixPotentialViewModel : ViewModelBase {
        public ObservableCollection<AutoFixPotentialItemViewModel> Items { get; } =
            new ObservableCollection<AutoFixPotentialItemViewModel>();

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

        private string _subtitle = "No fix-mode information loaded.";
        public string Subtitle {
            get => _subtitle;
            set => SetProperty(ref _subtitle, value);
        }

        public void Apply(IEnumerable<StatsFixModeItem> items) {
            Items.Clear();

            if (items == null) {
                TotalIssues = 0;
                MaxCount = 0;
                Subtitle = "No fix-mode information loaded.";
                return;
            }

            var list = items
                .Where(x => x != null)
                .OrderBy(x => GetFixModeOrder(x.FixMode))
                .ToList();

            TotalIssues = list.Sum(x => x.Count);
            MaxCount = list.Count > 0 ? list.Max(x => x.Count) : 0;

            foreach (var item in list) {
                double barPercent = MaxCount > 0
                    ? (double)item.Count / MaxCount * 100.0
                    : 0.0;

                Items.Add(new AutoFixPotentialItemViewModel {
                    FixMode = item.FixMode,
                    Count = item.Count,
                    CountDisplay = item.Count.ToString("N0", CultureInfo.InvariantCulture),
                    PercentOfTotal = item.PercentOfTotal,
                    PercentOfTotalDisplay = item.PercentOfTotal.ToString("0.0", CultureInfo.InvariantCulture) + "%",
                    BarPercent = barPercent,
                    Description = GetFixModeDescription(item.FixMode)
                });
            }

            Subtitle = TotalIssues > 0
                ? $"Grouped from {TotalIssues.ToString("N0", CultureInfo.InvariantCulture)} loaded issues."
                : "No fix-mode information loaded.";
        }

        private static int GetFixModeOrder(string fixMode) {
            var normalized = Normalize(fixMode);

            switch (normalized) {
                case "AUTO":
                    return 0;
                case "SEMI":
                    return 1;
                case "MANUAL":
                    return 2;
                case "NONE":
                    return 3;
                default:
                    return 99;
            }
        }

        private static string GetFixModeDescription(string fixMode) {
            var normalized = Normalize(fixMode);

            switch (normalized) {
                case "AUTO":
                    return "Can be fixed automatically.";
                case "SEMI":
                    return "Can be partially assisted.";
                case "MANUAL":
                    return "Requires artist or technical review.";
                case "NONE":
                    return "No fix action available.";
                default:
                    return "Unknown fix behavior.";
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

    public class AutoFixPotentialItemViewModel : ViewModelBase {
        private string _fixMode;
        public string FixMode {
            get => _fixMode;
            set => SetProperty(ref _fixMode, value);
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

        private double _barPercent;
        public double BarPercent {
            get => _barPercent;
            set => SetProperty(ref _barPercent, value);
        }

        private string _description;
        public string Description {
            get => _description;
            set => SetProperty(ref _description, value);
        }
    }
}