using System;
using System.Collections.Generic;
using System.IO;
using System.Text.Json;
using ValidationTool.UI.Models;
using ValidationTool.UI.ViewModels;

namespace ValidationTool.UI.Services {
    internal class JsonReportLoader {
        public static List<IssueResult> LoadIssues(string filePath) {
            var json = File.ReadAllText(filePath);

            var options = new JsonSerializerOptions {
                PropertyNameCaseInsensitive = true
            };

            var root = JsonSerializer.Deserialize<ValidationRunDto>(json, options);

            var issues = new List<IssueResult>();

            foreach (var asset in root.Assets)
                foreach (var stage in asset.Stages)
                    foreach (var issue in stage.Issues)
                        issues.Add(issue);

            return issues;
        }

        internal static ValidationRunDto Load(string path) {
            throw new NotImplementedException();
        }
    }
}
