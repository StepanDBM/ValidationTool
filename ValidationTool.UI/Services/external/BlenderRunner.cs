using System;
using System.Diagnostics;
using System.IO;
using System.Linq;

namespace ValidationTool.UI.Services.External {
    public static class BlenderRunner {
        public static void Run(string scriptPath, Action<string> onOutput) {
            var blenderExe = FindLatestBlenderExecutable();

            if (string.IsNullOrWhiteSpace(blenderExe) || !File.Exists(blenderExe)) {
                throw new FileNotFoundException("Could not find a valid Blender executable.");
            }

            var psi = new ProcessStartInfo {
                FileName = blenderExe,
                Arguments = $"-b --factory-startup -P \"{scriptPath}\"",
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

                process.WaitForExit(); // keeps IsBusy alive until Blender finishes
            }
        }

        private static string FindLatestBlenderExecutable() {
            string[] candidateRoots =
            {
                @"C:\Program Files\Blender Foundation",
                @"C:\Program Files (x86)\Blender Foundation"
            };

            foreach (var root in candidateRoots) {
                if (!Directory.Exists(root))
                    continue;

                var blenderDirs = Directory.GetDirectories(root, "Blender *")
                    .Select(d => new {
                        Path = d,
                        VersionText = Path.GetFileName(d).Replace("Blender ", "")
                    })
                    .Select(x => new {
                        x.Path,
                        Version = ParseVersionSafe(x.VersionText)
                    })
                    .Where(x => x.Version != null)
                    .OrderByDescending(x => x.Version)
                    .ToList();

                foreach (var dir in blenderDirs) {
                    var exePath = Path.Combine(dir.Path, "blender.exe");
                    if (File.Exists(exePath))
                        return exePath;
                }
            }

            return null;
        }

        private static Version ParseVersionSafe(string versionText) {
            try {
                return new Version(versionText);
            } catch {
                return null;
            }
        }
    }
}