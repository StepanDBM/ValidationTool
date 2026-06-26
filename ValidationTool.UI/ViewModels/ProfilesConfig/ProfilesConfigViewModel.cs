using System.Collections.ObjectModel;
using System.Collections.Specialized;
using System.Linq;
using System.Windows.Input;
using ValidationTool.UI.Commands;
using ValidationTool.UI.Models.DTOs.Profiles;
using ValidationTool.UI.Services.Config;
using ValidationTool.UI.ViewModels.General;

namespace ValidationTool.UI.ViewModels.ProfilesView_Models {
    public class ProfilesViewModel : ViewModelBase {
        private readonly ProfilesConfigService _profilesService;

        public ObservableCollection<ProfileItemViewModel> Profiles { get; } = new ObservableCollection<ProfileItemViewModel>();

        private ProfileItemViewModel _selectedProfile;
        public ProfileItemViewModel SelectedProfile {
            get => _selectedProfile;
            set {
                if (SetProperty(ref _selectedProfile, value)) {
                    RaisePropertyChanged(nameof(SelectedProfileDccDisplay));
                    RaisePropertyChanged(nameof(SelectedProfileCategoriesDisplay));
                    RefreshFilteredOverrides();

                    if (_selectedProfile != null) {
                        _selectedProfile.Overrides.CollectionChanged -= SelectedProfileOverrides_CollectionChanged;
                        _selectedProfile.Overrides.CollectionChanged += SelectedProfileOverrides_CollectionChanged;
                    }
                }
            }
        }

        public string SelectedProfileDccDisplay => SelectedProfile?.DccDisplay ?? "";
        public string SelectedProfileCategoriesDisplay => SelectedProfile?.EnabledCategoriesDisplay ?? "";

        public ObservableCollection<OverrideItemViewModel> FilteredOverrides { get; } = new ObservableCollection<OverrideItemViewModel>();

