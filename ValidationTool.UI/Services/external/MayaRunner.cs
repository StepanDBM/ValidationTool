using System;
using System.Diagnostics;
namespace ValidationTool.UI.Services.external {
    public static class MayaRunner {
        public static void Run(string scriptPath, Action<string> onOutput) {
            var psi = new ProcessStartInfo {
                FileName = @"C:\Program Files\Autodesk\Maya2026\bin\mayapy.exe",
                Arguments = $"\"{scriptPath}\"",
                UseShellExecute = false,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                CreateNoWindow = true,
                StandardOutputEncoding = System.Text.Encoding.UTF8,
                StandardErrorEncoding = System.Text.Encoding.UTF8
            };

            var process = new Process { StartInfo = psi, EnableRaisingEvents = true };

            process.OutputDataReceived += (s, e) => {
                if (e.Data != null)
                    onOutput(e.Data);
            };

            process.ErrorDataReceived += (s, e) => {
                if (e.Data != null)
                    onOutput("[ERR] " + e.Data);
            };

            process.Start();
            process.BeginOutputReadLine();
            process.BeginErrorReadLine();

            process.WaitForExit();
        }
    }
}