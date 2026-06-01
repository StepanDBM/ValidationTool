using System.Windows;
using ValidationTool.UI.ViewModels;

namespace ValidationTool.UI {
    public partial class MainWindow : Window {
        public MainWindow() {
            InitializeComponent();
            DataContext = new MainViewModel();
        }
    }
}