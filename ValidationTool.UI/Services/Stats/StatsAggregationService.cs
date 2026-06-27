using System;
using System.Collections.Generic;
using System.Linq;
using ValidationTool.UI.Models.DTOs;
using ValidationTool.UI.Models.Stats;
using ValidationTool.UI.ViewModels;

namespace ValidationTool.UI.Services.Stats {
    public class StatsAggregationService {
        private enum FixModeBucket {
            Auto,
            Semi,
            Manual,
            None
        }


        private const double AutoFixMinutesSaved = 2.0;
        private const double SemiFixMinutesSaved = 1.0;

        public StatsDashboardSnapshot Build(
            IEnumerable<IssueViewModel> issues,
            IEnumerable<ValidationRunDto> runs,
            int topChecksLimit = 10,
            int criticalFilesLimit = 10,
            int teamLimit = 10,
            int artistLimit = 10) {
            var issueList = issues != null
                ? issues.Where(i => i != null).ToList()
                : new List<IssueViewModel>();

            var runList = runs != null
                ? runs.Where(r => r != null).ToList()
                : new List<ValidationRunDto>();

            var snapshot = new StatsDashboardSnapshot();

            snapshot.Kpi = BuildKpi(issueList, runList);
            snapshot.IssuesByStage = BuildIssuesByStage(issueList);
            snapshot.DccComparison = BuildDccComparison(issueList);
            snapshot.AutoFixPotential = BuildAutoFixPotential(issueList);
            snapshot.TopOffendingChecks = BuildTopOffendingChecks(issueList, topChecksLimit);
            snapshot.CriticalFiles = BuildCriticalFiles(issueList, criticalFilesLimit);
            snapshot.TeamHealth = BuildTeamHealth(issueList, teamLimit);
            snapshot.ArtistSupport = BuildArtistSupport(issueList, artistLimit);
            snapshot.SeverityMix = BuildSeverityMix(issueList);
            snapshot.FixModeByStage = BuildFixModeByStage(issueList);
            snapshot.PipelineRoi = BuildPipelineRoi(issueList);

            return snapshot;
        }

        private StatsKpiSnapshot BuildKpi(List<IssueViewModel> issues, List<ValidationRunDto> runs) {
            int totalIssues = issues.Count;
            int errors = issues.Count(i => IsSeverity(i, "ERROR"));
            int warnings = issues.Count(i => IsSeverity(i, "WARNING"));
            int info = issues.Count(i => IsSeverity(i, "INFO"));
            int hard = issues.Count(i => IsSeverity(i, "HARD"));

            int auto = 0;
            int semi = 0;
            int manual = 0;
            int none = 0;

            foreach (var issue in issues) {
                switch (GetFixModeBucket(issue)) {
                    case FixModeBucket.Auto:
                        auto++;
                        break;

                    case FixModeBucket.Semi:
                        semi++;
                        break;

                    case FixModeBucket.Manual:
                        manual++;
                        break;

                    case FixModeBucket.None:
                    default:
                        none++;
                        break;
                }
            }

            int fileCount = CountDistinctFiles(issues, runs);

            double autoPercent = totalIssues > 0
                ? (double)auto / totalIssues * 100.0
                : 0.0;

            double estimatedMinutes = auto * AutoFixMinutesSaved + semi * SemiFixMinutesSaved;

            return new StatsKpiSnapshot {
                LoadedRuns = runs.Count,
                TotalIssues = totalIssues,
                TotalErrors = errors,
                TotalWarnings = warnings,
                TotalInfo = info,
                TotalHard = hard,
                TotalFiles = fileCount,
                AutoFixableIssues = auto,
                SemiFixableIssues = semi,
                ManualIssues = manual,
                NoFixIssues = none,
                AutoFixablePercent = Round1(autoPercent),
                HealthScore = CalculateHealthScore(totalIssues, errors, warnings, hard, autoPercent),
                EstimatedSavedHours = Round1(estimatedMinutes / 60.0)
            };
        }

