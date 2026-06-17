using System;
using System.Collections.Specialized;
using System.Windows;
using System.Windows.Controls;
using ValidationTool.UI.ViewModels;

namespace ValidationTool.UI.Views.ValidationView_Controls {
    public partial class UC_ChargingBar : UserControl {
        public UC_ChargingBar() {
            InitializeComponent();

            Loaded += (s, e) => { // same as Loaded += OnLoaded
                if (DataContext is ValidationViewModel vm) {
                    vm.LogLines.CollectionChanged += LogLines_CollectionChanged;
                }
            };

        }

        private void LogLines_CollectionChanged(object sender, NotifyCollectionChangedEventArgs e) {
            if (LogList.Items.Count > 0) {
                var lastItem = LogList.Items[LogList.Items.Count - 1];

                Dispatcher.InvokeAsync(() =>
                {
                    LogList.ScrollIntoView(lastItem);
                });
            }
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
        }

        private void LoadProxy_Click(object sender, RoutedEventArgs e) {
            VM?.LoadProxy();
        }
    }
}