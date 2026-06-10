using System;
using System.IO;

namespace ValidationTool.UI.Services.Config {
    public static class Paths {
        public static readonly string ROOT_DIR = Path.GetFullPath(Path.Combine(AppContext.BaseDirectory, "..", "..", ".."));

        public static readonly string CLIENT_DIR =
            Path.Combine(ROOT_DIR, "ValidationTool.Client");

        public static readonly string UI_DIR =
            Path.Combine(ROOT_DIR, "ValidationTool.UI");

        public static readonly string CONFIG_DIR =
            Path.Combine(CLIENT_DIR, "config");

        public static readonly string REPORTS_DIR =
            Path.Combine(CLIENT_DIR, "reports");
        public static readonly string RUNS_MAYA =
            Path.Combine(REPORTS_DIR, "maya_reports.json");
        public static readonly string RUNS_BLENDER =
            Path.Combine(REPORTS_DIR, "blender_reports.json");

        public static readonly string SOURCE_ARTISTS =
            Path.Combine(ROOT_DIR, "mArtists");

        public static readonly string SOURCE_MAYA =
            Path.Combine(ROOT_DIR, "Sourcefiles", "Source_Maya");

        public static readonly string SOURCE_BLENDER =
            Path.Combine(ROOT_DIR, "Sourcefiles", "Source_Blender");

        public static readonly string SOURCE_3DSMAX =
            Path.Combine(ROOT_DIR, "Sourcefiles", "Source_3DsMax");

        public static readonly string HEADLESS =
            Path.Combine(CLIENT_DIR, "ValidationTool", "misc_tools", "headless");

        public static readonly string GEN_CONFIGS =
            Path.Combine(ROOT_DIR, "configurations");
    }
}