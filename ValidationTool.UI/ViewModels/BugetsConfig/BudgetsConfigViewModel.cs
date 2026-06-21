using System.Collections.ObjectModel;
using System.Linq;
using System.Windows.Input;
using ValidationTool.UI.Commands;
using ValidationTool.UI.Models.DTOs.BudgetConfig;
using ValidationTool.UI.Models.Items;
using ValidationTool.UI.Services.Config;
using ValidationTool.UI.ViewModels.General;

namespace ValidationTool.UI.ViewModels.BudgetsView_Models {
    public class BudgetsConfigViewModel : ViewModelBase {
        private readonly BudgetConfigService _budgetService;

        private BudgetConfigDto _budgetConfig;
        public BudgetConfigDto BudgetConfig {
            get => _budgetConfig;
            set => SetProperty(ref _budgetConfig, value);
        }

        private GeometryBudgetsViewModel _geometry;
        public GeometryBudgetsViewModel Geometry {
            get => _geometry;
            set => SetProperty(ref _geometry, value);
        }

        private UvBudgetsViewModel _uv;
        public UvBudgetsViewModel Uv {
            get => _uv;
            set => SetProperty(ref _uv, value);
        }

        private MaterialBudgetsViewModel _materials;
        public MaterialBudgetsViewModel Materials {
            get => _materials;
            set => SetProperty(ref _materials, value);
        }

        private TextureBudgetsViewModel _textures;
        public TextureBudgetsViewModel Textures {
            get => _textures;
            set => SetProperty(ref _textures, value);
        }

        private RiggingBudgetsViewModel _rigging;
        public RiggingBudgetsViewModel Rigging {
            get => _rigging;
            set => SetProperty(ref _rigging, value);
        }

        private AnimationBudgetsViewModel _animation;
        public AnimationBudgetsViewModel Animation {
            get => _animation;
            set => SetProperty(ref _animation, value);
        }

        private LightingBudgetsViewModel _lighting;
        public LightingBudgetsViewModel Lighting {
            get => _lighting;
            set => SetProperty(ref _lighting, value);
        }

        private CameraBudgetsViewModel _camera;
        public CameraBudgetsViewModel Camera {
            get => _camera;
            set => SetProperty(ref _camera, value);
        }

        private RenderBudgetsViewModel _render;
        public RenderBudgetsViewModel Render {
            get => _render;
            set => SetProperty(ref _render, value);
        }

        private OutputBudgetsViewModel _output;
        public OutputBudgetsViewModel Output {
            get => _output;
            set => SetProperty(ref _output, value);
        }

        private ColorManagementBudgetsViewModel _colorManagement;
        public ColorManagementBudgetsViewModel ColorManagement {
            get => _colorManagement;
            set => SetProperty(ref _colorManagement, value);
        }

        private SceneHygieneBudgetsViewModel _sceneHygiene;
        public SceneHygieneBudgetsViewModel SceneHygiene {
            get => _sceneHygiene;
            set => SetProperty(ref _sceneHygiene, value);
        }

        private ExportBudgetsViewModel _export;
        public ExportBudgetsViewModel Export {
            get => _export;
            set => SetProperty(ref _export, value);
        }

        private PerformanceBudgetsViewModel _performance;
        public PerformanceBudgetsViewModel Performance {
            get => _performance;
            set => SetProperty(ref _performance, value);
        }

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

        private string _statusMessage;
        public string StatusMessage {
            get => _statusMessage;
            set => SetProperty(ref _statusMessage, value);
        }

        public ICommand LoadCommand { get; }
        public ICommand SaveCommand { get; }

        public BudgetsConfigViewModel(BudgetConfigDto budgetConfig = null, BudgetConfigService budgetService = null) {
            _budgetService = budgetService ?? new BudgetConfigService();

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

            LoadCommand = new RelayCommand(Load);
            SaveCommand = new RelayCommand(Save);

            BudgetConfig = budgetConfig ?? _budgetService.Load();
            RebuildSectionViewModels();

            SelectedSection = Sections.FirstOrDefault();
            StatusMessage = $"Loaded: {_budgetService.FilePath}";
        }

        private void Load() {
            BudgetConfig = _budgetService.Load();
            RebuildSectionViewModels();

            if (SelectedSection == null)
                SelectedSection = Sections.FirstOrDefault();
            else
                UpdateCurrentSection();

            StatusMessage = $"Loaded: {_budgetService.FilePath}";
        }

        private void Save() {
            _budgetService.Save(BudgetConfig);
            StatusMessage = $"Saved: {_budgetService.FilePath}";
        }

        private void RebuildSectionViewModels() {
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
