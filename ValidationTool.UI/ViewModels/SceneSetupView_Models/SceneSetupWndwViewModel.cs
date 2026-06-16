using System.Collections.ObjectModel;
using System.ComponentModel;
using ValidationTool.UI.Models.DTOs;

namespace ValidationTool.UI.ViewModels.SceneSetupView_Models {
    public class SceneSetupWndwViewModel : INotifyPropertyChanged {
        public event PropertyChangedEventHandler PropertyChanged;

        private void RaisePropertyChanged(string name) {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
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
            SceneSetup = sceneSetup;

            Sections.Add(new SceneSetupNavItem { Key = "general", Title = "General" });
            Sections.Add(new SceneSetupNavItem { Key = "render", Title = "Render Settings" });
            Sections.Add(new SceneSetupNavItem { Key = "output", Title = "Output Settings" });
            Sections.Add(new SceneSetupNavItem { Key = "sampling", Title = "Sampling" });
            Sections.Add(new SceneSetupNavItem { Key = "raydepth", Title = "Ray Depth" });
            Sections.Add(new SceneSetupNavItem { Key = "color", Title = "Color Management" });
            Sections.Add(new SceneSetupNavItem { Key = "camera", Title = "Camera Setup" });
            Sections.Add(new SceneSetupNavItem { Key = "layers", Title = "Render Layers" });
            Sections.Add(new SceneSetupNavItem { Key = "aovs", Title = "AOVs" });

            SelectedSection = Sections[0];
        }

        private void UpdateCurrentSection() {
            if (SelectedSection == null || SceneSetup == null) {
                CurrentSectionData = null;
                return;
            }

            switch (SelectedSection.Key) {
                case "general":
                    CurrentSectionData = SceneSetup;
                    break;

                case "render":
                    CurrentSectionData = SceneSetup.RenderSettings;
                    break;

                case "output":
                    CurrentSectionData = SceneSetup.OutputSettings;
                    break;

                case "sampling":
                    CurrentSectionData = SceneSetup.SamplingSettings;
                    break;

                case "raydepth":
                    CurrentSectionData = SceneSetup.RayDepthSettings;
                    break;

                case "color":
                    CurrentSectionData = SceneSetup.ColorManagement;
                    break;

                case "camera":
                    CurrentSectionData = SceneSetup.CameraSetup;
                    break;

                case "layers":
                    CurrentSectionData = SceneSetup.RenderLayers;
                    break;

                case "aovs":
                    CurrentSectionData = SceneSetup.Aovs;
                    break;

                default:
                    CurrentSectionData = null;
                    break;
            }
        }
    }
}
