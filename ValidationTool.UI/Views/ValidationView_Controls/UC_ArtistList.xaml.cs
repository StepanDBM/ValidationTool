using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace ValidationTool.UI.Views.ValidationView_Controls {
    /// <summary>
    /// Lógica de interacción para US_ArtistList.xaml
    /// </summary>
    public partial class UC_ArtistList : UserControl {
        public UC_ArtistList() {
            InitializeComponent();
            this.DataContext = this;
        }
    }
}
