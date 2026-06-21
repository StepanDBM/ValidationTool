using System.Text.Json.Serialization;

namespace ValidationTool.UI.Models.DTOs.BudgetConfig {
    public class ExportBudgetDto {
        [JsonPropertyName("export_file_size_mb_max")]
        public int ExportFileSizeMbMax { get; set; } = 500;

        [JsonPropertyName("draw_calls_max")]
        public int DrawCallsMax { get; set; } = 1000;

        [JsonPropertyName("submeshes_max")]
        public int SubmeshesMax { get; set; } = 20;

        [JsonPropertyName("lod_count_max")]
        public int LodCountMax { get; set; } = 4;

        [JsonPropertyName("collision_meshes_max")]
        public int CollisionMeshesMax { get; set; } = 10;
    }
}