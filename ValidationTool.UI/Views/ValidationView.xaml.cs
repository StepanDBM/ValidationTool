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
            vm.LoadReport(
                @"C:\Users\StyopaDBM\source\repos\ValidationTool\ValidationTool.Client\reports\2026-06-01_06-12-01\validation_report.json"
            );
        }
    }
}