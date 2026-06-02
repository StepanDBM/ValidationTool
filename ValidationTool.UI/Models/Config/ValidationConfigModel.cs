namespace ValidationTool.UI.Models.Config {
    public class ValidationConfigModel {
        public bool StrictMode { get; set; } = true;

        public bool FailOnFirstError { get; set; } = false;

        public bool AutoFixEnabled { get; set; } = false;

        public bool IncludeInfo { get; set; } = true;

        public bool IncludeWarnings { get; set; } = true;

        public bool DebugMode { get; set; } = false;
    }
}