using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Globalization;
using System.Linq;
using ValidationTool.UI.Models.Stats;
using ValidationTool.UI.ViewModels.General;

namespace ValidationTool.UI.ViewModels.StatsView_Models {
    public class UC_FixModeByStageViewModel : ViewModelBase {
        public ObservableCollection<FixModeByStageItemViewModel> Items { get; } =
            new ObservableCollection<FixModeByStageItemViewModel>();

        private string _subtitle = "No fix-mode by stage information loaded.";
        public string Subtitle {
            get => _subtitle;
            set => SetProperty(ref _subtitle, value);
        }

        private int _totalIssues;
        public int TotalIssues {
            get => _totalIssues;
            set => SetProperty(ref _totalIssues, value);
        }

        private int _maxStageTotal;
        public int MaxStageTotal {
            get => _maxStageTotal;
            set => SetProperty(ref _maxStageTotal, value);
        }

        public void Apply(IEnumerable<StatsFixModeByStageItem> items) {
            Items.Clear();

            if (items == null) {
                TotalIssues = 0;
                MaxStageTotal = 0;
                Subtitle = "No fix-mode by stage information loaded.";
                return;
            }

            var list = items
                .Where(x => x != null)
                .OrderByDescending(x => x.Total)
                .ThenBy(x => x.Stage)
                .ToList();

            TotalIssues = list.Sum(x => x.Total);
            MaxStageTotal = list.Count > 0 ? list.Max(x => x.Total) : 0;

            foreach (var item in list) {
                double stageBarPercent = MaxStageTotal > 0
                    ? (double)item.Total / MaxStageTotal * 100.0
                    : 0.0;

                double autoPercent = item.Total > 0 ? (double)item.Auto / item.Total * 100.0 : 0.0;
                double semiPercent = item.Total > 0 ? (double)item.Semi / item.Total * 100.0 : 0.0;
                double manualPercent = item.Total > 0 ? (double)item.Manual / item.Total * 100.0 : 0.0;
                double nonePercent = item.Total > 0 ? (double)item.None / item.Total * 100.0 : 0.0;

                Items.Add(new FixModeByStageItemViewModel {
                    Stage = item.Stage,

                    Total = item.Total,
                    TotalDisplay = item.Total.ToString("N0", CultureInfo.InvariantCulture),

                    Auto = item.Auto,
                    AutoDisplay = item.Auto.ToString("N0", CultureInfo.InvariantCulture),
                    AutoPercent = autoPercent,
                    AutoPercentDisplay = autoPercent.ToString("0.0", CultureInfo.InvariantCulture) + "%",

                    Semi = item.Semi,
                    SemiDisplay = item.Semi.ToString("N0", CultureInfo.InvariantCulture),
                    SemiPercent = semiPercent,
                    SemiPercentDisplay = semiPercent.ToString("0.0", CultureInfo.InvariantCulture) + "%",

                    Manual = item.Manual,
                    ManualDisplay = item.Manual.ToString("N0", CultureInfo.InvariantCulture),
                    ManualPercent = manualPercent,
                    ManualPercentDisplay = manualPercent.ToString("0.0", CultureInfo.InvariantCulture) + "%",

                    None = item.None,
                    NoneDisplay = item.None.ToString("N0", CultureInfo.InvariantCulture),
                    NonePercent = nonePercent,
                    NonePercentDisplay = nonePercent.ToString("0.0", CultureInfo.InvariantCulture) + "%",

                    StageBarPercent = stageBarPercent
                });
            }

            Subtitle = TotalIssues > 0
                ? $"Grouped from {TotalIssues.ToString("N0", CultureInfo.InvariantCulture)} loaded issues."
                : "No fix-mode by stage information loaded.";
        }
    }

    public class FixModeByStageItemViewModel : ViewModelBase {
        private string _stage;
        public string Stage {
            get => _stage;
            set => SetProperty(ref _stage, value);
        }

        private int _total;
        public int Total {
            get => _total;
            set => SetProperty(ref _total, value);
        }

        private string _totalDisplay;
        public string TotalDisplay {
            get => _totalDisplay;
            set => SetProperty(ref _totalDisplay, value);
        }

        private int _auto;
        public int Auto {
            get => _auto;
            set => SetProperty(ref _auto, value);
        }

        private string _autoDisplay;
        public string AutoDisplay {
            get => _autoDisplay;
            set => SetProperty(ref _autoDisplay, value);
        }

        private double _autoPercent;
        public double AutoPercent {
            get => _autoPercent;
            set => SetProperty(ref _autoPercent, value);
        }

        private string _autoPercentDisplay;
        public string AutoPercentDisplay {
            get => _autoPercentDisplay;
            set => SetProperty(ref _autoPercentDisplay, value);
        }

        private int _semi;
        public int Semi {
            get => _semi;
            set => SetProperty(ref _semi, value);
        }

        private string _semiDisplay;
        public string SemiDisplay {
            get => _semiDisplay;
            set => SetProperty(ref _semiDisplay, value);
        }

        private double _semiPercent;
        public double SemiPercent {
            get => _semiPercent;
            set => SetProperty(ref _semiPercent, value);
        }

        private string _semiPercentDisplay;
        public string SemiPercentDisplay {
            get => _semiPercentDisplay;
            set => SetProperty(ref _semiPercentDisplay, value);
        }

        private int _manual;
        public int Manual {
            get => _manual;
            set => SetProperty(ref _manual, value);
        }

        private string _manualDisplay;
        public string ManualDisplay {
            get => _manualDisplay;
            set => SetProperty(ref _manualDisplay, value);
        }

        private double _manualPercent;
        public double ManualPercent {
            get => _manualPercent;
            set => SetProperty(ref _manualPercent, value);
        }

        private string _manualPercentDisplay;
        public string ManualPercentDisplay {
            get => _manualPercentDisplay;
            set => SetProperty(ref _manualPercentDisplay, value);
        }

        private int _none;
        public int None {
            get => _none;
            set => SetProperty(ref _none, value);
        }

        private string _noneDisplay;
        public string NoneDisplay {
            get => _noneDisplay;
            set => SetProperty(ref _noneDisplay, value);
        }

        private double _nonePercent;
        public double NonePercent {
            get => _nonePercent;
            set => SetProperty(ref _nonePercent, value);
        }

        private string _nonePercentDisplay;
        public string NonePercentDisplay {
            get => _nonePercentDisplay;
            set => SetProperty(ref _nonePercentDisplay, value);
        }

        private double _stageBarPercent;
        public double StageBarPercent {
            get => _stageBarPercent;
            set => SetProperty(ref _stageBarPercent, value);
        }
    }
}
