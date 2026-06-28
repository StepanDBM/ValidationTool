using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using ValidationTool.UI.Services;

namespace ValidationTool.UI.Views {
    public partial class UC_TopBar : UserControl {
        private readonly ThemeService _themeService = new ThemeService();

        public static readonly DependencyProperty TitleTextProperty =
            DependencyProperty.Register(
                nameof(TitleText),
                typeof(string),
                typeof(UC_TopBar),
                new PropertyMetadata("ValidationTool"));

        public string TitleText {
            get => (string)GetValue(TitleTextProperty);
            set => SetValue(TitleTextProperty, value);
        }

        public UC_TopBar() {
            InitializeComponent();
        }

        private void TitleBar_MouseDown(object sender, MouseButtonEventArgs e) {
            var window = Window.GetWindow(this);

            if (window == null)
                return;

            if (e.ClickCount == 2 && e.ChangedButton == MouseButton.Left) {
                ToggleWindowMaximize(window);
                return;
            }

            if (e.LeftButton == MouseButtonState.Pressed) {
                window.DragMove();
            }
        }

        private void ToggleTheme_Click(object sender, RoutedEventArgs e) {
            _themeService.ToggleTheme();
        }

        private void Minimize_Click(object sender, RoutedEventArgs e) {
            var window = Window.GetWindow(this);

            if (window != null)
                window.WindowState = WindowState.Minimized;
        }

        private void Maximize_Click(object sender, RoutedEventArgs e) {
            var window = Window.GetWindow(this);

            if (window != null)
                ToggleWindowMaximize(window);
        }

        private void Close_Click(object sender, RoutedEventArgs e) {
            var window = Window.GetWindow(this);

            if (window != null)
                window.Close();
        }

        private static void ToggleWindowMaximize(Window window) {
            window.WindowState = window.WindowState == WindowState.Maximized
                ? WindowState.Normal
                : WindowState.Maximized;
        }
    }
}