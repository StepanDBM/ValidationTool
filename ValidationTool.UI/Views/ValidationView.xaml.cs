using System.Windows;
using System.Windows.Controls;
using ValidationTool.UI.ViewModels;

namespace ValidationTool.UI.Views {
    public partial class ValidationView : UserControl {
        public ValidationView() {
            InitializeComponent();
        }

        private void loadReportUI(object sender, RoutedEventArgs e) {
            var vm = (MainViewModel)DataContext;
            vm.LoadReport();
        }
        private void RunMaya_Click(object sender, RoutedEventArgs e) {
            var vm = (MainViewModel)DataContext;
            vm.RunMayaValidation();
        }

        private void RunBlender_Click(object sender, RoutedEventArgs e) {
            var vm = (MainViewModel)DataContext;
            vm.RunBlenderValidation();
        }
    }
}