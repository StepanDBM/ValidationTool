using System;
using System.Diagnostics;
using System.IO;

namespace ValidationTool.UI.Services.External {
    public static class ArtistsDataSetCreator {
        public static void Run(Action<string> onOutput) {
            var baseDir = AppDomain.CurrentDomain.BaseDirectory;

            // Navigate to solution root
            var solutionRoot = Path.GetFullPath(Path.Combine(baseDir, @"..\..\.."));

            // Build path to .bat
            var batPath = Path.Combine(
                solutionRoot,
                "ValidationTool.ScenesGen",
                "run_generator.bat"
            );

            var psi = new ProcessStartInfo {
                FileName = "cmd.exe",
                Arguments = $"/C \"{batPath}\"",
                WorkingDirectory = Path.GetDirectoryName(batPath),
                UseShellExecute = false,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                CreateNoWindow = true,
                StandardOutputEncoding = System.Text.Encoding.UTF8,
                StandardErrorEncoding = System.Text.Encoding.UTF8
            };

            using (var process = new Process { StartInfo = psi }) {
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
    }
}