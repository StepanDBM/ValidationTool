using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Runtime.CompilerServices;
using System.Windows.Input;
using ValidationTool.UI.Commands;
using ValidationTool.UI.Models.Config;
using ValidationTool.UI.Services.Config;

namespace ValidationTool.UI.ViewModels {
    public class ConfigurationViewModel : INotifyPropertyChanged {
        private readonly ConfigService _configService = new ConfigService();
        private readonly NamingRulesService _namingRulesService = new NamingRulesService();

        public ValidationConfigModel _config { get; set; }

        public NamingRulesModel NamingConfig { get; set; }

        public ValidationConfigModel Config {
            get => _config;
            set {
                _config = value;
                OnPropertyChanged();
            }
        }
        public ICommand LoadCommand { get; }
        public ICommand SaveCommand { get; }
        public ICommand LoadNamingRules { get; }
        public ICommand SaveNamingRules { get; }

        public ConfigurationViewModel() {
            LoadCommand = new RelayCommand(myLoad);
            SaveCommand = new RelayCommand(mySave);
            LoadNamingRules = new RelayCommand(myLoadNamingRules);
            SaveNamingRules = new RelayCommand(mySaveNamingRules);

            Config = _configService.LoadConfig(); // initial load
            NamingConfig = _namingRulesService.LoadNamingRules(); // initial load
        }

        private void myLoad() {
            Config = _configService.LoadConfig();
        }

        private void mySave() {
            _configService.SaveConfig(Config);
        }

        private void myLoadNamingRules() {
            NamingConfig = _namingRulesService.LoadNamingRules();
        }

        private void mySaveNamingRules() {
            _namingRulesService.SaveNamingRules(NamingConfig);
        }

        public event PropertyChangedEventHandler PropertyChanged;

        private void OnPropertyChanged([CallerMemberName] string name = null) {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
        }
        public string ValidPrefixesText {
            get => string.Join(",", NamingConfig.ValidPrefixes ?? new List<string>());
            set {
                NamingConfig.ValidPrefixes =
                    new List<string>(value.Split(new[] { ',' }, StringSplitOptions.RemoveEmptyEntries));
                OnPropertyChanged();
            }
        }

        public string DefaultMayaNamesText {
            get => string.Join(",", NamingConfig.DefaultMayaNames ?? new List<string>());
            set {
                NamingConfig.DefaultMayaNames =
                    new List<string>(value.Split(new[] { ',' }, StringSplitOptions.RemoveEmptyEntries));
                OnPropertyChanged();
            }
        }
    }
}