        private List<StatsBarItem> BuildIssuesByStage(List<IssueViewModel> issues) {
            int total = issues.Count;

            return issues
                .GroupBy(i => CleanKey(i.Stage, "Unknown Stage"), StringComparer.OrdinalIgnoreCase)
                .Select(g => new StatsBarItem {
                    Label = MakeDisplayName(g.Key),
                    Count = g.Count(),
                    PercentOfTotal = total > 0 ? Round1((double)g.Count() / total * 100.0) : 0.0,
                    SeverityScore = g.Sum(GetSeverityWeight)
                })
                .OrderByDescending(x => x.Count)
                .ThenBy(x => x.Label)
                .ToList();
        }

        private List<StatsDccItem> BuildDccComparison(List<IssueViewModel> issues) {
            return issues
                .GroupBy(i => CleanKey(i.Dcc, "Unknown DCC"), StringComparer.OrdinalIgnoreCase)
                .Select(g => {
                    int fileCount = g.Select(i => CleanKey(i.OriginFile, "Unknown File"))
                                     .Distinct(StringComparer.OrdinalIgnoreCase)
                                     .Count();

                    int errors = g.Count(i => IsSeverity(i, "ERROR"));
                    int total = g.Count();

                    return new StatsDccItem {
                        Dcc = g.Key,
                        TotalIssues = total,
                        Errors = errors,
                        Warnings = g.Count(i => IsSeverity(i, "WARNING")),
                        Info = g.Count(i => IsSeverity(i, "INFO")),
                        Hard = g.Count(i => IsSeverity(i, "HARD")),
                        FileCount = fileCount,
                        AverageErrorsPerFile = fileCount > 0 ? Round1((double)errors / fileCount) : 0.0,
                        AverageIssuesPerFile = fileCount > 0 ? Round1((double)total / fileCount) : 0.0,
                        SeverityScore = g.Sum(GetSeverityWeight)
                    };
                })
                .OrderByDescending(x => x.TotalIssues)
                .ThenBy(x => x.Dcc)
                .ToList();
        }

        private List<StatsFixModeItem> BuildAutoFixPotential(List<IssueViewModel> issues) {
            int total = issues.Count;

            int auto = 0;
            int semi = 0;
            int manual = 0;
            int none = 0;

            foreach (var issue in issues) {
                switch (GetFixModeBucket(issue)) {
                    case FixModeBucket.Auto:
                        auto++;
                        break;

                    case FixModeBucket.Semi:
                        semi++;
                        break;

                    case FixModeBucket.Manual:
                        manual++;
                        break;

                    case FixModeBucket.None:
                    default:
                        none++;
                        break;
                }
            }

            return new List<StatsFixModeItem> {
                new StatsFixModeItem {
                    FixMode = "Auto",
                    Count = auto,
                    PercentOfTotal = total > 0 ? Round1((double)auto / total * 100.0) : 0.0
                },
                new StatsFixModeItem {
                    FixMode = "Semi",
                    Count = semi,
                    PercentOfTotal = total > 0 ? Round1((double)semi / total * 100.0) : 0.0
                },
                new StatsFixModeItem {
                    FixMode = "Manual",
                    Count = manual,
                    PercentOfTotal = total > 0 ? Round1((double)manual / total * 100.0) : 0.0
                },
                new StatsFixModeItem {
                    FixMode = "None",
                    Count = none,
                    PercentOfTotal = total > 0 ? Round1((double)none / total * 100.0) : 0.0
                }
            };
        }

