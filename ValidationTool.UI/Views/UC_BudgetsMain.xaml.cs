using System.Windows.Controls;
using ValidationTool.UI.ViewModels.BudgetsView_Models;

namespace ValidationTool.UI.Views {

    public partial class UC_BudgetsMain : UserControl {
        public UC_BudgetsMain() {
            InitializeComponent();
            DataContext = new BudgetsConfigViewModel();
        }
    }

}
