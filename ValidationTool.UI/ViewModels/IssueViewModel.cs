using System;
using ValidationTool.UI.Models;

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

        public string FixModeRaw { get; set; }


        public FixMode FixMode =>
            Enum.TryParse<FixMode>(FixModeRaw, true, out var result)
                ? result
                : FixMode.None;
        public bool IsAutoFix => FixMode == FixMode.Auto;
        public bool IsSemiFix => FixMode == FixMode.Semi;
        public bool OpenDCCfix => FixMode == FixMode.None;

        public bool ShowFixButton =>
            IsSemiFix || OpenDCCfix;

        public string FixButtonText =>
            FixMode == FixMode.Semi ? "HL - Fix"  :
            FixMode == FixMode.None ? "DCC - Fix" : "";

        public string FixTooltip =>
            FixMode == FixMode.Semi
                ? "Accept Headless fixes"
                : FixMode == FixMode.None
                ? "Open the file in DCC to fix manually"
                :"";

        public string ReportButtonText =>
            FixMode != FixMode.Auto ?
            Severity == "ERROR" ? "Report" : "Force Report":
            "Fixed Report";

        public string ReportToolTip =>
            Severity == "ERROR"
                ? "Send error report"
                : "Force report (this is only a warning)";
    }
}