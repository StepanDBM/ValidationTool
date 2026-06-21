using System.Text.Json.Serialization;

namespace ValidationTool.UI.Models.DTOs.BudgetConfig {
    public class AnimationBudgetDto {
        [JsonPropertyName("key_count_max")]
        public int KeyCountMax { get; set; } = 10000;

        [JsonPropertyName("keyed_channels_max")]
        public int KeyedChannelsMax { get; set; } = 500;

        [JsonPropertyName("frame_range_max")]
        public int FrameRangeMax { get; set; } = 2000;

        [JsonPropertyName("animation_layers_max")]
        public int AnimationLayersMax { get; set; } = 10;

        [JsonPropertyName("clips_max")]
        public int ClipsMax { get; set; } = 50;
    }
}