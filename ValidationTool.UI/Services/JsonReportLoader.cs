using System.IO;
using System.Text.Json;
using ValidationTool.UI.Models.DTOs;

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
        public static string LoadLastRun() {
            return @"C:\\Users\\StyopaDBM\\source\\repos\\ValidationTool\\ValidationTool.Client\\reports\\Blender_runID_e5e18491-2534-4fca-a7c3-cf1f72b0df85\\validation_report.json";
        }
    }
}