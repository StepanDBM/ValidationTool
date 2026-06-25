using System.Collections.ObjectModel;
using System.Linq;
using System.Windows.Input;
using ValidationTool.UI.Commands;
using ValidationTool.UI.ViewModels;
using ValidationTool.UI.ViewModels.General;

namespace ValidationTool.UI.ViewModels.ProfilesView_Models {
    public class ProfilesConfigViewModel : ViewModelBase {
        public ObservableCollection<ProfileItemViewModel> Profiles { get; } = new ObservableCollection<ProfileItemViewModel>();

        private ProfileItemViewModel _selectedProfile;
        public ProfileItemViewModel SelectedProfile {
            get => _selectedProfile;
            set {
                if (SetProperty(ref _selectedProfile, value)) {
                    RaisePropertyChanged(nameof(SelectedProfileDccDisplay));
                    RaisePropertyChanged(nameof(SelectedProfileCategoriesDisplay));
                    RefreshFilteredOverrides();
                }
            }
        }

        public string SelectedProfileDccDisplay => SelectedProfile?.DccDisplay ?? "";
        public string SelectedProfileCategoriesDisplay => SelectedProfile?.EnabledCategoriesDisplay ?? "";

        public ObservableCollection<OverrideItemViewModel> FilteredOverrides { get; } = new ObservableCollection<OverrideItemViewModel>();

        public ObservableCollection<string> DomainFilters { get; } = new ObservableCollection<string>
        {
            "All",
            "Validation",
            "Naming",
            "Geometry",
            "UV",
            "Materials",
            "Textures",
            "Rigging",
            "Animation",
            "Lighting",
            "Camera",
            "Render",
            "Output",
            "Color",
            "Scene Hygiene",
            "Export",
            "Performance"
        };

        private string _selectedDomainFilter = "All";
        public string SelectedDomainFilter {
            get => _selectedDomainFilter;
            set {
                if (SetProperty(ref _selectedDomainFilter, value))
                    RefreshFilteredOverrides();
            }
        }

        private string _searchText;
        public string SearchText {
            get => _searchText;
            set {
                if (SetProperty(ref _searchText, value))
                    RefreshFilteredOverrides();
            }
        }

        public ICommand AddOverrideCommand { get; }
        public ICommand RemoveOverrideCommand { get; }
        public ICommand NewProfileCommand { get; }
        public ICommand DeleteProfileCommand { get; }

        public ProfilesConfigViewModel() {
            AddOverrideCommand = new RelayCommand(AddOverride);
            RemoveOverrideCommand = new RelayCommand<OverrideItemViewModel>(RemoveOverride);
            NewProfileCommand = new RelayCommand(NewProfile);
            DeleteProfileCommand = new RelayCommand(DeleteSelectedProfile);

            // Temporary mock data until service is wired
            SeedMockData();
        }

        private void SeedMockData() {
            var blender = new ProfileItemViewModel {
                Id = "blender_default",
                Name = "Blender Default",
                Description = "Default validation profile for Blender headless validation."
            };
            blender.Dcc.Add("Blender");
            blender.Overrides.Add(new OverrideItemViewModel { Path = "validation.strict_mode", ValueRaw = "false", IsEnabled = true });
            blender.Overrides.Add(new OverrideItemViewModel { Path = "budgets.geometry.vertices_max", ValueRaw = "50000", IsEnabled = true });
            blender.Overrides.Add(new OverrideItemViewModel { Path = "budgets.render.aa_samples_max", ValueRaw = "8", IsEnabled = true });

            var maya = new ProfileItemViewModel {
                Id = "maya_modeling_publish",
                Name = "Maya Modeling Publish",
                Description = "Strict Maya modeling profile for publish-ready assets."
            };
            maya.Dcc.Add("Maya");
            maya.EnabledCategories.Add("Geometry");
            maya.EnabledCategories.Add("UV");
            maya.EnabledCategories.Add("Transform");
            maya.EnabledCategories.Add("Naming");

            maya.Overrides.Add(new OverrideItemViewModel { Path = "validation.strict_mode", ValueRaw = "true", IsEnabled = true });
            maya.Overrides.Add(new OverrideItemViewModel { Path = "budgets.geometry.triangles_max", ValueRaw = "90000", IsEnabled = true });
            maya.Overrides.Add(new OverrideItemViewModel { Path = "naming.valid_prefixes", ValueRaw = "[\"CH\",\"HERO\",\"WP\",\"WPN\",\"PRP\",\"PROP\",\"ENV\",\"MOD\"]", IsEnabled = true });

            var render = new ProfileItemViewModel {
                Id = "blender_render_final",
                Name = "Blender Render Final",
                Description = "Strict final render validation profile for Blender scenes."
            };
            render.Dcc.Add("Blender");
            render.Overrides.Add(new OverrideItemViewModel { Path = "budgets.render.aa_samples_max", ValueRaw = "6", IsEnabled = true });
            render.Overrides.Add(new OverrideItemViewModel { Path = "budgets.output.required_multilayer_exr", ValueRaw = "true", IsEnabled = true });

            Profiles.Add(blender);
            Profiles.Add(maya);
            Profiles.Add(render);

            SelectedProfile = Profiles.FirstOrDefault();
        }

        private void RefreshFilteredOverrides() {
            FilteredOverrides.Clear();

            if (SelectedProfile == null)
                return;

            var items = SelectedProfile.Overrides.AsEnumerable();

            if (!string.IsNullOrWhiteSpace(SelectedDomainFilter) && SelectedDomainFilter != "All") {
                items = items.Where(o => o.Domain == SelectedDomainFilter);
            }

            if (!string.IsNullOrWhiteSpace(SearchText)) {
                var search = SearchText.Trim().ToLowerInvariant();
                items = items.Where(o =>
                    (!string.IsNullOrWhiteSpace(o.Path) && o.Path.ToLowerInvariant().Contains(search)) ||
                    (!string.IsNullOrWhiteSpace(o.ValueRaw) && o.ValueRaw.ToLowerInvariant().Contains(search)));
            }

            foreach (var item in items)
                FilteredOverrides.Add(item);
        }

        private void AddOverride() {
            if (SelectedProfile == null)
                return;

            var item = new OverrideItemViewModel {
                Path = "",
                ValueRaw = "",
                IsEnabled = true
            };

            SelectedProfile.Overrides.Add(item);
            RefreshFilteredOverrides();
        }

        private void RemoveOverride(OverrideItemViewModel item) {
            if (SelectedProfile == null || item == null)
                return;

            if (SelectedProfile.Overrides.Contains(item))
                SelectedProfile.Overrides.Remove(item);

            RefreshFilteredOverrides();
        }

        private void NewProfile() {
            var profile = new ProfileItemViewModel {
                Id = "new_profile",
                Name = "New Profile",
                Description = ""
            };

            Profiles.Add(profile);
            SelectedProfile = profile;
        }

        private void DeleteSelectedProfile() {
            if (SelectedProfile == null)
                return;

            var toDelete = SelectedProfile;
            Profiles.Remove(toDelete);
            SelectedProfile = Profiles.FirstOrDefault();
        }
    }
}