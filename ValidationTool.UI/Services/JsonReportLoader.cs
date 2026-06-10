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
            return @"C:\Users\StyopaDBM\source\repos\ValidationTool\ValidationTool.Client\reports\Maya_runID_ed1c1c71-504e-433f-9aa9-eefd6d2a734e\validation_report.json";
        }
    }
}