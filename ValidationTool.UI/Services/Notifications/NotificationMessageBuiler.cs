using System;
using System.Collections.Generic;
using System.Diagnostics;
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

            var sb = new StringBuilder();

            var first = orderedIssues[0];

            sb.AppendLine($"Project: {first.Artist?.ArtistProject}");
            sb.AppendLine($"DCC: {first.Dcc}");
            sb.AppendLine($"Artist: {first.Artist?.ArtistName}");
            sb.AppendLine($"Team: {first.Artist?.ArtistTeam}");
            sb.AppendLine();

            string currentFile = null;

            foreach (var issue in orderedIssues) {
                if (currentFile != issue.OriginFile) {
                    currentFile = issue.OriginFile;

                    sb.AppendLine();
                    sb.AppendLine("--------------------------------------------------");
                    sb.AppendLine($"FILE: {currentFile}");
                    sb.AppendLine(issue.Asset_name);
                    sb.AppendLine("--------------------------------------------------");
                }

                sb.AppendLine($"[{issue.Severity}] {issue.Check_name}");
                sb.AppendLine($"Message: {issue.Message}");

                if (!string.IsNullOrWhiteSpace(issue.Suggestion)) {
                    sb.AppendLine($"Suggestion: {issue.Suggestion}");
                }

                sb.AppendLine();
            }

            NotificationMessage completeMessage = new NotificationMessage {
                Title = $"Validation Report ({orderedIssues.Count} issues)",
                Body = sb.ToString(),
                RecipientId = orderedIssues[0].Artist?.ArtistGmail
                            ?? string.Empty
            };
            return completeMessage;
        }
    }
}