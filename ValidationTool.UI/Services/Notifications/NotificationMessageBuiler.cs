using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using ValidationTool.UI.ViewModels;

namespace ValidationTool.Services.Notifications {
    public class NotificationMessageBuilder {
        public NotificationMessage Build(List<IssueViewModel> orderedIssues) {
            if (orderedIssues == null || orderedIssues.Count == 0) {
                return new NotificationMessage {
                    Title = "Validation Report",
                    Body = "No issues provided.",
                    RecipientId = string.Empty
                };
            }

            var first = orderedIssues[0];

            int errorCount = orderedIssues.Count(i => i.Severity == "ERROR");
            int warningCount = orderedIssues.Count(i => i.Severity == "WARNING");
            int infoCount = orderedIssues.Count(i => i.Severity == "INFO");

            var dccs = orderedIssues
                .Select(i => i.Dcc)
                .Where(d => !string.IsNullOrWhiteSpace(d))
                .Distinct()
                .OrderBy(d => d)
                .ToList();

            var sb = new StringBuilder();

            // --------------------------------------------------
            // HEADER // added icons jeej
            // --------------------------------------------------
            sb.AppendLine("*Validation report* 🚨");
            sb.AppendLine();

            sb.AppendLine($"*Artist:* {first.Artist?.ArtistName ?? "Unknown"}");
            sb.AppendLine($"*Team:* {first.Artist?.ArtistTeam ?? "Unknown"}");
            sb.AppendLine($"*Project:* {first.Artist?.ArtistProject ?? "Unknown"}");

            if (dccs.Count > 0) {
                sb.AppendLine($"*DCCs involved:* {string.Join(", ", dccs)}");
            }

            sb.AppendLine();

            // --------------------------------------------------
            // SUMMARY
            // --------------------------------------------------
            sb.AppendLine("*Summary*");
            sb.AppendLine($"• Total issues: *{orderedIssues.Count}*");
            sb.AppendLine($"• Errors: *{errorCount}*");
            sb.AppendLine($"• Warnings: *{warningCount}*");
            sb.AppendLine($"• Info: *{infoCount}*");
            sb.AppendLine();

            // --------------------------------------------------
            // DETAILS BY DCC -> FILE
            // --------------------------------------------------
            var issuesByDcc = orderedIssues
                .GroupBy(i => i.Dcc ?? "Unknown")
                .OrderBy(g => g.Key);

            foreach (var dccGroup in issuesByDcc) {
                int dccErrors = dccGroup.Count(i => i.Severity == "ERROR");
                int dccWarnings = dccGroup.Count(i => i.Severity == "WARNING");
                int dccInfos = dccGroup.Count(i => i.Severity == "INFO");

                sb.AppendLine($"*DCC: {dccGroup.Key}*");
                sb.AppendLine($"• Issues: {dccGroup.Count()} | Errors: {dccErrors} | Warnings: {dccWarnings} | Info: {dccInfos}");
                sb.AppendLine();

                var fileGroups = dccGroup
                    .GroupBy(i => i.OriginFile ?? "Unknown file")
                    .OrderBy(g => g.Key);

                foreach (var fileGroup in fileGroups) {
                    string filePath = fileGroup.Key;
                    string fileName = Path.GetFileName(filePath);

                    int fileErrors = fileGroup.Count(i => i.Severity == "ERROR");
                    int fileWarnings = fileGroup.Count(i => i.Severity == "WARNING");
                    int fileInfos = fileGroup.Count(i => i.Severity == "INFO");

                    sb.AppendLine($"*File:* `{fileName}`");
                    sb.AppendLine($"• Issues: {fileGroup.Count()} | Errors: {fileErrors} | Warnings: {fileWarnings} | Info: {fileInfos}");
                    sb.AppendLine($"• Path: `{filePath}`");
                    sb.AppendLine();

                    foreach (var issue in fileGroup) {
                        sb.AppendLine($"• *[{issue.Severity}]* `{issue.Check_name}`");

                        if (!string.IsNullOrWhiteSpace(issue.Asset_name)) {
                            sb.AppendLine($"  Asset: `{issue.Asset_name}`");
                        }

                        if (!string.IsNullOrWhiteSpace(issue.Message)) {
                            sb.AppendLine($"  Message: {issue.Message}");
                        }

                        if (!string.IsNullOrWhiteSpace(issue.Suggestion)) {
                            sb.AppendLine($"  _Suggestion:_ {issue.Suggestion}");
                        }

                        sb.AppendLine();
                    }
                }

                sb.AppendLine("────────────────────────");
                sb.AppendLine();
            }

            return new NotificationMessage {
                Title = $"Validation Report ({orderedIssues.Count} issues)",
                Body = sb.ToString(),
                RecipientId = first.Artist?.ArtistGmail ?? string.Empty
            };
        }
    }
}