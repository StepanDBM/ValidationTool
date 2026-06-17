using System.Collections.Generic;
using ValidationTool.Services.Notifications;
using ValidationTool.UI.ViewModels;

namespace ValidationTool.UI.ViewModels {
    public class IssueViewModel {
        public ArtistViewModel Artist { get; set; }
        public string Dcc { get; set; }
        public string OriginFile { get; set; }
        public string Asset_name { get; set; }
        public string Check_name { get; set; }
        public string Stage { get; set; }
        public string Timestamp { get; set; }
        public string Severity { get; set; }
        public string Message { get; set; }
        public string Suggestion { get; set; }


        public string ReportButtonText =>
            Severity == "ERROR" ? "Report" : "Force Report";

        public string ReportToolTip => Severity == "ERROR"
            ? "Send error report"
            : "Force report (this is only a warning)";

    }
}