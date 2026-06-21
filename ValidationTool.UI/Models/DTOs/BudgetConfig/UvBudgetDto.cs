using System.Text.Json.Serialization;

namespace ValidationTool.UI.Models.DTOs.BudgetConfig {
    public class UvBudgetDto {
        [JsonPropertyName("uv_sets_max")]
        public int UvSetsMax { get; set; } = 2;

        [JsonPropertyName("empty_uv_sets_max")]
        public int EmptyUvSetsMax { get; set; } = 0;

        [JsonPropertyName("duplicate_uv_set_names_max")]
        public int DuplicateUvSetNamesMax { get; set; } = 0;

        [JsonPropertyName("uv_shells_max")]
        public int UvShellsMax { get; set; } = 100;

        [JsonPropertyName("overlap_percent_max")]
        public double OverlapPercentMax { get; set; } = 0.0;

        [JsonPropertyName("out_of_range_uvs_max")]
        public int OutOfRangeUvsMax { get; set; } = 0;

        [JsonPropertyName("texel_density_min")]
        public double TexelDensityMin { get; set; } = 1.0;

        [JsonPropertyName("texel_density_max")]
        public double TexelDensityMax { get; set; } = 20.0;

        [JsonPropertyName("udim_tiles_max")]
        public int UdimTilesMax { get; set; } = 10;
    }
}