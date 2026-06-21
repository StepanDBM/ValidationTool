using System.Collections.ObjectModel;
using System.Linq;

using ValidationTool.UI.Models.DTOs.BudgetConfig;
using ValidationTool.UI.ViewModels.General;
using ValidationTool.UI.Models.Items;

namespace ValidationTool.UI.ViewModels.BudgetsView_Models {
    public class BudgetsConfigViewModel : ViewModelBase {
        public BudgetConfigDto BudgetConfig { get; }

        public GeometryBudgetsViewModel Geometry { get; }
        public UvBudgetsViewModel Uv { get; }
        public MaterialBudgetsViewModel Materials { get; }
        public TextureBudgetsViewModel Textures { get; }
        public RiggingBudgetsViewModel Rigging { get; }
        public AnimationBudgetsViewModel Animation { get; }
        public LightingBudgetsViewModel Lighting { get; }
        public CameraBudgetsViewModel Camera { get; }
        public RenderBudgetsViewModel Render { get; }
        public OutputBudgetsViewModel Output { get; }
        public ColorManagementBudgetsViewModel ColorManagement { get; }
        public SceneHygieneBudgetsViewModel SceneHygiene { get; }
        public ExportBudgetsViewModel Export { get; }
        public PerformanceBudgetsViewModel Performance { get; }

        public ObservableCollection<BudgetSectionNavItemViewModel> Sections { get; }

        private BudgetSectionNavItemViewModel _selectedSection;
        public BudgetSectionNavItemViewModel SelectedSection {
            get => _selectedSection;
            set {
                if (SetProperty(ref _selectedSection, value))
                    UpdateCurrentSection();
            }
        }

        private BudgetSectionViewModelBase _currentSectionViewModel;
        public BudgetSectionViewModelBase CurrentSectionViewModel {
            get => _currentSectionViewModel;
            set => SetProperty(ref _currentSectionViewModel, value);
        }

        public BudgetsConfigViewModel(BudgetConfigDto budgetConfig = null) {
            BudgetConfig = budgetConfig ?? new BudgetConfigDto();

            Geometry = new GeometryBudgetsViewModel(BudgetConfig.Geometry);
            Uv = new UvBudgetsViewModel(BudgetConfig.Uv);
            Materials = new MaterialBudgetsViewModel(BudgetConfig.Materials);
            Textures = new TextureBudgetsViewModel(BudgetConfig.Textures);
            Rigging = new RiggingBudgetsViewModel(BudgetConfig.Rigging);
            Animation = new AnimationBudgetsViewModel(BudgetConfig.Animation);
            Lighting = new LightingBudgetsViewModel(BudgetConfig.Lighting);
            Camera = new CameraBudgetsViewModel(BudgetConfig.Camera);
            Render = new RenderBudgetsViewModel(BudgetConfig.Render);
            Output = new OutputBudgetsViewModel(BudgetConfig.Output);
            ColorManagement = new ColorManagementBudgetsViewModel(BudgetConfig.ColorManagement);
            SceneHygiene = new SceneHygieneBudgetsViewModel(BudgetConfig.SceneHygiene);
            Export = new ExportBudgetsViewModel(BudgetConfig.Export);
            Performance = new PerformanceBudgetsViewModel(BudgetConfig.Performance);

            Sections = new ObservableCollection<BudgetSectionNavItemViewModel>
            {
                new BudgetSectionNavItemViewModel { DisplayName = "Geometry", SectionType = BudgetSectionType.Geometry },
                new BudgetSectionNavItemViewModel { DisplayName = "UV", SectionType = BudgetSectionType.Uv },
                new BudgetSectionNavItemViewModel { DisplayName = "Materials", SectionType = BudgetSectionType.Materials },
                new BudgetSectionNavItemViewModel { DisplayName = "Textures", SectionType = BudgetSectionType.Textures },
                new BudgetSectionNavItemViewModel { DisplayName = "Rigging", SectionType = BudgetSectionType.Rigging },
                new BudgetSectionNavItemViewModel { DisplayName = "Animation", SectionType = BudgetSectionType.Animation },
                new BudgetSectionNavItemViewModel { DisplayName = "Lighting", SectionType = BudgetSectionType.Lighting },
                new BudgetSectionNavItemViewModel { DisplayName = "Camera", SectionType = BudgetSectionType.Camera },
                new BudgetSectionNavItemViewModel { DisplayName = "Render", SectionType = BudgetSectionType.Render },
                new BudgetSectionNavItemViewModel { DisplayName = "Output", SectionType = BudgetSectionType.Output },
                new BudgetSectionNavItemViewModel { DisplayName = "Color Management", SectionType = BudgetSectionType.ColorManagement },
                new BudgetSectionNavItemViewModel { DisplayName = "Scene Hygiene", SectionType = BudgetSectionType.SceneHygiene },
                new BudgetSectionNavItemViewModel { DisplayName = "Export", SectionType = BudgetSectionType.Export },
                new BudgetSectionNavItemViewModel { DisplayName = "Performance", SectionType = BudgetSectionType.Performance }
            };

            SelectedSection = Sections.FirstOrDefault();
        }

        private void UpdateCurrentSection() {
            if (SelectedSection == null) {
                CurrentSectionViewModel = null;
                return;
            }

            switch (SelectedSection.SectionType) {
                case BudgetSectionType.Geometry:
                    CurrentSectionViewModel = Geometry;
                    break;
                case BudgetSectionType.Uv:
                    CurrentSectionViewModel = Uv;
                    break;
                case BudgetSectionType.Materials:
                    CurrentSectionViewModel = Materials;
                    break;
                case BudgetSectionType.Textures:
                    CurrentSectionViewModel = Textures;
                    break;
                case BudgetSectionType.Rigging:
                    CurrentSectionViewModel = Rigging;
                    break;
                case BudgetSectionType.Animation:
                    CurrentSectionViewModel = Animation;
                    break;
                case BudgetSectionType.Lighting:
                    CurrentSectionViewModel = Lighting;
                    break;
                case BudgetSectionType.Camera:
                    CurrentSectionViewModel = Camera;
                    break;
                case BudgetSectionType.Render:
                    CurrentSectionViewModel = Render;
                    break;
                case BudgetSectionType.Output:
                    CurrentSectionViewModel = Output;
                    break;
                case BudgetSectionType.ColorManagement:
                    CurrentSectionViewModel = ColorManagement;
                    break;
                case BudgetSectionType.SceneHygiene:
                    CurrentSectionViewModel = SceneHygiene;
                    break;
                case BudgetSectionType.Export:
                    CurrentSectionViewModel = Export;
                    break;
                case BudgetSectionType.Performance:
                    CurrentSectionViewModel = Performance;
                    break;
                default:
                    CurrentSectionViewModel = Geometry;
                    break;
            }
        }
    }
}