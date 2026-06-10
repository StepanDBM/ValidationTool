using System;
using System.Collections.Generic;
using System.Text.Json.Serialization;

namespace ValidationTool.UI.Models.DTOs {
    public class LastRunsListDto {
        [JsonPropertyName("dcc")]
        public string Dcc { get; set; }
        [JsonPropertyName("runs")]
        public List<string> Runs { get; set; }
    }

    public class ValidationRunDto {
        [JsonPropertyName("summary")]
        public RunSummaryDto summary { get; set; }
        [JsonPropertyName("issues")]
        public List<ValidationIssueDto> issues { get; set; }
    }

    public class RunSummaryDto {
        [JsonPropertyName("run_id")]
        public string RunId { get; set; }

        [JsonPropertyName("timestamp")]
        public DateTime Timestamp { get; set; }

        [JsonPropertyName("dcc")]
        public string Dcc { get; set; }

        [JsonPropertyName("total_assets")]
        public int TotalAssets { get; set; }

        [JsonPropertyName("total_issues")]
        public int TotalIssues { get; set; }

        [JsonPropertyName("errors")]
        public int Errors { get; set; }

        [JsonPropertyName("warnings")]
        public int Warnings { get; set; }

        [JsonPropertyName("infos")]
        public int Infos { get; set; }
    }

    public class ValidationIssueDto {
        [JsonPropertyName("dcc")]
        public string Dcc { get; set; }

        [JsonPropertyName("asset_name")]
        public string AssetName { get; set; }

        [JsonPropertyName("check_name")]
        public string CheckName { get; set; }

        [JsonPropertyName("stage")]
        public string Stage { get; set; }

        [JsonPropertyName("timestamp")]
        public DateTime Timestamp { get; set; }

        [JsonPropertyName("severity")]
        public string Severity { get; set; }

        [JsonPropertyName("message")]
        public string Message { get; set; }

        [JsonPropertyName("suggestion")]
        public string Suggestion { get; set; }
    }
}