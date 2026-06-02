using System.Collections.Generic;

namespace ValidationTool.UI.Models.Config {
    public class ValidationProfileModel {
        public List<string> EnabledCategories { get; set; } = new List<string>();

        public List<string> EnabledChecks { get; set; }
        public List<string> DisabledChecks { get; set; }

        public bool StrictMode { get; set; } = true;
    }
}