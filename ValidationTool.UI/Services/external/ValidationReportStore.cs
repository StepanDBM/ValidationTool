using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Threading.Tasks;
using System.Windows;
using ValidationTool.UI.Models.DTOs;

namespace ValidationTool.UI.Services.Reports {
    public class ValidationReportStore : INotifyPropertyChanged {
        public event PropertyChangedEventHandler PropertyChanged;

        private IReadOnlyList<ValidationRunDto> _runs = new List<ValidationRunDto>();
        public IReadOnlyList<ValidationRunDto> Runs {
            get => _runs;
            private set {
                _runs = value ?? new List<ValidationRunDto>();
                PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(nameof(Runs)));
                PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(nameof(HasLoaded)));
            }
        }

        private bool _isLoading;
        public bool IsLoading {
            get => _isLoading;
            private set {
                _isLoading = value;
                PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(nameof(IsLoading)));
            }
        }

        private DateTime? _lastLoadedAt;
        public DateTime? LastLoadedAt {
            get => _lastLoadedAt;
            private set {
                _lastLoadedAt = value;
                PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(nameof(LastLoadedAt)));
            }
        }

        public bool HasLoaded => Runs.Count > 0;

        public async Task<IReadOnlyList<ValidationRunDto>> LoadAsync(bool forceReload = false) {
            if (IsLoading)
                return Runs;

            if (!forceReload && HasLoaded)
                return Runs;

            IsLoading = true;

            try {
                var loaded = await Task.Run(() => {
                    return JsonReportLoader.Load();
                });

                await Application.Current.Dispatcher.InvokeAsync(() => {
                    Runs = loaded;
                    LastLoadedAt = DateTime.Now;
                });

                return Runs;
            } finally {
                IsLoading = false;
            }
        }

        public void Clear() {
            Runs = new List<ValidationRunDto>();
            LastLoadedAt = null;
        }
    }
}