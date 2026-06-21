using System.Text.Json.Serialization;

namespace ValidationTool.UI.Models.DTOs.BudgetConfig {
    public class SceneHygieneBudgetDto {
        [JsonPropertyName("unknown_nodes_max")]
        public int UnknownNodesMax { get; set; } = 0;

        [JsonPropertyName("duplicate_names_max")]
        public int DuplicateNamesMax { get; set; } = 0;

        [JsonPropertyName("namespaces_max")]
        public int NamespacesMax { get; set; } = 5;

        [JsonPropertyName("broken_references_max")]
        public int BrokenReferencesMax { get; set; } = 0;

        [JsonPropertyName("missing_references_max")]
        public int MissingReferencesMax { get; set; } = 0;

        [JsonPropertyName("script_nodes_max")]
        public int ScriptNodesMax { get; set; } = 0;

        [JsonPropertyName("expressions_max")]
        public int ExpressionsMax { get; set; } = 0;
    }
}
