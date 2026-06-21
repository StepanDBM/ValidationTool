using System.Text.Json.Serialization;

namespace ValidationTool.UI.Models.DTOs.BudgetConfig {
    public class GeometryBudgetDto {
        [JsonPropertyName("vertices_max")]
        public int VerticesMax { get;   set; } = 50000;

        [JsonPropertyName("triangles_max")]
        public int TrianglesMax { get; set; } = 100000;

        [JsonPropertyName("faces_max")]
        public int FacesMax { get; set; } = 50000;

        [JsonPropertyName("edges_max")]
        public int EdgesMax { get; set; } = 150000;

        [JsonPropertyName("ngons_max")]
        public int NgonsMax { get; set; } = 0;

        [JsonPropertyName("lamina_faces_max")]
        public int LaminaFacesMax { get; set; } = 0;

        [JsonPropertyName("isolated_vertices_max")]
        public int IsolatedVerticesMax { get; set; } = 0;

        [JsonPropertyName("hard_edges_max")]
        public int HardEdgesMax { get; set; } = 1000;

        [JsonPropertyName("mesh_count_max")]
        public int MeshCountMax { get; set; } = 50;

        [JsonPropertyName("shells_max")]
        public int ShellsMax { get; set; } = 20;

        [JsonPropertyName("bounding_box_diagonal_max")]
        public double BoundingBoxDiagonalMax { get; set; } = 10000.0;

        [JsonPropertyName("scale_max")]
        public double ScaleMax { get; set; } = 1000.0;

        [JsonPropertyName("non_uniform_scale_ratio_max")]
        public double NonUniformScaleRatioMax { get; set; } = 10.0;
    }
}