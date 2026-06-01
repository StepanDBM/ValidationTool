using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using ValidationTool.UI.ViewModels;

namespace ValidationTool.UI.Models {
    public class ValidationRun {
        public Summary Summary { get; set; }
        public List<AssetResult> Assets { get; set; }
    }

    public class Summary {
        
    }

    public class AssetResult {
        
    }

    public class StageResult {
        
    }

    public class IssueResult {
        public string AssetName { get; set; }
        public string CheckName { get; set; }
        public string Severity { get; set; }
        public string Message { get; set; }
        public string Suggestion { get; set; }
        private IssueViewModel CreateIssueViewModel(IssueResult issue) {
            return new IssueViewModel {
                AssetName = issue.AssetName,
                CheckName = issue.CheckName,
                Severity = issue.Severity,
                Message = issue.Message,
                Suggestion = issue.Suggestion
            };
        }
    }
}