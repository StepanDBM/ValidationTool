using System.Windows;
using System.Windows.Input;
using ValidationTool.UI.Models.DTOs;
using ValidationTool.UI.Models.DTOs.SceneSetup;
using ValidationTool.UI.ViewModels.SceneSetupView_Models;

namespace ValidationTool.UI.Views {
    public partial class SceneSetupWndw : Window {
        public SceneSetupWndw(SceneSetupDto sceneSetup) {
            InitializeComponent();
            DataContext = new SceneSetupWndwViewModel(sceneSetup);
        }

        private void TitleBar_MouseDown(object sender, MouseButtonEventArgs e) {
            if (e.LeftButton == MouseButtonState.Pressed) {
                DragMove();
            }
        }

        private void Close_Click(object sender, RoutedEventArgs e) {
            Close();
        }

        private void Minimize_Click(object sender, RoutedEventArgs e) {
            WindowState = WindowState.Minimized;
        }

        private void Maximize_Click(object sender, RoutedEventArgs e) {
            WindowState = WindowState == WindowState.Maximized
                ? WindowState.Normal
                : WindowState.Maximized;
        }
    }
}