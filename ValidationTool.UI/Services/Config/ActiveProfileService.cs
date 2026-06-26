using System;
using System.IO;
using System.Text.Json;
using ValidationTool.UI.Models.DTOs.Profiles;

namespace ValidationTool.UI.Services.Config {
    public class ActiveProfileService {
        private readonly string _filePath;
        private readonly JsonSerializerOptions _jsonOptions;

        public ActiveProfileService(string filePath = null) {
            _filePath = filePath ?? Path.Combine(Paths.GEN_CONFIGS, "active_profile.json");

            _jsonOptions = new JsonSerializerOptions {
                WriteIndented = true,
                PropertyNameCaseInsensitive = true
            };
        }

        public string FilePath => _filePath;

        public void Save(ProfileDto profile) {
            EnsureDirectoryExists();

            if (profile == null) {
                File.WriteAllText(_filePath, string.Empty);
                return;
            }

            var json = JsonSerializer.Serialize(profile, _jsonOptions);
            File.WriteAllText(_filePath, json);
        }

        private void EnsureDirectoryExists() {
            var dir = Path.GetDirectoryName(_filePath);

            if (!string.IsNullOrWhiteSpace(dir))
                Directory.CreateDirectory(dir);
        }
    }
}