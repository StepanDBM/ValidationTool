using System;
using System.Globalization;
using System.Windows.Data;
using System.Windows.Media;

namespace ValidationTool.UI.Converters {
    public class SeverityToBrushConverter : IValueConverter {
        public object Convert(
            object value,
            Type targetType,
            object parameter,
            CultureInfo culture) {

            var severity = value as string;

            switch (severity) {
                case "INFO":
                    return (Brush)System.Windows.Application.Current.FindResource("BrushInfo");

                case "WARNING":
                    return (Brush)System.Windows.Application.Current.FindResource("BrushWarning");

                case "ERROR":
                    return (Brush)System.Windows.Application.Current.FindResource("BrushError");

                case "HARD_ERROR":
                    return Brushes.DarkRed;

                default:
                    return (Brush)System.Windows.Application.Current.FindResource("BrushText");
            }
        }

        public object ConvertBack(
            object value,
            Type targetType,
            object parameter,
            CultureInfo culture) {

            throw new NotImplementedException();
        }
    }
}