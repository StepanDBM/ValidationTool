using System.IO;
using System.Text.Json;
using ValidationTool.UI.Models.Config;

namespace ValidationTool.UI.Services.Config {
    public class ConfigService {
        private static string ConfigPath = Path.Combine(Paths.GEN_CONFIGS, "validation_config.json");

        public ValidationConfigModel LoadConfig() {
            if (!File.Exists(ConfigPath))
                return new ValidationConfigModel();

            var json = File.ReadAllText(ConfigPath);

            return JsonSerializer.Deserialize<ValidationConfigModel>(json,
                new JsonSerializerOptions {
                    PropertyNameCaseInsensitive = true
                });
        }

        public void SaveConfig(ValidationConfigModel config) {
            var json = JsonSerializer.Serialize(config, new JsonSerializerOptions {
                WriteIndented = true
            });

            File.WriteAllText(ConfigPath, json);
        }
    }
}