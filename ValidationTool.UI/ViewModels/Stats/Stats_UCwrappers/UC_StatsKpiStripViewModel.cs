using System;
using ValidationTool.UI.Models.Stats;
using ValidationTool.UI.ViewModels.General;

namespace ValidationTool.UI.ViewModels.StatsView_Models {
    public class UC_StatsKpiStripViewModel : ViewModelBase {
        private int _totalIssues;
        public int TotalIssues {
            get => _totalIssues;
            set => SetProperty(ref _totalIssues, value);
        }

        private int _errors;
        public int Errors {
            get => _errors;
            set => SetProperty(ref _errors, value);
        }

        private int _warnings;
        public int Warnings {
            get => _warnings;
            set => SetProperty(ref _warnings, value);
        }

        private int _files;
        public int Files {
            get => _files;
            set => SetProperty(ref _files, value);
        }

        private double _autoFixablePercent;
        public double AutoFixablePercent {
            get => _autoFixablePercent;
            set => SetProperty(ref _autoFixablePercent, value);
        }

        private int _healthScore;
        public int HealthScore {
            get => _healthScore;
            set => SetProperty(ref _healthScore, value);
        }

        public void Apply(StatsKpiSnapshot kpi) {
            if (kpi == null)
                return;
            TotalIssues = kpi.TotalIssues;
            Errors = kpi.TotalErrors;
            Warnings = kpi.TotalWarnings;
            Files = kpi.TotalFiles;
            AutoFixablePercent = kpi.AutoFixablePercent;
            HealthScore = kpi.HealthScore;
        }
    }
}