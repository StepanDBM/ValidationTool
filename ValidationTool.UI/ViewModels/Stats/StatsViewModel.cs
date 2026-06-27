using System;
using System.Collections.ObjectModel;
using System.Windows.Input;
using ValidationTool.UI.Commands;
using ValidationTool.UI.Models.DTOs;
using ValidationTool.UI.Models.Stats;
using ValidationTool.UI.Services.Stats;
using ValidationTool.UI.ViewModels.General;

namespace ValidationTool.UI.ViewModels.StatsView_Models {
    public class StatsViewModel : ViewModelBase {
        private readonly ObservableCollection<IssueViewModel> _issues;
        private readonly ObservableCollection<ValidationRunDto> _runs;
        private readonly StatsAggregationService _aggregationService;

        public UC_StatsKpiStripViewModel KpiStripVM { get; }
        public UC_IssuesByStageViewModel IssuesByStageVM { get; }
        public UC_DccComparisonViewModel DccComparisonVM { get; }
        public UC_AutoFixPotentialViewModel AutoFixPotentialVM { get; }
        public UC_TopOffendingChecksViewModel TopOffendingChecksVM { get; }
        public UC_CriticalFilesRankingViewModel CriticalFilesRankingVM { get; }
        public UC_TeamHealthViewModel TeamHealthVM { get; }
        public UC_ArtistSupportSummaryViewModel ArtistSupportSummaryVM { get; }
        public UC_SeverityMixViewModel SeverityMixVM { get; }
        public UC_FixModeByStageViewModel FixModeByStageVM { get; }
        public UC_PipelineRoiViewModel PipelineRoiVM { get; }

        public ICommand RefreshStatsCommand { get; }

        private string _statusMessage;
        public string StatusMessage {
            get => _statusMessage;
            set => SetProperty(ref _statusMessage, value);
        }

        private int _loadedRuns;
        public int LoadedRuns {
            get => _loadedRuns;
            set => SetProperty(ref _loadedRuns, value);
        }

        private int _loadedIssues;
        public int LoadedIssues {
            get => _loadedIssues;
            set => SetProperty(ref _loadedIssues, value);
        }

        private DateTime? _lastRefreshTime;
        public DateTime? LastRefreshTime {
            get => _lastRefreshTime;
            set => SetProperty(ref _lastRefreshTime, value);
        }

        public StatsViewModel(
            ObservableCollection<IssueViewModel> issues,
            ObservableCollection<ValidationRunDto> runs) {
            _issues = issues ?? new ObservableCollection<IssueViewModel>();
            _runs = runs ?? new ObservableCollection<ValidationRunDto>();
            _aggregationService = new StatsAggregationService();

            KpiStripVM = new UC_StatsKpiStripViewModel();
            IssuesByStageVM = new UC_IssuesByStageViewModel();
            DccComparisonVM = new UC_DccComparisonViewModel();
            AutoFixPotentialVM = new UC_AutoFixPotentialViewModel();
            TopOffendingChecksVM = new UC_TopOffendingChecksViewModel();
            CriticalFilesRankingVM = new UC_CriticalFilesRankingViewModel();
            TeamHealthVM = new UC_TeamHealthViewModel();
            ArtistSupportSummaryVM = new UC_ArtistSupportSummaryViewModel();
            SeverityMixVM = new UC_SeverityMixViewModel();
            FixModeByStageVM = new UC_FixModeByStageViewModel();
            PipelineRoiVM = new UC_PipelineRoiViewModel();

            RefreshStatsCommand = new RelayCommand(RefreshStats);

            RefreshStats();
        }

        public void RefreshStats() {
            try {
                var snapshot = _aggregationService.Build(_issues, _runs);

                ApplySnapshot(snapshot);

                LoadedRuns = snapshot.Kpi.LoadedRuns;
                LoadedIssues = snapshot.Kpi.TotalIssues;
                LastRefreshTime = DateTime.Now;

                StatusMessage = $"Stats refreshed. Runs: {LoadedRuns} | Issues: {LoadedIssues}";

            } catch (Exception ex) {
                StatusMessage = $"Stats refresh failed: {ex.Message}";
            }
        }

        private void ApplySnapshot(StatsDashboardSnapshot snapshot) {
            if (snapshot == null)
                return;

            KpiStripVM.Apply(snapshot.Kpi);
            IssuesByStageVM.Apply(snapshot.IssuesByStage);
            DccComparisonVM.Apply(snapshot.DccComparison);
            AutoFixPotentialVM.Apply(snapshot.AutoFixPotential);
            TopOffendingChecksVM.Apply(snapshot.TopOffendingChecks);
            CriticalFilesRankingVM.Apply(snapshot.CriticalFiles);
            TeamHealthVM.Apply(snapshot.TeamHealth);
            ArtistSupportSummaryVM.Apply(snapshot.ArtistSupport);
            SeverityMixVM.Apply(snapshot.SeverityMix);
            FixModeByStageVM.Apply(snapshot.FixModeByStage);
            PipelineRoiVM.Apply(snapshot.PipelineRoi);
        }
    }
}