using System.Windows;
using ValidationTool.UI.ViewModels;

namespace ValidationTool.UI {
    public partial class MainWindow : Window {
        public MainWindow() {
            InitializeComponent();
            DataContext = new MainViewModel();
        }
        private void Run_Click(object sender, RoutedEventArgs e) {
            var vm = (MainViewModel)DataContext;
            vm.LoadReport(@"C:\Users\StyopaDBM\source\repos\ValidationTool\ValidationTool.Client\reports\2026-06-01_06-12-01\validation_report.json");
        }
    }
}