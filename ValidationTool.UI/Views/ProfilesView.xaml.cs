using System.Windows.Controls;
using ValidationTool.UI.ViewModels;
using ValidationTool.UI.ViewModels.ProfilesView_Models;

namespace ValidationTool.UI.Views {
    public partial class ProfilesView : UserControl {
        public ProfilesView() {
            InitializeComponent();
            DataContext = new ProfilesViewModel();
        }
    }
}