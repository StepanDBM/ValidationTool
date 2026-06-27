using System.Globalization;
using ValidationTool.UI.Models.Stats;
using ValidationTool.UI.ViewModels.General;

namespace ValidationTool.UI.ViewModels.StatsView_Models {
    public class UC_PipelineRoiViewModel : ViewModelBase {
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

        private int _semiFixableIssues;
        public int SemiFixableIssues {
            get => _semiFixableIssues;
            set => SetProperty(ref _semiFixableIssues, value);
        }

        private string _semiFixableIssuesDisplay;
        public string SemiFixableIssuesDisplay {
            get => _semiFixableIssuesDisplay;
            set => SetProperty(ref _semiFixableIssuesDisplay, value);
        }

        private int _manualOnlyIssues;
        public int ManualOnlyIssues {
            get => _manualOnlyIssues;
            set => SetProperty(ref _manualOnlyIssues, value);
        }

        private string _manualOnlyIssuesDisplay;
        public string ManualOnlyIssuesDisplay {
            get => _manualOnlyIssuesDisplay;
            set => SetProperty(ref _manualOnlyIssuesDisplay, value);
        }

        private int _noFixIssues;
        public int NoFixIssues {
            get => _noFixIssues;
            set => SetProperty(ref _noFixIssues, value);
        }

        private string _noFixIssuesDisplay;
        public string NoFixIssuesDisplay {
            get => _noFixIssuesDisplay;
            set => SetProperty(ref _noFixIssuesDisplay, value);
        }

        private double _estimatedSavedMinutes;
        public double EstimatedSavedMinutes {
            get => _estimatedSavedMinutes;
            set => SetProperty(ref _estimatedSavedMinutes, value);
        }

        private string _estimatedSavedMinutesDisplay;
        public string EstimatedSavedMinutesDisplay {
            get => _estimatedSavedMinutesDisplay;
            set => SetProperty(ref _estimatedSavedMinutesDisplay, value);
        }

        private double _estimatedSavedHours;
        public double EstimatedSavedHours {
            get => _estimatedSavedHours;
            set => SetProperty(ref _estimatedSavedHours, value);
        }

        private string _estimatedSavedHoursDisplay;
        public string EstimatedSavedHoursDisplay {
            get => _estimatedSavedHoursDisplay;
            set => SetProperty(ref _estimatedSavedHoursDisplay, value);
        }

        private string _bestAutoFixDomain;
        public string BestAutoFixDomain {
            get => _bestAutoFixDomain;
            set => SetProperty(ref _bestAutoFixDomain, value);
        }

        private int _bestAutoFixDomainCount;
        public int BestAutoFixDomainCount {
            get => _bestAutoFixDomainCount;
            set => SetProperty(ref _bestAutoFixDomainCount, value);
        }

        private string _bestAutoFixDomainCountDisplay;
        public string BestAutoFixDomainCountDisplay {
            get => _bestAutoFixDomainCountDisplay;
            set => SetProperty(ref _bestAutoFixDomainCountDisplay, value);
        }

        private string _subtitle = "No pipeline ROI information loaded.";
        public string Subtitle {
            get => _subtitle;
            set => SetProperty(ref _subtitle, value);
        }

        private double _autoBarPercent;
        public double AutoBarPercent {
            get => _autoBarPercent;
            set => SetProperty(ref _autoBarPercent, value);
        }

        private double _semiBarPercent;
        public double SemiBarPercent {
            get => _semiBarPercent;
            set => SetProperty(ref _semiBarPercent, value);
        }

        private double _manualBarPercent;
        public double ManualBarPercent {
            get => _manualBarPercent;
            set => SetProperty(ref _manualBarPercent, value);
        }

        private double _noneBarPercent;
        public double NoneBarPercent {
            get => _noneBarPercent;
            set => SetProperty(ref _noneBarPercent, value);
        }

        public void Apply(StatsPipelineRoiSnapshot roi) {
            if (roi == null) {
                Reset();
                return;
            }

            AutoFixableIssues = roi.AutoFixableIssues;
            SemiFixableIssues = roi.SemiFixableIssues;
            ManualOnlyIssues = roi.ManualOnlyIssues;
            NoFixIssues = roi.NoFixIssues;

            EstimatedSavedMinutes = roi.EstimatedSavedMinutes;
            EstimatedSavedHours = roi.EstimatedSavedHours;

            BestAutoFixDomain = string.IsNullOrWhiteSpace(roi.BestAutoFixDomain)
                ? "None"
                : roi.BestAutoFixDomain;

            BestAutoFixDomainCount = roi.BestAutoFixDomainCount;

            AutoFixableIssuesDisplay = AutoFixableIssues.ToString("N0", CultureInfo.InvariantCulture);
            SemiFixableIssuesDisplay = SemiFixableIssues.ToString("N0", CultureInfo.InvariantCulture);
            ManualOnlyIssuesDisplay = ManualOnlyIssues.ToString("N0", CultureInfo.InvariantCulture);
            NoFixIssuesDisplay = NoFixIssues.ToString("N0", CultureInfo.InvariantCulture);

            EstimatedSavedMinutesDisplay = EstimatedSavedMinutes.ToString("N1", CultureInfo.InvariantCulture) + " min";
            EstimatedSavedHoursDisplay = EstimatedSavedHours.ToString("N1", CultureInfo.InvariantCulture) + " h";

            BestAutoFixDomainCountDisplay = BestAutoFixDomainCount.ToString("N0", CultureInfo.InvariantCulture);

            int max = AutoFixableIssues;

            if (SemiFixableIssues > max)
                max = SemiFixableIssues;

            if (ManualOnlyIssues > max)
                max = ManualOnlyIssues;

            if (NoFixIssues > max)
                max = NoFixIssues;

            AutoBarPercent = max > 0 ? (double)AutoFixableIssues / max * 100.0 : 0.0;
            SemiBarPercent = max > 0 ? (double)SemiFixableIssues / max * 100.0 : 0.0;
            ManualBarPercent = max > 0 ? (double)ManualOnlyIssues / max * 100.0 : 0.0;
            NoneBarPercent = max > 0 ? (double)NoFixIssues / max * 100.0 : 0.0;

            Subtitle = "Estimated production time recovered through automated and assisted fixes.";
        }

        private void Reset() {
            AutoFixableIssues = 0;
            SemiFixableIssues = 0;
            ManualOnlyIssues = 0;
            NoFixIssues = 0;

            EstimatedSavedMinutes = 0;
            EstimatedSavedHours = 0;

            BestAutoFixDomain = "None";
            BestAutoFixDomainCount = 0;

            AutoFixableIssuesDisplay = "0";
            SemiFixableIssuesDisplay = "0";
            ManualOnlyIssuesDisplay = "0";
            NoFixIssuesDisplay = "0";

            EstimatedSavedMinutesDisplay = "0.0 min";
            EstimatedSavedHoursDisplay = "0.0 h";
            BestAutoFixDomainCountDisplay = "0";

            AutoBarPercent = 0;
            SemiBarPercent = 0;
            ManualBarPercent = 0;
            NoneBarPercent = 0;

            Subtitle = "No pipeline ROI information loaded.";
        }
    }
}