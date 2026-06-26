using System;
using System.IO;

namespace ValidationTool.UI.Services.Config {
    public static class Paths {//mild copy from the backend python version
        private const string APP_NAME = "ValidationTool";

        // ============================================================
        // ENVIRONMENT DETECTION
        // ============================================================

        private static string FindDevRoot() {
            var dir = new DirectoryInfo(AppContext.BaseDirectory);

            while (dir != null) {
                var marker = Path.Combine(dir.FullName, ".validation_root");
                if (File.Exists(marker) || Directory.Exists(marker))
                    return dir.FullName;

                dir = dir.Parent;
            }

            return null;
        }

        private static string GetRuntimeRoot() {
            // In deployed mode, assume tool root = folder where the exe lives
            // Could have put this inside the GetToolsRoot, but might change the
            // Hierarchy at some point, so it seemed fitting and cleaner.
            return AppContext.BaseDirectory;
        }

        private static string GetToolsRoot() {
            var devRoot = FindDevRoot();
            if (!string.IsNullOrEmpty(devRoot))
                return devRoot;

            return GetRuntimeRoot();
        }

        private static string GetDocumentsRoot() {
            return Path.Combine(
                Environment.GetFolderPath(
                    Environment.SpecialFolder.MyDocuments), APP_NAME
            );
        }

        // ============================================================
        // ROOTS
        // ============================================================

        public static readonly string TOOLS_ROOT = GetToolsRoot();
        public static readonly string DATA_ROOT = GetDocumentsRoot();

        // ============================================================
        // TOOL PATHS
        // ============================================================

        public static readonly string CLIENT_DIR =
            Path.Combine(TOOLS_ROOT, "ValidationTool.Client");

        public static readonly string UI_DIR =
            Path.Combine(TOOLS_ROOT, "ValidationTool.UI");

        public static readonly string SCENESGEN_DIR =
            Path.Combine(TOOLS_ROOT, "ValidationTool.ScenesGen");

        public static readonly string CONFIG_DIR =
            Path.Combine(CLIENT_DIR, "Config");

        public static readonly string HEADLESS =
            Path.Combine(CLIENT_DIR, "ValidationTool", "misc_tools", "headless");

        public static readonly string GEN_CONFIGS =
            Path.Combine(DATA_ROOT, "Config");

        // ============================================================
        // DATA PATHS (ALWAYS IN DOCUMENTS)
        // ============================================================

        public static readonly string ARTISTS_DIR =
            Path.Combine(DATA_ROOT, "Artists");

        public static readonly string REPORTS_DIR =
            Path.Combine(DATA_ROOT, "Reports");

        public static readonly string LOGS_DIR =
            Path.Combine(DATA_ROOT, "Logs");//empty for now, but will be using it in the future for sure

        public static readonly string RUNS_MAYA =
            Path.Combine(REPORTS_DIR, "maya_reports.json");

        public static readonly string RUNS_BLENDER =
            Path.Combine(REPORTS_DIR, "blender_reports.json");

        // ============================================================
        // INIT
        // ============================================================

        static Paths() {
            Directory.CreateDirectory(DATA_ROOT);
            Directory.CreateDirectory(ARTISTS_DIR);
            Directory.CreateDirectory(REPORTS_DIR);
            Directory.CreateDirectory(LOGS_DIR);
        }
    }
}