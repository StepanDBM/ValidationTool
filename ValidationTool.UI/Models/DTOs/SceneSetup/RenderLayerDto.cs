using System.Collections.Generic;
using System.Text.Json.Serialization;

namespace ValidationTool.UI.Models.DTOs.SceneSetup {
    public class RenderLayerDto {
        [JsonPropertyName("name")]
        public string Name { get; set; }

        [JsonPropertyName("enabled")]
        public bool Enabled { get; set; }

        [JsonPropertyName("renderable")]
        public bool Renderable { get; set; }

        [JsonPropertyName("is_active")]
        public bool IsActive { get; set; }

        [JsonPropertyName("camera_override")]
        public string CameraOverride { get; set; }

        [JsonPropertyName("material_override")]
        public string MaterialOverride { get; set; }

        [JsonPropertyName("light_overrides")]
        public List<string> LightOverrides { get; set; }

        [JsonPropertyName("object_overrides")]
        public List<string> ObjectOverrides { get; set; }

        [JsonPropertyName("collection_overrides")]
        public List<string> CollectionOverrides { get; set; }

        [JsonPropertyName("has_members")]
        public bool HasMembers { get; set; }

        [JsonPropertyName("member_count")]
        public int MemberCount { get; set; }

        [JsonPropertyName("has_valid_name")]
        public bool HasValidName { get; set; }

        [JsonPropertyName("is_required")]
        public bool IsRequired { get; set; }
    }
}