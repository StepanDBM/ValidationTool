using System.Text.Json.Serialization;

namespace ValidationTool.UI.Models.DTOs.BudgetConfig {
    public class BudgetConfigDto {
        [JsonPropertyName("geometry")]
        public GeometryBudgetDto Geometry { get; set; } = new GeometryBudgetDto();

        [JsonPropertyName("uv")]
        public UvBudgetDto Uv { get; set; } = new UvBudgetDto();

        [JsonPropertyName("materials")]
        public MaterialBudgetDto Materials { get; set; } = new MaterialBudgetDto();

        [JsonPropertyName("textures")]
        public TextureBudgetDto Textures { get; set; } = new TextureBudgetDto();

        [JsonPropertyName("rigging")]
        public RiggingBudgetDto Rigging { get; set; } = new RiggingBudgetDto();

        [JsonPropertyName("animation")]
        public AnimationBudgetDto Animation { get; set; } = new AnimationBudgetDto();

        [JsonPropertyName("lighting")]
        public LightingBudgetDto Lighting { get; set; } = new LightingBudgetDto();

        [JsonPropertyName("camera")]
        public CameraBudgetDto Camera { get; set; } = new CameraBudgetDto();

        [JsonPropertyName("render")]
        public RenderBudgetDto Render { get; set; } = new RenderBudgetDto();

        [JsonPropertyName("output")]
        public OutputBudgetDto Output { get; set; } = new OutputBudgetDto();

        [JsonPropertyName("color_management")]
        public ColorManagementBudgetDto ColorManagement { get; set; } = new ColorManagementBudgetDto();

        [JsonPropertyName("scene_hygiene")]
        public SceneHygieneBudgetDto SceneHygiene { get; set; } = new SceneHygieneBudgetDto();

        [JsonPropertyName("export")]
        public ExportBudgetDto Export { get; set; } = new ExportBudgetDto();

        [JsonPropertyName("performance")]
        public PerformanceBudgetDto Performance { get; set; } = new PerformanceBudgetDto();
    }
}
