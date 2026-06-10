using System.Collections.Generic;
using System.IO;
using System.Text.Json;
using System.Windows.Documents;
using ValidationTool.UI.Models.DTOs;
using ValidationTool.UI.Services.Config;

namespace ValidationTool.UI.Services {
    public static class JsonReportLoader {
        public static List<ValidationRunDto> Load() {
            var reports = new List<ValidationRunDto>();

            var lastRuns = LoadLastReportList();

            foreach (var dcc in lastRuns) {
                foreach (var reportPath in dcc.Runs) {
                    var json = File.ReadAllText(reportPath);

                    var report = JsonSerializer.Deserialize<ValidationRunDto>(
                        json,
                        new JsonSerializerOptions {
                            PropertyNameCaseInsensitive = true
                        });

                    if (report != null) {
                        reports.Add(report);
                    }
                }
            }

            return reports;
        }
        public static List<LastRunsListDto> LoadLastReportList() {
            var result = new List<LastRunsListDto>();

            var reportFiles = Directory.GetFiles(Paths.REPORTS_DIR, "*_reports.json");

            foreach (string reportFile in reportFiles) {
                var json = File.ReadAllText(reportFile);

                var dto = JsonSerializer.Deserialize<LastRunsListDto>(
                    json,
                    new JsonSerializerOptions {
                        PropertyNameCaseInsensitive = true
                    });

                if (dto != null) {
                    result.Add(dto);
                }
            }

            return result;
        }
    }
}