using System;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text.RegularExpressions;

namespace ValidationTool.UI.Services.External {
    public static class MayaRunner {
        public static void Run(string scriptPath, Action<string> onOutput) {
            var mayapyExe = FindLatestMayapyExecutable();

            if (string.IsNullOrWhiteSpace(mayapyExe) || !File.Exists(mayapyExe)) {
                throw new FileNotFoundException("Could not find a valid Maya mayapy.exe executable.");
            }

            onOutput?.Invoke("[INFO] Using MAYAPY: " + mayapyExe);

            var psi = new ProcessStartInfo {
                FileName = mayapyExe,
                Arguments = $"\"{scriptPath}\"",
                UseShellExecute = false,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                CreateNoWindow = true,
                StandardOutputEncoding = System.Text.Encoding.UTF8,
                StandardErrorEncoding = System.Text.Encoding.UTF8
            };

            using (var process = new Process { StartInfo = psi, EnableRaisingEvents = true }) {
                process.OutputDataReceived += (s, e) => {
                    if (e.Data != null)
                        onOutput?.Invoke(e.Data);
                };

                process.ErrorDataReceived += (s, e) => {
                    if (e.Data != null)
                        onOutput?.Invoke("[ERR] " + e.Data);
                };

                process.Start();
                process.BeginOutputReadLine();
                process.BeginErrorReadLine();

                process.WaitForExit();
            }
        }

        private static string FindLatestMayapyExecutable() {
            string[] candidateRoots =
            {
                @"C:\Program Files\Autodesk",
                @"C:\Program Files (x86)\Autodesk"
            };

            foreach (var root in candidateRoots) {
                if (!Directory.Exists(root))
                    continue;

                var mayaDirs = Directory.GetDirectories(root, "Maya*")
                    .Select(d => new {
                        Path = d,
                        FolderName = Path.GetFileName(d),
                        Version = ParseMayaVersion(Path.GetFileName(d))
                    })
                    .Where(x => x.Version.HasValue)
                    .OrderByDescending(x => x.Version.Value)
                    .ToList();

                foreach (var dir in mayaDirs) {
                    var exePath = Path.Combine(dir.Path, "bin", "mayapy.exe");
                    if (File.Exists(exePath))
                        return exePath;
                }
            }

            return null;
        }

        private static int? ParseMayaVersion(string folderName) {
            // Kind of like:
            // Maya2022
            // Maya2024
            // Maya2026
            var match = Regex.Match(folderName, @"Maya(\d{4})", RegexOptions.IgnoreCase);

            if (!match.Success)
                return null;

            int version;
            if (int.TryParse(match.Groups[1].Value, out version))
                return version;

            return null;
        }
    }
}