        private List<StatsCheckItem> BuildTopOffendingChecks(List<IssueViewModel> issues, int limit) {
            return issues
                .GroupBy(i => CleanKey(i.Check_name, "Unknown Check"), StringComparer.OrdinalIgnoreCase)
                .Select(g => new StatsCheckItem {
                    CheckName = g.Key,
                    Count = g.Count(),
                    Errors = g.Count(i => IsSeverity(i, "ERROR")),
                    Warnings = g.Count(i => IsSeverity(i, "WARNING")),
                    Info = g.Count(i => IsSeverity(i, "INFO")),
                    Hard = g.Count(i => IsSeverity(i, "HARD")),
                    TopStage = GetTopValue(g, i => CleanKey(i.Stage, "Unknown Stage")),
                    SeverityScore = g.Sum(GetSeverityWeight)
                })
                .OrderByDescending(x => x.Count)
                .ThenByDescending(x => x.SeverityScore)
                .ThenBy(x => x.CheckName)
                .Take(limit)
                .ToList();
        }

        private List<StatsCriticalFileItem> BuildCriticalFiles(List<IssueViewModel> issues, int limit) {
            return issues
                .GroupBy(i => CleanKey(i.OriginFile, "Unknown File"), StringComparer.OrdinalIgnoreCase)
                .Select(g => {
                    int total = g.Count();
                    int auto = g.Count(i => IsFixMode(i, "AUTO"));

                    return new StatsCriticalFileItem {
                        File = g.Key,
                        Team = GetTopValue(g, i => GetArtistTeam(i)),
                        Artist = GetTopValue(g, i => GetArtistName(i)),
                        Dcc = GetTopValue(g, i => CleanKey(i.Dcc, "Unknown DCC")),
                        TotalIssues = total,
                        Errors = g.Count(i => IsSeverity(i, "ERROR")),
                        Warnings = g.Count(i => IsSeverity(i, "WARNING")),
                        Info = g.Count(i => IsSeverity(i, "INFO")),
                        Hard = g.Count(i => IsSeverity(i, "HARD")),
                        AutoFixableIssues = auto,
                        AutoFixablePercent = total > 0 ? Round1((double)auto / total * 100.0) : 0.0,
                        TopStage = GetTopValue(g, i => CleanKey(i.Stage, "Unknown Stage")),
                        TopCheck = GetTopValue(g, i => CleanKey(i.Check_name, "Unknown Check")),
                        SeverityScore = g.Sum(GetSeverityWeight)
                    };
                })
                .OrderByDescending(x => x.SeverityScore)
                .ThenByDescending(x => x.Errors)
                .ThenByDescending(x => x.TotalIssues)
                .Take(limit)
                .ToList();
        }

        private List<StatsTeamHealthItem> BuildTeamHealth(List<IssueViewModel> issues, int limit) {
            return issues
                .GroupBy(i => GetArtistTeam(i), StringComparer.OrdinalIgnoreCase)
                .Select(g => {
                    int total = g.Count();
                    int errors = g.Count(i => IsSeverity(i, "ERROR"));
                    int fileCount = g.Select(i => CleanKey(i.OriginFile, "Unknown File"))
                                     .Distinct(StringComparer.OrdinalIgnoreCase)
                                     .Count();

                    int artistCount = g.Select(GetArtistName)
                                       .Distinct(StringComparer.OrdinalIgnoreCase)
                                       .Count();

                    return new StatsTeamHealthItem {
                        Team = g.Key,
                        TotalIssues = total,
                        Errors = errors,
                        Warnings = g.Count(i => IsSeverity(i, "WARNING")),
                        Info = g.Count(i => IsSeverity(i, "INFO")),
                        Hard = g.Count(i => IsSeverity(i, "HARD")),
                        FileCount = fileCount,
                        ArtistCount = artistCount,
                        AverageIssuesPerFile = fileCount > 0 ? Round1((double)total / fileCount) : 0.0,
                        AverageErrorsPerFile = fileCount > 0 ? Round1((double)errors / fileCount) : 0.0,
                        TopStage = GetTopValue(g, i => CleanKey(i.Stage, "Unknown Stage")),
                        TopCheck = GetTopValue(g, i => CleanKey(i.Check_name, "Unknown Check")),
                        SeverityScore = g.Sum(GetSeverityWeight)
                    };
                })
                .OrderByDescending(x => x.SeverityScore)
                .ThenByDescending(x => x.TotalIssues)
                .ThenBy(x => x.Team)
                .Take(limit)
                .ToList();
        }

