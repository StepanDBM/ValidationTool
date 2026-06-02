using System.Diagnostics;
namespace ValidationTool.UI.Services.external {
    public static class BlenderRunner {
        public static void Run(string scriptPath) {
            var psi = new ProcessStartInfo {

                FileName = @"C:\Program Files\Blender Foundation\Blender 4.5\blender.exe",
                Arguments = $"-b --factory-startup -P \"{scriptPath}\"",
                UseShellExecute = false,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                CreateNoWindow = true
            };

            Process.Start(psi);
        }
    }
}