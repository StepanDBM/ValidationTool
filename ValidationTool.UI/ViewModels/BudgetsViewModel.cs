using System.ComponentModel;
using ValidationTool.UI.Models.Config;
using ValidationTool.UI.Services.Config;
using System.ComponentModel;

namespace ValidationTool.UI.ViewModels {
    public class BudgetsViewModel : INotifyPropertyChanged {
        private readonly BudgetsConfigService _service = new BudgetsConfigService();

        public event PropertyChangedEventHandler PropertyChanged;
        private BudgetsConfigModel _config;
        public BudgetsConfigModel Config {
            get => _config;
            set {
                _config = value;
                PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(nameof(Config)));
            }
        }
        public BudgetsViewModel() {
            Load();
        }

        public void Load() {
            Config = _service.Load();
        }

        public void Save() {
            _service.Save(Config);
        }
    }
}