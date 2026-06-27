using System;
using System.Collections.Generic;
using System.IO;
using System.Text.Json;
using ValidationTool.UI.Models.DTOs;
using ValidationTool.UI.Services.Config;

namespace ValidationTool.UI.Services {
    public static class JsonReportLoader {
        public static List<ValidationRunDto> Load() {
            var reports = new List<ValidationRunDto>();

            var lastRuns = LoadLastReportList();

            foreach (var dcc in lastRuns) {
                foreach (var reportPath in dcc.Runs) {
                    try {
                        var json = File.ReadAllText(Path.Combine(Paths.REPORTS_DIR, reportPath));
                        var report = JsonSerializer.Deserialize<ValidationRunDto>(
                            json,
                            new JsonSerializerOptions {
                                PropertyNameCaseInsensitive = true
                            });

                        if (report != null) {
                            reports.Add(report);
                        }
                    } catch {
                    }
                }
            }

            return reports;
        }
        public static List<LastRunsListDto> LoadLastReportList() {
            var result = new List<LastRunsListDto>();

            if (!Directory.Exists(Paths.REPORTS_DIR))
                return result;

            var reportFiles = Directory.GetFiles(Paths.REPORTS_DIR, "*_reports.json");

            foreach (string reportFile in reportFiles) {
                if (!File.Exists(reportFile))
                    continue;

                var json = File.ReadAllText(reportFile);

                if (string.IsNullOrWhiteSpace(json))
                    continue;

                try {
                    var dto = JsonSerializer.Deserialize<LastRunsListDto>(
                        json,
                        new JsonSerializerOptions {
                            PropertyNameCaseInsensitive = true
                        });

                    if (dto != null) {
                        result.Add(dto);
                    }
                } catch (Exception ex) {
                    System.Diagnostics.Debug.WriteLine(
                        $"[REPORT LOAD ERROR] {reportFile}: {ex.Message}");
                }
            }

            return result;
        }

    }
}