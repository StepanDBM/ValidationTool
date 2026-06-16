using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Globalization;
using ValidationTool.UI.Models.DTOs;
using ValidationTool.UI.Models.DTOs.SceneSetup;

namespace ValidationTool.UI.ViewModels.SceneSetupView_Models {
    public class SceneSetupWndwViewModel : INotifyPropertyChanged {
        public event PropertyChangedEventHandler PropertyChanged;

        private void RaisePropertyChanged(string propertyName) {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }

        public SceneSetupDto SceneSetup { get; }

        public ObservableCollection<SceneSetupNavItem> Sections { get; }
            = new ObservableCollection<SceneSetupNavItem>();

        private SceneSetupNavItem _selectedSection;
        public SceneSetupNavItem SelectedSection {
            get => _selectedSection;
            set {
                _selectedSection = value;
                RaisePropertyChanged(nameof(SelectedSection));
                UpdateCurrentSection();
            }
        }

        private object _currentSectionData;
        public object CurrentSectionData {
            get => _currentSectionData;
            set {
                _currentSectionData = value;
                RaisePropertyChanged(nameof(CurrentSectionData));
            }
        }

        public SceneSetupWndwViewModel(SceneSetupDto sceneSetup) {
            SceneSetup = sceneSetup ?? new SceneSetupDto();
            //just for null-cases
            SceneSetup.RenderSettings = SceneSetup.RenderSettings ?? new RenderSettingsDto();
            SceneSetup.OutputSettings = SceneSetup.OutputSettings ?? new OutputSettingsDto();
            SceneSetup.SamplingSettings = SceneSetup.SamplingSettings ?? new SamplingSettingsDto();
            SceneSetup.RayDepthSettings = SceneSetup.RayDepthSettings ?? new RayDepthSettingsDto();
            SceneSetup.ColorManagement = SceneSetup.ColorManagement ?? new ColorManagementDto();
            SceneSetup.CameraSetup = SceneSetup.CameraSetup ?? new CameraSetupDto();
            SceneSetup.RenderLayers = SceneSetup.RenderLayers ?? new System.Collections.Generic.List<RenderLayerDto>();
            SceneSetup.Aovs = SceneSetup.Aovs ?? new System.Collections.Generic.List<AovDto>();

            Sections.Add(new SceneSetupNavItem { Key = "general", Title = "General" });
            Sections.Add(new SceneSetupNavItem { Key = "render", Title = "Render Settings" });
            Sections.Add(new SceneSetupNavItem { Key = "output", Title = "Output Settings" });
            Sections.Add(new SceneSetupNavItem { Key = "sampling", Title = "Sampling" });
            Sections.Add(new SceneSetupNavItem { Key = "raydepth", Title = "Ray Depth" });
            Sections.Add(new SceneSetupNavItem { Key = "color", Title = "Color Management" });
            Sections.Add(new SceneSetupNavItem { Key = "camera", Title = "Camera Setup" });
            Sections.Add(new SceneSetupNavItem { Key = "layers", Title = "Render Layers" });
            Sections.Add(new SceneSetupNavItem { Key = "aovs", Title = "AOVs" });

            if (Sections.Count > 0) {
                SelectedSection = Sections[0];
            }
        }

        private void UpdateCurrentSection() {
            if (SelectedSection == null || SceneSetup == null) {
                CurrentSectionData = null;
                return;
            }

            switch (SelectedSection.Key) {
                case "general":
                    CurrentSectionData = new SceneSetupGeneralViewModel(SceneSetup);
                    break;

                case "render":
                    CurrentSectionData = new RenderSettingsViewModel(SceneSetup.RenderSettings);
                    break;

                case "output":
                    CurrentSectionData = new OutputSettingsViewModel(SceneSetup.OutputSettings);
                    break;

                case "sampling":
                    CurrentSectionData = new SamplingSettingsViewModel(SceneSetup.SamplingSettings);
                    break;

                case "raydepth":
                    CurrentSectionData = new RayDepthSettingsViewModel(SceneSetup.RayDepthSettings);
                    break;

                case "color":
                    CurrentSectionData = new ColorManagementViewModel(SceneSetup.ColorManagement);
                    break;

                case "camera":
                    CurrentSectionData = new CameraSetupViewModel(SceneSetup.CameraSetup);
                    break;

                case "layers":
                    CurrentSectionData = new RenderLayersViewModel(SceneSetup.RenderLayers);
                    break;

                case "aovs":
                    CurrentSectionData = new AovsViewModel(SceneSetup.Aovs);
                    break;

                default:
                    CurrentSectionData = null;
                    break;
            }
        }
    }
}