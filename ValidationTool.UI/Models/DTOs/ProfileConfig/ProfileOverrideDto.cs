using System.Text.Json;

namespace ValidationTool.UI.Models.DTOs.Profiles {
    public class ProfileOverrideDto {
        public string path { get; set; }
        public JsonElement value { get; set; }
        public bool enabled { get; set; } = true;
    }
}