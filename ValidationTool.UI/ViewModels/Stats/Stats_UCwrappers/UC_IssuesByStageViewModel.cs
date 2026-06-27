using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Globalization;
using System.Linq;
using ValidationTool.UI.Models.Stats;
using ValidationTool.UI.ViewModels.General;

namespace ValidationTool.UI.ViewModels.StatsView_Models {
    public class UC_IssuesByStageViewModel : ViewModelBase {
        public ObservableCollection<IssuesByStageItemViewModel> Items { get; } =
            new ObservableCollection<IssuesByStageItemViewModel>();

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

        private string _subtitle = "No stage information loaded.";
        public string Subtitle {
            get => _subtitle;
            set => SetProperty(ref _subtitle, value);
        }

        public void Apply(IEnumerable<StatsBarItem> items) {
            Items.Clear();

            if (items == null) {
                TotalIssues = 0;
                MaxCount = 0;
                Subtitle = "No stage information loaded.";
                return;
            }

            var list = items
                .Where(x => x != null)
                .OrderByDescending(x => x.Count)
                .ToList();

            TotalIssues = list.Sum(x => x.Count);
            MaxCount = list.Count > 0 ? list.Max(x => x.Count) : 0;

            foreach (var item in list) {
                double barPercent = MaxCount > 0
                    ? (double)item.Count / MaxCount * 100.0
                    : 0.0;

                Items.Add(new IssuesByStageItemViewModel {
                    Stage = item.Label,
                    Count = item.Count,
                    CountDisplay = item.Count.ToString("N0", CultureInfo.InvariantCulture),
                    PercentOfTotal = item.PercentOfTotal,
                    PercentOfTotalDisplay = item.PercentOfTotal.ToString("0.0", CultureInfo.InvariantCulture) + "%",
                    BarPercent = barPercent,
                    SeverityScore = item.SeverityScore
                });
            }

            Subtitle = TotalIssues > 0
                ? $"Grouped from {TotalIssues.ToString("N0", CultureInfo.InvariantCulture)} loaded issues."
                : "No stage information loaded.";
        }
    }

    public class IssuesByStageItemViewModel : ViewModelBase {
        private string _stage;
        public string Stage {
            get => _stage;
            set => SetProperty(ref _stage, value);
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

        private int _severityScore;
        public int SeverityScore {
            get => _severityScore;
            set => SetProperty(ref _severityScore, value);
        }
    }
}