using System.Collections.Generic;
using System.Text.Json.Serialization;

namespace ValidationTool.UI.Models.Dto {
    public class ValidationRunDto {
        [JsonPropertyName("assets")]
        public List<AssetDto> Assets { get; set; }
    }

    public class AssetDto {
        [JsonPropertyName("stages")]
        public List<StageDto> Stages { get; set; }
    }

    public class StageDto {
        [JsonPropertyName("issues")]
        public List<IssueDto> Issues { get; set; }
    }

    public class IssueDto {
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
    }
}