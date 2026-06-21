using System;
using System.IO;
using System.Text.Json;
using ValidationTool.UI.Models.DTOs.BudgetConfig;

namespace ValidationTool.UI.Services.Config {
    public class BudgetConfigService {
        private readonly string _filePath;
        private readonly JsonSerializerOptions _jsonOptions;

        public BudgetConfigService(string filePath = null) {
            _filePath = filePath ?? GetDefaultPath();

            _jsonOptions = new JsonSerializerOptions {
                WriteIndented = true,
                PropertyNameCaseInsensitive = true
            };
        }

        public string FilePath => _filePath;

        public BudgetConfigDto Load() {
            EnsureDirectoryExists();

            if (!File.Exists(_filePath)) {
                var defaults = new BudgetConfigDto();
                Save(defaults);
                return defaults;
            }

            var json = File.ReadAllText(_filePath);

            if (string.IsNullOrWhiteSpace(json)) {
                var defaults = new BudgetConfigDto();
                Save(defaults);
                return defaults;
            }

            var loaded = JsonSerializer.Deserialize<BudgetConfigDto>(json, _jsonOptions);
            return loaded ?? new BudgetConfigDto();
        }

        public void Save(BudgetConfigDto config) {
            if (config == null)
                throw new ArgumentNullException(nameof(config));

            EnsureDirectoryExists();

            var json = JsonSerializer.Serialize(config, _jsonOptions);
            File.WriteAllText(_filePath, json);
        }

        private void EnsureDirectoryExists() {
            var dir = Path.GetDirectoryName(_filePath);
            if (!string.IsNullOrWhiteSpace(dir))
                Directory.CreateDirectory(dir);
        }

        private static string GetDefaultPath() {
            var docs = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments);
            var root = Path.Combine(docs, "ValidationTool", "Config");
            return Path.Combine(root, "budgets.json");
        }
    }
}