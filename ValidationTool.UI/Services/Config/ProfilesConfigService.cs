using System;
using System.IO;
using System.Text.Json;
using ValidationTool.UI.Models.DTOs.Profiles;

namespace ValidationTool.UI.Services.Config {
    public class ProfilesConfigService {
        private readonly string _filePath;
        private readonly JsonSerializerOptions _jsonOptions;

        public ProfilesConfigService(string filePath = null) {
            _filePath = filePath ?? Path.Combine(Paths.GEN_CONFIGS, "profiles.json");

            _jsonOptions = new JsonSerializerOptions {
                WriteIndented = true,
                PropertyNameCaseInsensitive = true
            };
        }

        public string FilePath => _filePath;

        public ProfilesFileDto Load() {
            EnsureDirectoryExists();

            if (!File.Exists(_filePath)) {
                var defaults = new ProfilesFileDto();
                Save(defaults);
                return defaults;
            }

            var json = File.ReadAllText(_filePath);

            if (string.IsNullOrWhiteSpace(json)) {
                var defaults = new ProfilesFileDto();
                Save(defaults);
                return defaults;
            }

            var loaded = JsonSerializer.Deserialize<ProfilesFileDto>(json, _jsonOptions);
            return loaded ?? new ProfilesFileDto();
        }

        public void Save(ProfilesFileDto fileDto) {
            if (fileDto == null)
                throw new ArgumentNullException(nameof(fileDto));

            EnsureDirectoryExists();

            var json = JsonSerializer.Serialize(fileDto, _jsonOptions);
            File.WriteAllText(_filePath, json);
        }

        private void EnsureDirectoryExists() {
            var dir = Path.GetDirectoryName(_filePath);
            if (!string.IsNullOrWhiteSpace(dir))
                Directory.CreateDirectory(dir);
        }
    }
}