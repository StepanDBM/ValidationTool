using System.Collections.Generic;
using ValidationTool.UI.ViewModels;

namespace ValidationTool.UI.ViewModels {
    public class IssueViewModel {
        public string Artist { get; set; }
        public string A_lv{ get; set; }
        public string Dcc { get; set; }
        public string Asset_name { get; set; }
        public string Check_name { get; set; }
        public string Stage { get; set; }
        public string Timestamp { get; set; }
        public string Severity { get; set; }
        public string Message { get; set; }
        public string Suggestion { get; set; }
    }
}