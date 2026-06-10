using System.Diagnostics;
namespace ValidationTool.UI.Services.external {
    public static class MayaRunner {
        public static void Run(string scriptPath) {
            var psi = new ProcessStartInfo {
                FileName = @"C:\Program Files\Autodesk\Maya2026\bin\mayapy.exe",
                Arguments = $"\"{scriptPath}\"",
                UseShellExecute = false,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                CreateNoWindow = true
            };

            Process.Start(psi);
        }
    }
}