        public ObservableCollection<string> DomainFilters { get; } = new ObservableCollection<string> {
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

        private string _statusMessage;
        public string StatusMessage {
            get => _statusMessage;
            set => SetProperty(ref _statusMessage, value);
        }


        private string _newOverridePath;
        public string NewOverridePath {
            get => _newOverridePath;
            set => SetProperty(ref _newOverridePath, value);
        }

        private string _newOverrideValueRaw;
        public string NewOverrideValueRaw {
            get => _newOverrideValueRaw;
            set => SetProperty(ref _newOverrideValueRaw, value);
        }

        private bool _newOverrideEnabled = true;
        public bool NewOverrideEnabled {
            get => _newOverrideEnabled;
            set => SetProperty(ref _newOverrideEnabled, value);
        }



        public ICommand LoadCommand { get; }
        public ICommand SaveCommand { get; }
        public ICommand AddOverrideCommand { get; }
        public ICommand RemoveOverrideCommand { get; }
        public ICommand NewProfileCommand { get; }
        public ICommand DeleteProfileCommand { get; }

        public ProfilesViewModel() {
            _profilesService = new ProfilesConfigService();

            LoadCommand = new RelayCommand(LoadProfiles);
            SaveCommand = new RelayCommand(SaveProfiles);
            AddOverrideCommand = new RelayCommand(AddOrReplaceOverride);
            RemoveOverrideCommand = new RelayCommand<OverrideItemViewModel>(RemoveOverride);
            NewProfileCommand = new RelayCommand(NewProfile);
            DeleteProfileCommand = new RelayCommand(DeleteSelectedProfile);

            LoadProfiles();
        }

        private void LoadProfiles() {
            Profiles.Clear();

            var fileDto = _profilesService.Load();

            foreach (var dto in fileDto.profiles) {
                var vm = ProfileItemViewModel.FromDto(dto);
                vm.Overrides.CollectionChanged += SelectedProfileOverrides_CollectionChanged;
                Profiles.Add(vm);
            }

            SelectedProfile = Profiles.FirstOrDefault();
            RefreshFilteredOverrides();

            StatusMessage = $"Loaded: {_profilesService.FilePath}";
        }

        private void SaveProfiles() {
            var dto = new ProfilesFileDto {
                profiles = Profiles.Select(p => p.ToDto()).ToList()
            };

            _profilesService.Save(dto);
            StatusMessage = $"Saved: {_profilesService.FilePath}";
        }

        private void RefreshFilteredOverrides() {
            FilteredOverrides.Clear();

            if (SelectedProfile == null)
                return;

            var items = SelectedProfile.Overrides.AsEnumerable();

            if (!string.IsNullOrWhiteSpace(SelectedDomainFilter) && SelectedDomainFilter != "All")
                items = items.Where(o => o.Domain == SelectedDomainFilter);

            if (!string.IsNullOrWhiteSpace(SearchText)) {
                var search = SearchText.Trim().ToLowerInvariant();
                items = items.Where(o =>
                    (!string.IsNullOrWhiteSpace(o.Path) && o.Path.ToLowerInvariant().Contains(search)) ||
                    (!string.IsNullOrWhiteSpace(o.ValueRaw) && o.ValueRaw.ToLowerInvariant().Contains(search)));
            }

            foreach (var item in items)
                FilteredOverrides.Add(item);

            RaisePropertyChanged(nameof(SelectedProfileDccDisplay));
            RaisePropertyChanged(nameof(SelectedProfileCategoriesDisplay));
        }

        /// <summary>
        /// Adds a blank override if there is no path conflict.
        /// If the user later types a path already present, Save still works,
        /// but for first UX pass we can also choose to "replace the selected one" in future.
        /// </summary>
        private void AddOrReplaceOverride() {
            if (SelectedProfile == null)
                return;

            if (string.IsNullOrWhiteSpace(NewOverridePath)) {
                StatusMessage = "Override path cannot be empty.";
                return;
            }

            var path = NewOverridePath.Trim();
            var value = NewOverrideValueRaw?.Trim() ?? "";

            var existing = SelectedProfile.Overrides
                .FirstOrDefault(o => string.Equals(o.Path, path, System.StringComparison.OrdinalIgnoreCase));

            if (existing != null) {
                existing.ValueRaw = value;
                existing.IsEnabled = NewOverrideEnabled;

                StatusMessage = $"Updated override: {path}";
            } else {
                var item = new OverrideItemViewModel {
                    Path = path,
                    ValueRaw = value,
                    IsEnabled = NewOverrideEnabled
                };

                SelectedProfile.Overrides.Add(item);

                StatusMessage = $"Added override: {path}";
            }

            NewOverridePath = "";
            NewOverrideValueRaw = "";
            NewOverrideEnabled = true;

            RefreshFilteredOverrides();
        }

        public void AddOrReplaceOverride(string path, string valueRaw, bool enabled = true) {
            if (SelectedProfile == null || string.IsNullOrWhiteSpace(path))
                return;

            var existing = SelectedProfile.Overrides.FirstOrDefault(o => o.Path == path);
            if (existing != null) {
                existing.ValueRaw = valueRaw;
                existing.IsEnabled = enabled;
            } else {
                SelectedProfile.Overrides.Add(new OverrideItemViewModel {
                    Path = path,
                    ValueRaw = valueRaw,
                    IsEnabled = enabled
                });
            }

            RefreshFilteredOverrides();
        }

        private void RemoveOverride(OverrideItemViewModel item) {
            if (SelectedProfile == null || item == null)
                return;

            if (SelectedProfile.Overrides.Contains(item)) {
                SelectedProfile.Overrides.Remove(item);
                StatusMessage = $"Deleted override: {item.Path}";
            }

            RefreshFilteredOverrides();
        }

        private void NewProfile() {
            var profile = new ProfileItemViewModel {
                Id = "new_profile",
                Name = "New Profile",
                Description = ""
            };

            profile.Overrides.CollectionChanged += SelectedProfileOverrides_CollectionChanged;

            Profiles.Add(profile);
            SelectedProfile = profile;
            StatusMessage = "New profile created.";
        }

        private void DeleteSelectedProfile() {
            if (SelectedProfile == null)
                return;

            var toDelete = SelectedProfile;
            Profiles.Remove(toDelete);
            SelectedProfile = Profiles.FirstOrDefault();

            StatusMessage = "Profile deleted.";
        }

        private void SelectedProfileOverrides_CollectionChanged(object sender, NotifyCollectionChangedEventArgs e) {
            RefreshFilteredOverrides();
        }
    }
}