using System.IO;
using System.Text.Json;
using ValidationTool.UI.Models.Dto;

namespace ValidationTool.UI.Services {
    public static class JsonReportLoader {
        public static ValidationRunDto Load(string path) {
            var json = File.ReadAllText(path);

            return JsonSerializer.Deserialize<ValidationRunDto>(
                json,
                new JsonSerializerOptions {
                    PropertyNameCaseInsensitive = true
                });
        }
    }
}