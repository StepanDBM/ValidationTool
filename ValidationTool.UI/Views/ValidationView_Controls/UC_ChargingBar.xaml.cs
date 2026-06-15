using System;
using System.Windows;
using System.Windows.Controls;
using ValidationTool.UI.ViewModels;

namespace ValidationTool.UI.Views.ValidationView_Controls {
    public partial class UC_ChargingBar : UserControl {
        public UC_ChargingBar() {
            InitializeComponent();
        }

        private ValidationViewModel VM => DataContext as ValidationViewModel;

        private void RunMaya_Click(object sender, RoutedEventArgs e) {
            VM?.RunMayaValidation();
        }

        private void RunBlender_Click(object sender, RoutedEventArgs e) {
            VM?.RunBlenderValidation();
        }

        private void LoadReport_Click(object sender, RoutedEventArgs e) {
            VM?.LoadReport();

            Console.WriteLine("This is actualy being done");
        }

        private void LoadProxy_Click(object sender, RoutedEventArgs e) {
            VM?.LoadProxy();
        }
    }
}