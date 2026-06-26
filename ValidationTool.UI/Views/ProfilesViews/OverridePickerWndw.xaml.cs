using System.Windows;
using ValidationTool.UI.ViewModels.ProfilesView_Models;

namespace ValidationTool.UI.Views {
    public partial class ProfileOverridePickerWndw : Window {
        private readonly ProfileOverridePickerViewModel _vm;

        public string ResultPath { get; private set; }
        public string ResultValueRaw { get; private set; }
        public bool ResultEnabled { get; private set; }

        public ProfileOverridePickerWndw() {
            InitializeComponent();

            _vm = new ProfileOverridePickerViewModel();
            DataContext = _vm;
        }

        private void Confirm_Click(object sender, RoutedEventArgs e) {
            if (!_vm.TryConfirm())
                return;

            ResultPath = _vm.GeneratedPath;
            ResultValueRaw = _vm.FinalValueRaw;
            ResultEnabled = _vm.IsEnabled;

            DialogResult = true;
            Close();
        }

        private void Cancel_Click(object sender, RoutedEventArgs e) {
            DialogResult = false;
            Close();
        }
    }
}