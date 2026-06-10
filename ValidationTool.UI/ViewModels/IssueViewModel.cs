using System.Collections.Generic;

namespace ValidationTool.UI.ViewModels {
    public class IssueViewModel {
        public string dcc { get; set; }
        public string asset_name { get; set; }
        public string check_name { get; set; }
        public string stage { get; set; }
        public string timestamp { get; set; }
        public string severity { get; set; }
        public string message { get; set; }
        public string suggestion { get; set; }
    }
}