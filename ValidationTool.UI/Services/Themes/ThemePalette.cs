using System.Windows;
using System.Windows.Media;

namespace ValidationTool.UI.Services.Themes {
    public class ThemePalette : DependencyObject {
        public static readonly DependencyProperty ColorBgMainProperty =
            RegisterColor(nameof(ColorBgMain));

        public static readonly DependencyProperty ColorBgPanelProperty =
            RegisterColor(nameof(ColorBgPanel));

        public static readonly DependencyProperty ColorBgRowAltProperty =
            RegisterColor(nameof(ColorBgRowAlt));

        public static readonly DependencyProperty ColorBgElementProperty =
            RegisterColor(nameof(ColorBgElement));

        public static readonly DependencyProperty ColorTextProperty =
            RegisterColor(nameof(ColorText));

        public static readonly DependencyProperty ColorTextMutedProperty =
            RegisterColor(nameof(ColorTextMuted));

        public static readonly DependencyProperty ColorTextDisabledProperty =
            RegisterColor(nameof(ColorTextDisabled));

        public static readonly DependencyProperty ColorTextOnAccentProperty =
            RegisterColor(nameof(ColorTextOnAccent));

        public static readonly DependencyProperty ColorBorderProperty =
            RegisterColor(nameof(ColorBorder));

        public static readonly DependencyProperty ColorHoverProperty =
            RegisterColor(nameof(ColorHover));

        public static readonly DependencyProperty ColorAccentProperty =
            RegisterColor(nameof(ColorAccent));

        public static readonly DependencyProperty ColorErrorProperty =
            RegisterColor(nameof(ColorError));

        public static readonly DependencyProperty ColorWarningProperty =
            RegisterColor(nameof(ColorWarning));

        public static readonly DependencyProperty ColorInfoProperty =
            RegisterColor(nameof(ColorInfo));

        public static readonly DependencyProperty ColorTransparentProperty =
            RegisterColor(nameof(ColorTransparent));

        public Color ColorBgMain {
            get => (Color)GetValue(ColorBgMainProperty);
            set => SetValue(ColorBgMainProperty, value);
        }

        public Color ColorBgPanel {
            get => (Color)GetValue(ColorBgPanelProperty);
            set => SetValue(ColorBgPanelProperty, value);
        }

        public Color ColorBgRowAlt {
            get => (Color)GetValue(ColorBgRowAltProperty);
            set => SetValue(ColorBgRowAltProperty, value);
        }

        public Color ColorBgElement {
            get => (Color)GetValue(ColorBgElementProperty);
            set => SetValue(ColorBgElementProperty, value);
        }

        public Color ColorText {
            get => (Color)GetValue(ColorTextProperty);
            set => SetValue(ColorTextProperty, value);
        }

        public Color ColorTextMuted {
            get => (Color)GetValue(ColorTextMutedProperty);
            set => SetValue(ColorTextMutedProperty, value);
        }

        public Color ColorTextDisabled {
            get => (Color)GetValue(ColorTextDisabledProperty);
            set => SetValue(ColorTextDisabledProperty, value);
        }

        public Color ColorTextOnAccent {
            get => (Color)GetValue(ColorTextOnAccentProperty);
            set => SetValue(ColorTextOnAccentProperty, value);
        }

        public Color ColorBorder {
            get => (Color)GetValue(ColorBorderProperty);
            set => SetValue(ColorBorderProperty, value);
        }

        public Color ColorHover {
            get => (Color)GetValue(ColorHoverProperty);
            set => SetValue(ColorHoverProperty, value);
        }

        public Color ColorAccent {
            get => (Color)GetValue(ColorAccentProperty);
            set => SetValue(ColorAccentProperty, value);
        }

        public Color ColorError {
            get => (Color)GetValue(ColorErrorProperty);
            set => SetValue(ColorErrorProperty, value);
        }

        public Color ColorWarning {
            get => (Color)GetValue(ColorWarningProperty);
            set => SetValue(ColorWarningProperty, value);
        }

        public Color ColorInfo {
            get => (Color)GetValue(ColorInfoProperty);
            set => SetValue(ColorInfoProperty, value);
        }

        public Color ColorTransparent {
            get => (Color)GetValue(ColorTransparentProperty);
            set => SetValue(ColorTransparentProperty, value);
        }

        private static DependencyProperty RegisterColor(string name) {
            return DependencyProperty.Register(
                name,
                typeof(Color),
                typeof(ThemePalette),
                new PropertyMetadata(Colors.Transparent)
            );
        }
    }
}