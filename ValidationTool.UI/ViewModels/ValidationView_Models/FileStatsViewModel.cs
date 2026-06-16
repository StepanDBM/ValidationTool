using ValidationTool.UI.Models.DTOs;

namespace ValidationTool.UI.ViewModels.ValidationView_Models {
    public class FileStatsViewModel {
        public string FileName { get; set; }
        public string FilePath { get; set; }
        public int Issues { get; set; }
        public int Warnings { get; set; }
        public int Errors { get; set; }
        public SceneSetupDto SceneSetup { get; set; }
    }
}
