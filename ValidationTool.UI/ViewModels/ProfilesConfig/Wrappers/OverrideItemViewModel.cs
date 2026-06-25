using System.Text.Json;
using ValidationTool.UI.Models.DTOs.Profiles;
using ValidationTool.UI.ViewModels.General;

namespace ValidationTool.UI.ViewModels.ProfilesView_Models {
    public class OverrideItemViewModel : ViewModelBase {
        private string _path;
        public string Path {
            get => _path;
            set {
                if (SetProperty(ref _path, value))
                    RaisePropertyChanged(nameof(Domain));
            }
        }

        private string _valueRaw;
        public string ValueRaw {
            get => _valueRaw;
            set => SetProperty(ref _valueRaw, value);
        }

        private bool _isEnabled;
        public bool IsEnabled {
            get => _isEnabled;
            set => SetProperty(ref _isEnabled, value);
        }

        public string Domain {
            get {
                if (string.IsNullOrWhiteSpace(Path))
                    return "Unknown";

                if (Path.StartsWith("validation."))
                    return "Validation";

                if (Path.StartsWith("naming."))
                    return "Naming";

                if (Path.StartsWith("budgets.geometry."))
                    return "Geometry";

                if (Path.StartsWith("budgets.uv."))
                    return "UV";

                if (Path.StartsWith("budgets.materials."))
                    return "Materials";

                if (Path.StartsWith("budgets.textures."))
                    return "Textures";

                if (Path.StartsWith("budgets.rigging."))
                    return "Rigging";

                if (Path.StartsWith("budgets.animation."))
                    return "Animation";

                if (Path.StartsWith("budgets.lighting."))
                    return "Lighting";

                if (Path.StartsWith("budgets.camera."))
                    return "Camera";

                if (Path.StartsWith("budgets.render."))
                    return "Render";

                if (Path.StartsWith("budgets.output."))
                    return "Output";

                if (Path.StartsWith("budgets.color_management."))
                    return "Color";

                if (Path.StartsWith("budgets.scene_hygiene."))
                    return "Scene Hygiene";

                if (Path.StartsWith("budgets.export."))
                    return "Export";

                if (Path.StartsWith("budgets.performance."))
                    return "Performance";

                if (Path.StartsWith("budgets."))
                    return "Budgets";

                return "Other";
            }
        }

        public static OverrideItemViewModel FromDto(ProfileOverrideDto dto) {
            return new OverrideItemViewModel {
                Path = dto?.path ?? "",
                ValueRaw = JsonElementToString(dto?.value),
                IsEnabled = dto?.enabled ?? true
            };
        }

        public ProfileOverrideDto ToDto() {
            return new ProfileOverrideDto {
                path = Path,
                enabled = IsEnabled,
                value = ParseValueToJsonElement(ValueRaw)
            };
        }

        private static string JsonElementToString(JsonElement? element) {
            if (element == null)
                return "";

            var e = element.Value;

            switch (e.ValueKind) {
                case JsonValueKind.String:
                    return e.GetString();

                case JsonValueKind.Number:
                case JsonValueKind.True:
                case JsonValueKind.False:
                    return e.ToString();

                case JsonValueKind.Array:
                case JsonValueKind.Object:
                    return e.GetRawText();

                case JsonValueKind.Null:
                case JsonValueKind.Undefined:
                default:
                    return "";
            }
        }

        private static JsonElement ParseValueToJsonElement(string raw) {
            if (string.IsNullOrWhiteSpace(raw))
                return JsonDocument.Parse("\"\"").RootElement.Clone();

            try {
                // Try parse as raw JSON first:
                // true / false / 42 / 1.2 / ["A"] / {"x":1}
                return JsonDocument.Parse(raw).RootElement.Clone();
            } catch {
                // Fallback: treat as plain string
                string safe = JsonSerializer.Serialize(raw);
                return JsonDocument.Parse(safe).RootElement.Clone();
            }
        }
    }
}