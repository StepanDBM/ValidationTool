using System.Xml.Linq;

namespace ValidationTool.UI.ViewModels.ProfilesView_Models {
    public enum OverrideValueKind {
        Boolean,
        Integer,
        Decimal,
        String,
        JsonArray,
        Regex
    }

    public class OverridePickerOption {
        public string DisplayName { get; set; }
        public string PathSegment { get; set; }
        public string FullPath { get; set; }
        public OverrideValueKind ValueKind { get; set; }
        public string DefaultValueRaw { get; set; }
        public string HelpText { get; set; }

        public override string ToString() {
            if (!string.IsNullOrWhiteSpace(DisplayName)) {
                return DisplayName;
            }
            if (!string.IsNullOrWhiteSpace(PathSegment)) {
                return PathSegment;
            }
            return base.ToString();
        }
    }
}