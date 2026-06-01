using System.ComponentModel;
using System.Runtime.CompilerServices;
using System.Windows.Input;
using ValidationTool.UI.Models.Config;
using ValidationTool.UI.Services.Config;
using ValidationTool.UI.Commands;

namespace ValidationTool.UI.ViewModels {
    public class ConfigurationViewModel : INotifyPropertyChanged {
        private readonly ConfigService _service = new ConfigService();

        private ValidationConfigModel _config;

        public ValidationConfigModel Config {
            get => _config;
            set {
                _config = value;
                OnPropertyChanged();
            }
        }

        public ICommand LoadCommand { get; }
        public ICommand SaveCommand { get; }

        public ConfigurationViewModel() {
            LoadCommand = new RelayCommand(Load);
            SaveCommand = new RelayCommand(Save);

            Config = _service.LoadConfig(); // initial load
        }

        private void Load() {
            Config = _service.LoadConfig();
        }

        private void Save() {
            _service.SaveConfig(Config);
        }

        public event PropertyChangedEventHandler PropertyChanged;

        private void OnPropertyChanged([CallerMemberName] string name = null) {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
        }
    }
}