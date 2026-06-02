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
                @"C:\Users\StyopaDBM\source\repos\ValidationTool\ValidationTool.Client\reports\Maya_runID_23814949-8426-4de2-8a12-20821dcae982\validation_report.json"
            );
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