        private List<StatsArtistSupportItem> BuildArtistSupport(List<IssueViewModel> issues, int limit) {
            return issues
                .GroupBy(i => GetArtistName(i), StringComparer.OrdinalIgnoreCase)
                .Select(g => {
                    int total = g.Count();
                    int errors = g.Count(i => IsSeverity(i, "ERROR"));
                    int fileCount = g.Select(i => CleanKey(i.OriginFile, "Unknown File"))
                                     .Distinct(StringComparer.OrdinalIgnoreCase)
                                     .Count();

                    int severityScore = g.Sum(GetSeverityWeight);
                    double avgIssuesPerFile = fileCount > 0 ? (double)total / fileCount : 0.0;
                    double avgErrorsPerFile = fileCount > 0 ? (double)errors / fileCount : 0.0;

                    return new StatsArtistSupportItem {
                        Artist = g.Key,
                        Team = GetTopValue(g, i => GetArtistTeam(i)),
                        TotalIssues = total,
                        Errors = errors,
                        Warnings = g.Count(i => IsSeverity(i, "WARNING")),
                        Info = g.Count(i => IsSeverity(i, "INFO")),
                        Hard = g.Count(i => IsSeverity(i, "HARD")),
                        FileCount = fileCount,
                        AverageIssuesPerFile = Round1(avgIssuesPerFile),
                        AverageErrorsPerFile = Round1(avgErrorsPerFile),
                        TopStage = GetTopValue(g, i => CleanKey(i.Stage, "Unknown Stage")),
                        TopCheck = GetTopValue(g, i => CleanKey(i.Check_name, "Unknown Check")),
                        SeverityScore = severityScore,
                        SupportLevel = GetSupportLevel(severityScore, avgErrorsPerFile, avgIssuesPerFile)
                    };
                })
                .OrderByDescending(x => x.SeverityScore)
                .ThenByDescending(x => x.Errors)
                .ThenBy(x => x.Artist)
                .Take(limit)
                .ToList();
        }

        private List<StatsSeverityItem> BuildSeverityMix(List<IssueViewModel> issues) {
            int total = issues.Count;

            var hard = issues.Count(i => IsSeverity(i, "HARD"));
            var errors = issues.Count(i => IsSeverity(i, "ERROR"));
            var warnings = issues.Count(i => IsSeverity(i, "WARNING"));
            var info = issues.Count(i => IsSeverity(i, "INFO"));

            return new List<StatsSeverityItem>
            {
                new StatsSeverityItem
                {
                    Severity = "Hard",
                    Count = hard,
                    PercentOfTotal = total > 0 ? Round1((double)hard / total * 100.0) : 0.0,
                    Weight = 10
                },
                new StatsSeverityItem
                {
                    Severity = "Errors",
                    Count = errors,
                    PercentOfTotal = total > 0 ? Round1((double)errors / total * 100.0) : 0.0,
                    Weight = 5
                },
                new StatsSeverityItem
                {
                    Severity = "Warnings",
                    Count = warnings,
                    PercentOfTotal = total > 0 ? Round1((double)warnings / total * 100.0) : 0.0,
                    Weight = 2
                },
                new StatsSeverityItem
                {
                    Severity = "Info",
                    Count = info,
                    PercentOfTotal = total > 0 ? Round1((double)info / total * 100.0) : 0.0,
                    Weight = 1
                }
            };
        }

