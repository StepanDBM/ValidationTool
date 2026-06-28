using System;
using System.Linq;
using System.Windows;

namespace ValidationTool.UI.Services {
    public enum AppTheme {
        Dark,
        Light
    }

    public class ThemeService {
        public AppTheme CurrentTheme { get; private set; } = AppTheme.Dark;

        public void ToggleTheme() {
            ApplyTheme(CurrentTheme == AppTheme.Dark
                ? AppTheme.Light
                : AppTheme.Dark);
        }

        public void ApplyTheme(AppTheme theme) {
            string source = theme == AppTheme.Dark
                ? "Themes/Theme_dark.xaml"
                : "Themes/Theme_light.xaml";

            var dictionaries = Application.Current.Resources.MergedDictionaries;

            var oldColorDictionaries = dictionaries
                .Where(d =>
                    d.Source != null &&
                    d.Source.OriginalString.IndexOf("Theme_", StringComparison.OrdinalIgnoreCase) >= 0)
                .ToList();

            foreach (var dictionary in oldColorDictionaries)
                dictionaries.Remove(dictionary);

            dictionaries.Insert(0, new ResourceDictionary {
                Source = new Uri(source, UriKind.Relative)
            });

            CurrentTheme = theme;
        }
    }
}