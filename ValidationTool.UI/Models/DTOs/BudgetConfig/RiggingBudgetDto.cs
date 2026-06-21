using System.Text.Json.Serialization;

namespace ValidationTool.UI.Models.DTOs.BudgetConfig {
    public class RiggingBudgetDto {
        [JsonPropertyName("joint_count_max")]
        public int JointCountMax { get; set; } = 256;

        [JsonPropertyName("deform_joints_max")]
        public int DeformJointsMax { get; set; } = 128;

        [JsonPropertyName("controls_max")]
        public int ControlsMax { get; set; } = 300;

        [JsonPropertyName("constraints_max")]
        public int ConstraintsMax { get; set; } = 200;

        [JsonPropertyName("blendshapes_max")]
        public int BlendshapesMax { get; set; } = 100;

        [JsonPropertyName("influences_per_vertex_max")]
        public int InfluencesPerVertexMax { get; set; } = 4;
    }
}
