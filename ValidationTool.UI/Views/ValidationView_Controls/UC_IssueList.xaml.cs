using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;
using ValidationTool.UI.ViewModels;

namespace ValidationTool.UI.Views.ValidationView_Controls {
    public partial class UC_IssueList : UserControl {
        public UC_IssueList() {
            InitializeComponent();
        }

        private void GridViewHeader_Click(object sender, RoutedEventArgs e) {
            var vm = DataContext as ValidationViewModel;
            if (vm == null)
                return;

            DependencyObject obj = (DependencyObject)e.OriginalSource;

            while (obj != null && !(obj is GridViewColumnHeader))
                obj = VisualTreeHelper.GetParent(obj);

            var header = obj as GridViewColumnHeader;

            if (header?.Column == null)
                return;

            string sortProperty = header.Column.DisplayMemberBinding is System.Windows.Data.Binding b
                ? b.Path.Path
                : header.Column.Header.ToString();

            vm.GridViewColumnHeader_Click(sortProperty, true);
        }
    }
}