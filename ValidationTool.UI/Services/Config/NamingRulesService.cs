using System.IO;
using System.Text.Json;
using ValidationTool.UI.Models.Config;

namespace ValidationTool.UI.Services.Config {
    public class NamingRulesService {
        private static string namingPath = Path.Combine(Paths.GEN_CONFIGS, "naming_rules.json");

        public NamingRulesModel LoadNamingRules() {
            if (!File.Exists(namingPath))
                return new NamingRulesModel();

            var json = File.ReadAllText(namingPath);

            return JsonSerializer.Deserialize<NamingRulesModel>(json,
                new JsonSerializerOptions {
                    PropertyNameCaseInsensitive = true
                });
        }

        public void SaveNamingRules(NamingRulesModel config) {
            var json = JsonSerializer.Serialize(config, new JsonSerializerOptions {
                WriteIndented = true
            });

            File.WriteAllText(namingPath, json);
        }
    }
}