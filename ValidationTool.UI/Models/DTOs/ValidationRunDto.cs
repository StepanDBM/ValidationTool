using System;
using System.Collections.Generic;
using System.Text.Json.Serialization;
using ValidationTool.UI.ViewModels;

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
        public SceneSetupDto scene_setup {  get; set; }
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
        [JsonPropertyName("artist")]
        public ArtistDto Artist { get; set; }
        [JsonPropertyName("dcc")]
        public string Dcc { get; set; }
        [JsonPropertyName("origin_file")]
        public string OriginFile { get; set; }

        [JsonPropertyName("object_name")]
        public string ObjectName { get; set; }

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

    public class ArtistDto {

        [JsonPropertyName("name")]
        public string ArtistName { get; set; }
        [JsonPropertyName("id")]
        public string ArtistID { get; set; }
        [JsonPropertyName("level")]
        public string ArtistLevel { get; set; }
        [JsonPropertyName("lead")]
        public string LeadArtist { get; set; }
        [JsonPropertyName("team")]
        public string ArtistTeam { get; set; }
        [JsonPropertyName("project")]
        public string ArtistProject { get; set; }
        [JsonPropertyName("slack_id")]
        public string ArtistSlackID { get; set; }
        [JsonPropertyName("teams_id")]
        public string ArtistTeamsID { get; set; }
        [JsonPropertyName("gmail")]
        public string ArtistGmail { get; set; }

    }
}