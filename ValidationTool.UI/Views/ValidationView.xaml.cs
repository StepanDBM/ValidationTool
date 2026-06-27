using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;
using ValidationTool.UI.ViewModels;

namespace ValidationTool.UI.Views {
    public partial class ValidationView : UserControl {
        public ValidationView() {
            InitializeComponent();
        }

        private void loadReportUI(object sender, RoutedEventArgs e) {
            var vm = DataContext as ValidationViewModel;
            vm.LoadReport();
        }
        private async void RunMaya_Click(object sender, RoutedEventArgs e) {
            var vm = DataContext as ValidationViewModel;
            await vm.RunMayaValidation();
        }


        private async void RunBlender_Click(object sender, RoutedEventArgs e) {
            var vm = DataContext as ValidationViewModel;
            await vm.RunBlenderValidation();
        }
        private void GridViewHeader_Click(object sender, RoutedEventArgs e) {
            var vm = DataContext as ValidationViewModel;
           
            DependencyObject obj = (DependencyObject)e.OriginalSource;

            // walk up visual tree until header found
            while (obj != null && !(obj is GridViewColumnHeader))
                obj = VisualTreeHelper.GetParent(obj);

            var header = obj as GridViewColumnHeader;
            if (header?.Column == null)
                return;

            var binding = header.Column.DisplayMemberBinding as System.Windows.Data.Binding;


            string sortProperty = header.Column.DisplayMemberBinding is System.Windows.Data.Binding b
                ? b.Path.Path
                : header.Column.Header.ToString();

            vm.GridViewColumnHeader_Click(sortProperty, true);
        }
    }
}