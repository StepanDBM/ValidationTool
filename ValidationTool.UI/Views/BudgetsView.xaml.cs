using System.Windows;
using System.Windows.Controls;
using ValidationTool.UI.ViewModels;

namespace ValidationTool.UI.Views {
    public partial class BudgetsView : UserControl {
        private BudgetsViewModel _vm;

        public BudgetsView() {
            InitializeComponent();
            _vm = new BudgetsViewModel();
            DataContext = _vm;
        }

        private void Load_Click(object sender, RoutedEventArgs e) {
            _vm.Load();
        }
        private void Save_Click(object sender, RoutedEventArgs e) {
            _vm.Save();
        }
    }
}