using System.IO;

namespace ValidationTool.UI.Services.Config {
    public static class Paths {
        public static readonly string ROOT_PATH = //To be changed in case of opening in another machine
            @"C:\Users\StyopaDBM\source\repos\ValidationTool";

        public static readonly string CLIENT_PATH =
            Path.Combine(ROOT_PATH, "ValidationTool.Client");

        public static readonly string UI_PATH =
            Path.Combine(ROOT_PATH, "ValidationTool.UI");

        public static readonly string CONFIG_DIR =
            Path.Combine(CLIENT_PATH, "config");

        public static readonly string REPORTS_DIR =
            Path.Combine(CLIENT_PATH, "reports");

        public static readonly string SOURCE_MAYA =
            Path.Combine(ROOT_PATH, "Sourcefiles", "Source_Maya");

        public static readonly string SOURCE_BLENDER =
            Path.Combine(ROOT_PATH, "Sourcefiles", "Source_Blender");

        public static readonly string SOURCE_3DSMAX =
            Path.Combine(ROOT_PATH, "Sourcefiles", "Source_3DsMax");

        public static readonly string HEADLESS =
            Path.Combine(CLIENT_PATH, "ValidationTool", "misc_tools", "headless");
    }
}