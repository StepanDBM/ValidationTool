using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.Collections.ObjectModel;
using System.Linq;
using System.Security.Authentication;
using ValidationTool.UI.Services;
using ValidationTool.UI.Services.Config;
using ValidationTool.UI.ViewModels;
using ValidationTool.UI.Models.Config;


namespace ValidationTool.UI.Views {
    public partial class ConfigurationView : UserControl {
        private ConfigurationViewModel _vm;
        public ConfigurationView() {
            InitializeComponent();
            _vm = new ConfigurationViewModel();
            DataContext = _vm;

        }
    }
}