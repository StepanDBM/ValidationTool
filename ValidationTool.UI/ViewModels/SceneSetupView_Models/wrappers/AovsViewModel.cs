using System.Collections.Generic;
using ValidationTool.UI.Models.DTOs.SceneSetup;

namespace ValidationTool.UI.ViewModels.SceneSetupView_Models {
    public class AovsViewModel {
        public List<AovDto> Aovs { get; }

        public AovsViewModel(List<AovDto> aovs) {
            Aovs = aovs ?? new List<AovDto>();
        }
    }
}