        private List<StatsFixModeByStageItem> BuildFixModeByStage(List<IssueViewModel> issues) {
            return issues
                .GroupBy(i => CleanKey(i.Stage, "Unknown Stage"), StringComparer.OrdinalIgnoreCase)
                .Select(g => {
                    int auto = 0;
                    int semi = 0;
                    int manual = 0;
                    int none = 0;

                    foreach (var issue in g) {
                        switch (GetFixModeBucket(issue)) {
                            case FixModeBucket.Auto:
                                auto++;
                                break;

                            case FixModeBucket.Semi:
                                semi++;
                                break;

                            case FixModeBucket.Manual:
                                manual++;
                                break;

                            case FixModeBucket.None:
                            default:
                                none++;
                                break;
                        }
                    }

                    return new StatsFixModeByStageItem {
                        Stage = MakeDisplayName(g.Key),
                        Auto = auto,
                        Semi = semi,
                        Manual = manual,
                        None = none
                    };
                })
                .OrderByDescending(x => x.Total)
                .ThenBy(x => x.Stage)
                .ToList();
        }

        private StatsPipelineRoiSnapshot BuildPipelineRoi(List<IssueViewModel> issues) {
            int auto = issues.Count(i => IsFixMode(i, "AUTO"));
            int semi = issues.Count(i => IsFixMode(i, "SEMI"));
            int manual = issues.Count(i => IsFixMode(i, "MANUAL"));
            int none = issues.Count(IsNoFixMode);

            double minutes = auto * AutoFixMinutesSaved + semi * SemiFixMinutesSaved;

            var bestAutoDomain = issues
                .Where(i => GetFixModeBucket(i) == FixModeBucket.Auto)
                .GroupBy(i => CleanKey(i.Stage, "Unknown Stage"), StringComparer.OrdinalIgnoreCase)
                .Select(g => new {
                    Stage = MakeDisplayName(g.Key),
                    Count = g.Count()
                })
                .OrderByDescending(x => x.Count)
                .FirstOrDefault();

            return new StatsPipelineRoiSnapshot {
                AutoFixableIssues = auto,
                SemiFixableIssues = semi,
                ManualOnlyIssues = manual,
                NoFixIssues = none,
                EstimatedSavedMinutes = Round1(minutes),
                EstimatedSavedHours = Round1(minutes / 60.0),
                BestAutoFixDomain = bestAutoDomain != null ? bestAutoDomain.Stage : "None",
                BestAutoFixDomainCount = bestAutoDomain != null ? bestAutoDomain.Count : 0
            };
        }

        private int CountDistinctFiles(List<IssueViewModel> issues, List<ValidationRunDto> runs) {
            var countFromIssues = issues
                .Select(i => CleanKey(i.OriginFile, ""))
                .Where(x => !string.IsNullOrWhiteSpace(x))
                .Distinct(StringComparer.OrdinalIgnoreCase)
                .Count();

            if (countFromIssues > 0)
                return countFromIssues;

            return runs.Count;
        }

        private static bool IsSeverity(IssueViewModel issue, string severity) {
            return Normalize(issue != null ? issue.Severity : null) == Normalize(severity);
        }

        private static bool IsFixMode(IssueViewModel issue, string fixMode) {
            var raw = Normalize(issue != null ? issue.FixModeRaw : null);
            var target = Normalize(fixMode);

            return raw == target || raw.Contains(target);
        }

        private static bool IsNoFixMode(IssueViewModel issue) {
            var raw = Normalize(issue != null ? issue.FixModeRaw : null);

            return string.IsNullOrWhiteSpace(raw)
                   || raw == "NONE"
                   || raw == "NOFIX"
                   || raw == "NOTFIXABLE"
                   || raw == "N/A"
                   || raw == "NULL";
        }

        private static int GetSeverityWeight(IssueViewModel issue) {
            if (issue == null)
                return 0;

            var severity = Normalize(issue.Severity);

            switch (severity) {
                case "HARD":
                    return 10;
                case "ERROR":
                    return 5;
                case "WARNING":
                    return 2;
                case "INFO":
                    return 1;
                default:
                    return 0;
            }
        }

