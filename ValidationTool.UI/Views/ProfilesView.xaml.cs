using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Data;
using ValidationTool.UI.ViewModels.ProfilesView_Models;

namespace ValidationTool.UI.Views {
    public partial class ProfilesView : UserControl {
        public ProfilesView() {
            InitializeComponent();
            DataContext = new ProfilesViewModel();
        }

        private void CommitTextBoxOnEnter(object sender, KeyEventArgs e) {
            if (e.Key != Key.Enter)
                return;

            if (sender is TextBox textBox) {
                var binding = textBox.GetBindingExpression(TextBox.TextProperty);
                binding?.UpdateSource();

                // Optional: remove focus so it behaves like a "commit"
                Keyboard.ClearFocus();
            }

            e.Handled = true;
        }
    }
}