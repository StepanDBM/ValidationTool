using System.Collections.Generic;

namespace ValidationTool.UI.Models.Config {
    public class NamingRulesModel {
        public List<string> ValidPrefixes { get; set; } = new List<string>();
        public List<string> DefaultMayaNames { get; set; } = new List<string>();

        public string NamePattern { get; set; }
    }
}