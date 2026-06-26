using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Linq;
using ValidationTool.UI.Models.DTOs.Profiles;
using ValidationTool.UI.ViewModels.General;

namespace ValidationTool.UI.ViewModels.ProfilesView_Models {
    public class ProfileItemViewModel : ViewModelBase {
        private string _id;
        public string Id {
            get => _id;
            set => SetProperty(ref _id, value);
        }

        private string _name;
        public string Name {
            get => _name;
            set => SetProperty(ref _name, value);
        }

        private string _description;
        public string Description {
            get => _description;
            set => SetProperty(ref _description, value);
        }

        public ObservableCollection<string> Dcc { get; } = new ObservableCollection<string>();
        public ObservableCollection<string> EnabledCategories { get; } = new ObservableCollection<string>();
        public ObservableCollection<OverrideItemViewModel> Overrides { get; } = new ObservableCollection<OverrideItemViewModel>();

        public string DccDisplay => string.Join(", ", Dcc);
        public string EnabledCategoriesDisplay => string.Join(", ", EnabledCategories);
        public int EnabledOverrideCount => Overrides.Count(o => o.IsEnabled);

        public string DccRaw {
            get => string.Join(", ", Dcc);
            set {
                Dcc.Clear();

                if (!string.IsNullOrWhiteSpace(value)) {
                    var parts = value
                        .Split(',')
                        .Select(x => x.Trim())
                        .Where(x => !string.IsNullOrWhiteSpace(x));

                    foreach (var part in parts)
                        Dcc.Add(part);
                }

                RaisePropertyChanged(nameof(DccRaw));
                RaisePropertyChanged(nameof(DccDisplay));
            }
        }

        public string EnabledCategoriesRaw {
            get => string.Join(", ", EnabledCategories);
            set {
                EnabledCategories.Clear();

                if (!string.IsNullOrWhiteSpace(value)) {
                    var parts = value
                        .Split(',')
                        .Select(x => x.Trim())
                        .Where(x => !string.IsNullOrWhiteSpace(x));

                    foreach (var part in parts)
                        EnabledCategories.Add(part);
                }

                RaisePropertyChanged(nameof(EnabledCategoriesRaw));
                RaisePropertyChanged(nameof(EnabledCategoriesDisplay));
            }
        }

        public ProfileItemViewModel() {
            Dcc.CollectionChanged += (_, __) => {
                RaisePropertyChanged(nameof(DccRaw));
                RaisePropertyChanged(nameof(DccDisplay));
            };

            EnabledCategories.CollectionChanged += (_, __) => {
                RaisePropertyChanged(nameof(EnabledCategoriesRaw));
                RaisePropertyChanged(nameof(EnabledCategoriesDisplay));
            };

            Overrides.CollectionChanged += (_, e) => {
                if (e.NewItems != null) {
                    foreach (OverrideItemViewModel item in e.NewItems)
                        item.PropertyChanged += Override_PropertyChanged;
                }

                if (e.OldItems != null) {
                    foreach (OverrideItemViewModel item in e.OldItems)
                        item.PropertyChanged -= Override_PropertyChanged;
                }

                RaisePropertyChanged(nameof(EnabledOverrideCount));
            };
        }

        private void Override_PropertyChanged(object sender, PropertyChangedEventArgs e) {
            if (e.PropertyName == nameof(OverrideItemViewModel.IsEnabled))
                RaisePropertyChanged(nameof(EnabledOverrideCount));
        }

        public static ProfileItemViewModel FromDto(ProfileDto dto) {
            var vm = new ProfileItemViewModel {
                Id = dto?.id ?? "",
                Name = dto?.name ?? "",
                Description = dto?.description ?? ""
            };

            if (dto?.dcc != null) {
                foreach (var d in dto.dcc)
                    vm.Dcc.Add(d);
            }

            if (dto?.enabled_categories != null) {
                foreach (var c in dto.enabled_categories)
                    vm.EnabledCategories.Add(c);
            }

            if (dto?.overrides != null) {
                foreach (var ov in dto.overrides)
                    vm.Overrides.Add(OverrideItemViewModel.FromDto(ov));
            }

            return vm;
        }

        public ProfileDto ToDto() {
            return new ProfileDto {
                id = Id,
                name = Name,
                description = Description,
                dcc = Dcc.ToList(),
                enabled_categories = EnabledCategories.ToList(),
                overrides = Overrides.Select(o => o.ToDto()).ToList()
            };
        }
    }
}