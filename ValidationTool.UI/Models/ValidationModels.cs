using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.Json.Serialization;
using ValidationTool.UI.ViewModels;

namespace ValidationTool.UI.Models {
    public class ValidationRun {

    }

    public class IssueResult {
        [JsonPropertyName("asset_name")]
        public string AssetName { get; set; }

        [JsonPropertyName("check_name")]
        public string CheckName { get; set; }

        [JsonPropertyName("severity")]
        public string Severity { get; set; }

        [JsonPropertyName("message")]
        public string Message { get; set; }

        [JsonPropertyName("suggestion")]
        public string Suggestion { get; set; }

        private IssueViewModel CreateIssueViewModel(IssueResult issue) {
            return new IssueViewModel {
                AssetName = issue.AssetName,
                CheckName = issue.CheckName,
                Severity = issue.Severity,
                Message = issue.Message,
                Suggestion = issue.Suggestion
            };
        }
    }
}