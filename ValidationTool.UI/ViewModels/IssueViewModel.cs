using System.Collections.Generic;

namespace ValidationTool.UI.ViewModels {
    public class IssueViewModel {
        public string AssetName { get; set; }
        public string CheckName { get; set; }
        public string Severity { get; set; }
        public string Message { get; set; }
        public string Suggestion { get; set; }

        public bool IsError => Severity == "ERROR";
        public bool IsWarning => Severity == "WARNING";
        public bool IsInfo => Severity == "INFO";
    }
}