using System.Collections.Generic;

namespace ValidationTool.UI.Models.Stats {
    public class StatsDashboardSnapshot {
        public StatsKpiSnapshot Kpi { get; set; } = new StatsKpiSnapshot();

        public List<StatsBarItem> IssuesByStage { get; set; } = new List<StatsBarItem>();
        public List<StatsDccItem> DccComparison { get; set; } = new List<StatsDccItem>();
        public List<StatsFixModeItem> AutoFixPotential { get; set; } = new List<StatsFixModeItem>();
        public List<StatsCheckItem> TopOffendingChecks { get; set; } = new List<StatsCheckItem>();
        public List<StatsCriticalFileItem> CriticalFiles { get; set; } = new List<StatsCriticalFileItem>();
        public List<StatsTeamHealthItem> TeamHealth { get; set; } = new List<StatsTeamHealthItem>();
        public List<StatsArtistSupportItem> ArtistSupport { get; set; } = new List<StatsArtistSupportItem>();
        public List<StatsSeverityItem> SeverityMix { get; set; } = new List<StatsSeverityItem>();
        public List<StatsFixModeByStageItem> FixModeByStage { get; set; } = new List<StatsFixModeByStageItem>();

        public StatsPipelineRoiSnapshot PipelineRoi { get; set; } = new StatsPipelineRoiSnapshot();
    }

    public class StatsKpiSnapshot {
        public int LoadedRuns { get; set; }
        public int TotalIssues { get; set; }
        public int TotalErrors { get; set; }
        public int TotalWarnings { get; set; }
        public int TotalInfo { get; set; }
        public int TotalHard { get; set; }
        public int TotalFiles { get; set; }

        public int AutoFixableIssues { get; set; }
        public int SemiFixableIssues { get; set; }
        public int ManualIssues { get; set; }
        public int NoFixIssues { get; set; }

        public double AutoFixablePercent { get; set; }
        public int HealthScore { get; set; }

        public double EstimatedSavedHours { get; set; }
    }

    public class StatsBarItem {
        public string Label { get; set; }
        public int Count { get; set; }
        public double PercentOfTotal { get; set; }
        public int SeverityScore { get; set; }
    }

    public class StatsDccItem {
        public string Dcc { get; set; }
        public int TotalIssues { get; set; }
        public int Errors { get; set; }
        public int Warnings { get; set; }
        public int Info { get; set; }
        public int Hard { get; set; }
        public int FileCount { get; set; }
        public double AverageErrorsPerFile { get; set; }
        public double AverageIssuesPerFile { get; set; }
        public int SeverityScore { get; set; }
    }

    public class StatsFixModeItem {
        public string FixMode { get; set; }
        public int Count { get; set; }
        public double PercentOfTotal { get; set; }
    }

    public class StatsCheckItem {
        public string CheckName { get; set; }
        public int Count { get; set; }
        public int Errors { get; set; }
        public int Warnings { get; set; }
        public int Info { get; set; }
        public int Hard { get; set; }
        public string TopStage { get; set; }
        public int SeverityScore { get; set; }
    }

    public class StatsCriticalFileItem {
        public string File { get; set; }
        public string Team { get; set; }
        public string Artist { get; set; }
        public string Dcc { get; set; }

        public int TotalIssues { get; set; }
        public int Errors { get; set; }
        public int Warnings { get; set; }
        public int Info { get; set; }
        public int Hard { get; set; }

        public int AutoFixableIssues { get; set; }
        public double AutoFixablePercent { get; set; }

        public string TopStage { get; set; }
        public string TopCheck { get; set; }

        public int SeverityScore { get; set; }
    }

    public class StatsTeamHealthItem {
        public string Team { get; set; }

        public int TotalIssues { get; set; }
        public int Errors { get; set; }
        public int Warnings { get; set; }
        public int Info { get; set; }
        public int Hard { get; set; }

        public int FileCount { get; set; }
        public int ArtistCount { get; set; }

        public double AverageIssuesPerFile { get; set; }
        public double AverageErrorsPerFile { get; set; }

        public string TopStage { get; set; }
        public string TopCheck { get; set; }

        public int SeverityScore { get; set; }
    }

    public class StatsArtistSupportItem {
        public string Artist { get; set; }
        public string Team { get; set; }

        public int TotalIssues { get; set; }
        public int Errors { get; set; }
        public int Warnings { get; set; }
        public int Info { get; set; }
        public int Hard { get; set; }

        public int FileCount { get; set; }
        public double AverageIssuesPerFile { get; set; }
        public double AverageErrorsPerFile { get; set; }

        public string TopStage { get; set; }
        public string TopCheck { get; set; }

        public int SeverityScore { get; set; }
        public string SupportLevel { get; set; }
    }

    public class StatsSeverityItem {
        public string Severity { get; set; }
        public int Count { get; set; }
        public double PercentOfTotal { get; set; }
        public int Weight { get; set; }
    }

    public class StatsFixModeByStageItem {
        public string Stage { get; set; }

        public int Auto { get; set; }
        public int Semi { get; set; }
        public int Manual { get; set; }
        public int None { get; set; }

        public int Total => Auto + Semi + Manual + None;
    }

    public class StatsPipelineRoiSnapshot {
        public int AutoFixableIssues { get; set; }
        public int SemiFixableIssues { get; set; }
        public int ManualOnlyIssues { get; set; }
        public int NoFixIssues { get; set; }

        public double EstimatedSavedMinutes { get; set; }
        public double EstimatedSavedHours { get; set; }

        public string BestAutoFixDomain { get; set; }
        public int BestAutoFixDomainCount { get; set; }
    }
}