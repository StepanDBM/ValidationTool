using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using ValidationTool.UI.Models;

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
    // minimal DTO just for navigation
    internal class ValidationRunDto {
        public List<AssetDto> Assets { get; set; }
    }

    internal class AssetDto {
        public List<StageDto> Stages { get; set; }
    }

    internal class StageDto {
        public List<IssueResult> Issues { get; set; }
    }

}