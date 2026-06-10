using System.Windows;
using System.Windows.Controls;
using ValidationTool.UI.ViewModels;
using System.Collections.ObjectModel;

namespace ValidationTool.UI.Views {
    public partial class ValidationView : UserControl {
        public ValidationView() {
            InitializeComponent();
            DataContext = new ValidationViewModel();
        }

        private void loadReportUI(object sender, RoutedEventArgs e) {
            var vm = DataContext as ValidationViewModel;
            vm.LoadReport();
        }
        private void RunMaya_Click(object sender, RoutedEventArgs e) {
            var vm = DataContext as ValidationViewModel;
            vm.RunMayaValidation();
        }

        private void RunBlender_Click(object sender, RoutedEventArgs e) {
            var vm = DataContext as ValidationViewModel;
            vm.RunBlenderValidation();
        }
    }
}