using System.Collections.Generic;
using ValidationTool.UI.Models.DTOs.SceneSetup;

namespace ValidationTool.UI.ViewModels.SceneSetupView_Models {
    public class RenderLayersViewModel {
        public List<RenderLayerDto> RenderLayers { get; }

        public RenderLayersViewModel(List<RenderLayerDto> renderLayers) {
            RenderLayers = renderLayers ?? new List<RenderLayerDto>();
        }
    }
}