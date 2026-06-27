using System.Collections.Generic;

namespace ValidationTool.UI.Models.DTOs.Profiles {
    public class ProfileDto {
        public string id { get; set; }
        public string name { get; set; }
        public string description { get; set; }
        public List<string> dcc { get; set; } = new List<string>();
        public List<string> enabled_categories { get; set; } = new List<string>();
        public List<ProfileOverrideDto> overrides { get; set; } = new List<ProfileOverrideDto>();

        public override string ToString() {
            if (!string.IsNullOrWhiteSpace(name)) {
                return name;
            }
            if(!string.IsNullOrWhiteSpace(id)) {
                return id;
            }
            return base.ToString();
        }
    }
}