        private static int CalculateHealthScore(
            int totalIssues,
            int errors,
            int warnings,
            int hard,
            double autoFixablePercent) {
            if (totalIssues <= 0)
                return 100;

            double errorRatio = (double)errors / totalIssues;
            double warningRatio = (double)warnings / totalIssues;
            double hardRatio = (double)hard / totalIssues;

            double score = 100.0;

            score -= hardRatio * 60.0;
            score -= errorRatio * 45.0;
            score -= warningRatio * 18.0;
            score += autoFixablePercent * 0.10;

            if (score < 0)
                score = 0;

            if (score > 100)
                score = 100;

            return (int)Math.Round(score);
        }

        private static string GetSupportLevel(
            int severityScore,
            double avgErrorsPerFile,
            double avgIssuesPerFile) {
            if (severityScore >= 500 || avgErrorsPerFile >= 10 || avgIssuesPerFile >= 25)
                return "High";

            if (severityScore >= 150 || avgErrorsPerFile >= 4 || avgIssuesPerFile >= 10)
                return "Medium";

            return "Low";
        }

        private static string GetArtistName(IssueViewModel issue) {
            if (issue == null || issue.Artist == null)
                return "Unknown Artist";

            return CleanKey(issue.Artist.ArtistName, "Unknown Artist");
        }

        private static string GetArtistTeam(IssueViewModel issue) {
            if (issue == null || issue.Artist == null)
                return "Unknown Team";

            return CleanKey(issue.Artist.ArtistTeam, "Unknown Team");
        }

        private static string GetTopValue(
            IEnumerable<IssueViewModel> items,
            Func<IssueViewModel, string> selector) {
            var top = items
                .Select(selector)
                .Where(x => !string.IsNullOrWhiteSpace(x))
                .GroupBy(x => x, StringComparer.OrdinalIgnoreCase)
                .Select(g => new {
                    Value = g.Key,
                    Count = g.Count()
                })
                .OrderByDescending(x => x.Count)
                .ThenBy(x => x.Value)
                .FirstOrDefault();

            return top != null ? MakeDisplayName(top.Value) : "Unknown";
        }

        private static string CleanKey(string value, string fallback) {
            if (string.IsNullOrWhiteSpace(value))
                return fallback;

            return value.Trim();
        }

        private static string Normalize(string value) {
            if (string.IsNullOrWhiteSpace(value))
                return "";

            return value.Trim()
                .ToUpperInvariant()
                .Replace(" ", "")
                .Replace("_", "")
                .Replace("-", "");
        }

        private static string MakeDisplayName(string value) {
            if (string.IsNullOrWhiteSpace(value))
                return "Unknown";

            var cleaned = value.Trim().Replace("_", " ");

            if (cleaned.Length == 0)
                return "Unknown";

            if (cleaned.Length == 1)
                return cleaned.ToUpperInvariant();

            return char.ToUpperInvariant(cleaned[0]) + cleaned.Substring(1);
        }

        private static double Round1(double value) {
            return Math.Round(value, 1);
        }

        private static FixModeBucket GetFixModeBucket(IssueViewModel issue) {
            var raw = Normalize(issue != null ? issue.FixModeRaw : null);

            if (string.IsNullOrWhiteSpace(raw))
                return FixModeBucket.None;

            if (raw.Contains("AUTO"))
                return FixModeBucket.Auto;

            if (raw.Contains("SEMI"))
                return FixModeBucket.Semi;

            if (raw.Contains("MANUAL"))
                return FixModeBucket.Manual;

            if (raw.Contains("NONE") ||
                raw.Contains("NOFIX") ||
                raw.Contains("NOTFIXABLE") ||
                raw.Contains("NOTAVAILABLE") ||
                raw.Contains("NA") ||
                raw.Contains("NULL"))
                return FixModeBucket.None;

            return FixModeBucket.None;
        }
    }
}