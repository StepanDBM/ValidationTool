using System.Collections.ObjectModel;
using System.Globalization;
using System.Linq;
using System.Text.Json;
using System.Text.RegularExpressions;
using ValidationTool.UI.ViewModels.General;

namespace ValidationTool.UI.ViewModels.ProfilesView_Models {
    public class ProfileOverridePickerViewModel : ViewModelBase {
        public ObservableCollection<OverridePickerOption> RootOptions { get; } =
            new ObservableCollection<OverridePickerOption>();

        public ObservableCollection<OverridePickerOption> SectionOptions { get; } =
            new ObservableCollection<OverridePickerOption>();

        public ObservableCollection<OverridePickerOption> AttributeOptions { get; } =
            new ObservableCollection<OverridePickerOption>();

        public ObservableCollection<string> BooleanValues { get; } =
            new ObservableCollection<string> { "true", "false" };

        private OverridePickerOption _selectedRoot;
        public OverridePickerOption SelectedRoot {
            get => _selectedRoot;
            set {
                if (SetProperty(ref _selectedRoot, value))
                    RebuildSections();
            }
        }

        private OverridePickerOption _selectedSection;
        public OverridePickerOption SelectedSection {
            get => _selectedSection;
            set {
                if (SetProperty(ref _selectedSection, value))
                    RebuildAttributes();
            }
        }

        private OverridePickerOption _selectedAttribute;
        public OverridePickerOption SelectedAttribute {
            get => _selectedAttribute;
            set {
                if (SetProperty(ref _selectedAttribute, value))
                    ApplySelectedAttributeDefaults();
            }
        }

        private string _valueRaw;
        public string ValueRaw {
            get => _valueRaw;
            set {
                if (SetProperty(ref _valueRaw, value))
                    RaisePropertyChanged(nameof(FinalValueRaw));
            }
        }

        private string _boolValueRaw = "true";
        public string BoolValueRaw {
            get => _boolValueRaw;
            set {
                if (SetProperty(ref _boolValueRaw, value))
                    RaisePropertyChanged(nameof(FinalValueRaw));
            }
        }

        private bool _isEnabled = true;
        public bool IsEnabled {
            get => _isEnabled;
            set => SetProperty(ref _isEnabled, value);
        }

        private string _errorMessage;
        public string ErrorMessage {
            get => _errorMessage;
            set => SetProperty(ref _errorMessage, value);
        }

        public string GeneratedPath => SelectedAttribute?.FullPath ?? "";
        public string ExpectedType => SelectedAttribute?.ValueKind.ToString() ?? "";
        public string HelpText => SelectedAttribute?.HelpText ?? "Select a config root, section, and attribute.";
        public bool IsBooleanValue => SelectedAttribute?.ValueKind == OverrideValueKind.Boolean;
        public string FinalValueRaw => IsBooleanValue ? BoolValueRaw : ValueRaw;

        public ProfileOverridePickerViewModel() {
            BuildRoots();
            SelectedRoot = RootOptions.FirstOrDefault();
        }

        private void BuildRoots() {
            RootOptions.Clear();

            RootOptions.Add(new OverridePickerOption {
                DisplayName = "Validation Config",
                PathSegment = "validation"
            });

            RootOptions.Add(new OverridePickerOption {
                DisplayName = "Naming Rules",
                PathSegment = "naming"
            });

            RootOptions.Add(new OverridePickerOption {
                DisplayName = "Budgets",
                PathSegment = "budgets"
            });
        }

        private void RebuildSections() {
            SectionOptions.Clear();
            AttributeOptions.Clear();

            if (SelectedRoot == null)
                return;

            switch (SelectedRoot.PathSegment) {
                case "validation":
                    SectionOptions.Add(new OverridePickerOption {
                        DisplayName = "General Validation",
                        PathSegment = "validation"
                    });
                    break;

                case "naming":
                    SectionOptions.Add(new OverridePickerOption {
                        DisplayName = "Naming Rules",
                        PathSegment = "naming"
                    });
                    break;

                case "budgets":
                    AddBudgetSections();
                    break;
            }

            SelectedSection = SectionOptions.FirstOrDefault();
        }

        private void AddBudgetSections() {
            SectionOptions.Add(new OverridePickerOption { DisplayName = "Geometry", PathSegment = "geometry" });
            SectionOptions.Add(new OverridePickerOption { DisplayName = "UV", PathSegment = "uv" });
            SectionOptions.Add(new OverridePickerOption { DisplayName = "Materials", PathSegment = "materials" });
            SectionOptions.Add(new OverridePickerOption { DisplayName = "Textures", PathSegment = "textures" });
            SectionOptions.Add(new OverridePickerOption { DisplayName = "Rigging", PathSegment = "rigging" });
            SectionOptions.Add(new OverridePickerOption { DisplayName = "Animation", PathSegment = "animation" });
            SectionOptions.Add(new OverridePickerOption { DisplayName = "Lighting", PathSegment = "lighting" });
            SectionOptions.Add(new OverridePickerOption { DisplayName = "Camera", PathSegment = "camera" });
            SectionOptions.Add(new OverridePickerOption { DisplayName = "Render", PathSegment = "render" });
            SectionOptions.Add(new OverridePickerOption { DisplayName = "Output", PathSegment = "output" });
            SectionOptions.Add(new OverridePickerOption { DisplayName = "Color Management", PathSegment = "color_management" });
            SectionOptions.Add(new OverridePickerOption { DisplayName = "Scene Hygiene", PathSegment = "scene_hygiene" });
            SectionOptions.Add(new OverridePickerOption { DisplayName = "Export", PathSegment = "export" });
            SectionOptions.Add(new OverridePickerOption { DisplayName = "Performance", PathSegment = "performance" });
        }

        private void RebuildAttributes() {
            AttributeOptions.Clear();

            if (SelectedRoot == null || SelectedSection == null)
                return;

            if (SelectedRoot.PathSegment == "validation")
                AddValidationAttributes();
            else if (SelectedRoot.PathSegment == "naming")
                AddNamingAttributes();
            else if (SelectedRoot.PathSegment == "budgets")
                AddBudgetAttributes(SelectedSection.PathSegment);

            SelectedAttribute = AttributeOptions.FirstOrDefault();
        }

        private void AddValidationAttributes() {
            AddAttr("Strict Mode", "validation.strict_mode", OverrideValueKind.Boolean, "true", "Enables strict validation behavior.");
            AddAttr("Fail On First Error", "validation.fail_on_first_error", OverrideValueKind.Boolean, "false", "Stops validation after the first error.");
            AddAttr("Auto Fix Enabled", "validation.auto_fix_enabled", OverrideValueKind.Boolean, "false", "Allows automatic fixes where supported.");
            AddAttr("Include Info", "validation.include_info", OverrideValueKind.Boolean, "true", "Includes informational validation results.");
            AddAttr("Include Warnings", "validation.include_warnings", OverrideValueKind.Boolean, "true", "Includes warning validation results.");
            AddAttr("Debug Mode", "validation.debug_mode", OverrideValueKind.Boolean, "false", "Enables debug output.");
        }

        private void AddNamingAttributes() {
            AddAttr("Valid Prefixes", "naming.valid_prefixes", OverrideValueKind.JsonArray, "[\"CH\",\"PROP\",\"ENV\"]", "JSON array of allowed naming prefixes.");
            AddAttr("Default Maya Names", "naming.default_maya_names", OverrideValueKind.JsonArray, "[\"pCube\",\"pSphere\",\"polySurface\"]", "JSON array of forbidden default Maya names.");
            AddAttr("Name Pattern", "naming.name_pattern", OverrideValueKind.Regex, "^[A-Z]+_[A-Za-z0-9_]+$", "Regex pattern used to validate object names.");
        }

        private void AddBudgetAttributes(string section) {
            switch (section) {
                case "geometry":
                    AddAttr("Max Vertices", "budgets.geometry.vertices_max", OverrideValueKind.Integer, "50000", "Maximum allowed vertex count.");
                    AddAttr("Max Triangles", "budgets.geometry.triangles_max", OverrideValueKind.Integer, "100000", "Maximum allowed triangle count.");
                    AddAttr("Max Faces", "budgets.geometry.faces_max", OverrideValueKind.Integer, "50000", "Maximum allowed face count.");
                    AddAttr("Max Edges", "budgets.geometry.edges_max", OverrideValueKind.Integer, "150000", "Maximum allowed edge count.");
                    AddAttr("Max Ngons", "budgets.geometry.ngons_max", OverrideValueKind.Integer, "0", "Maximum allowed n-gon count.");
                    AddAttr("Max Lamina Faces", "budgets.geometry.lamina_faces_max", OverrideValueKind.Integer, "0", "Maximum allowed lamina face count.");
                    AddAttr("Max Isolated Vertices", "budgets.geometry.isolated_vertices_max", OverrideValueKind.Integer, "0", "Maximum allowed isolated vertices.");
                    AddAttr("Max Hard Edges", "budgets.geometry.hard_edges_max", OverrideValueKind.Integer, "1000", "Maximum allowed hard edges.");
                    AddAttr("Max Mesh Count", "budgets.geometry.mesh_count_max", OverrideValueKind.Integer, "50", "Maximum amount of mesh objects.");
                    AddAttr("Max Shells", "budgets.geometry.shells_max", OverrideValueKind.Integer, "20", "Maximum shell count.");
                    AddAttr("Max Bounding Box Diagonal", "budgets.geometry.bounding_box_diagonal_max", OverrideValueKind.Decimal, "10000", "Maximum bounding-box diagonal.");
                    AddAttr("Max Scale", "budgets.geometry.scale_max", OverrideValueKind.Decimal, "1000", "Maximum object scale.");
                    AddAttr("Max Non-Uniform Scale Ratio", "budgets.geometry.non_uniform_scale_ratio_max", OverrideValueKind.Decimal, "10", "Maximum allowed non-uniform scale ratio.");
                    break;

                case "uv":
                    AddAttr("Max UV Sets", "budgets.uv.uv_sets_max", OverrideValueKind.Integer, "2", "Maximum UV set count.");
                    AddAttr("Max Empty UV Sets", "budgets.uv.empty_uv_sets_max", OverrideValueKind.Integer, "0", "Maximum empty UV set count.");
                    AddAttr("Max Duplicate UV Set Names", "budgets.uv.duplicate_uv_set_names_max", OverrideValueKind.Integer, "0", "Maximum duplicate UV set names.");
                    AddAttr("Max UV Shells", "budgets.uv.uv_shells_max", OverrideValueKind.Integer, "100", "Maximum UV shell count.");
                    AddAttr("Max Overlap Percent", "budgets.uv.overlap_percent_max", OverrideValueKind.Decimal, "0", "Maximum overlapping UV percentage.");
                    AddAttr("Max Out Of Range UVs", "budgets.uv.out_of_range_uvs_max", OverrideValueKind.Integer, "0", "Maximum UVs outside allowed range.");
                    AddAttr("Min Texel Density", "budgets.uv.texel_density_min", OverrideValueKind.Decimal, "1", "Minimum texel density.");
                    AddAttr("Max Texel Density", "budgets.uv.texel_density_max", OverrideValueKind.Decimal, "20", "Maximum texel density.");
                    AddAttr("Max UDIM Tiles", "budgets.uv.udim_tiles_max", OverrideValueKind.Integer, "10", "Maximum UDIM tile count.");
                    break;

                case "materials":
                    AddAttr("Max Material Slots", "budgets.materials.material_slots_max", OverrideValueKind.Integer, "6", "Maximum material slots.");
                    AddAttr("Max Unique Materials", "budgets.materials.unique_materials_max", OverrideValueKind.Integer, "10", "Maximum unique materials.");
                    AddAttr("Max Unused Materials", "budgets.materials.unused_materials_max", OverrideValueKind.Integer, "0", "Maximum unused materials.");
                    AddAttr("Max Shader Nodes", "budgets.materials.shader_node_count_max", OverrideValueKind.Integer, "50", "Maximum shader node count.");
                    AddAttr("Max Texture Samplers", "budgets.materials.texture_samplers_max", OverrideValueKind.Integer, "10", "Maximum texture samplers per material.");
                    AddAttr("Max Layered Shaders", "budgets.materials.layered_shaders_max", OverrideValueKind.Integer, "4", "Maximum layered shader count.");
                    AddAttr("Default Material Allowed", "budgets.materials.default_material_allowed", OverrideValueKind.Boolean, "false", "Allows or forbids default material usage.");
                    break;

                case "textures":
                    AddAttr("Max Texture Count", "budgets.textures.texture_count_max", OverrideValueKind.Integer, "50", "Maximum texture count.");
                    AddAttr("Max Texture Resolution", "budgets.textures.texture_resolution_max", OverrideValueKind.Integer, "4096", "Maximum texture resolution.");
                    AddAttr("Min Texture Resolution", "budgets.textures.texture_resolution_min", OverrideValueKind.Integer, "256", "Minimum texture resolution.");
                    AddAttr("Max 4K Textures", "budgets.textures.textures_4k_max", OverrideValueKind.Integer, "10", "Maximum 4K texture count.");
                    AddAttr("Max 8K Textures", "budgets.textures.textures_8k_max", OverrideValueKind.Integer, "0", "Maximum 8K texture count.");
                    AddAttr("Max Total Texture Memory MB", "budgets.textures.total_texture_memory_mb_max", OverrideValueKind.Integer, "2048", "Maximum total texture memory.");
                    AddAttr("Max Missing Textures", "budgets.textures.missing_textures_max", OverrideValueKind.Integer, "0", "Maximum missing textures.");
                    AddAttr("Max Non-Power-Of-Two Textures", "budgets.textures.non_power_of_two_max", OverrideValueKind.Integer, "0", "Maximum non-power-of-two textures.");
                    break;

                case "rigging":
                    AddAttr("Max Joints", "budgets.rigging.joint_count_max", OverrideValueKind.Integer, "256", "Maximum joint count.");
                    AddAttr("Max Deform Joints", "budgets.rigging.deform_joints_max", OverrideValueKind.Integer, "128", "Maximum deform joint count.");
                    AddAttr("Max Controls", "budgets.rigging.controls_max", OverrideValueKind.Integer, "300", "Maximum rig control count.");
                    AddAttr("Max Constraints", "budgets.rigging.constraints_max", OverrideValueKind.Integer, "200", "Maximum constraints.");
                    AddAttr("Max Blendshapes", "budgets.rigging.blendshapes_max", OverrideValueKind.Integer, "100", "Maximum blendshape count.");
                    AddAttr("Max Influences Per Vertex", "budgets.rigging.influences_per_vertex_max", OverrideValueKind.Integer, "4", "Maximum skinning influences per vertex.");
                    break;

                case "animation":
                    AddAttr("Max Key Count", "budgets.animation.key_count_max", OverrideValueKind.Integer, "10000", "Maximum animation key count.");
                    AddAttr("Max Keyed Channels", "budgets.animation.keyed_channels_max", OverrideValueKind.Integer, "500", "Maximum keyed channel count.");
                    AddAttr("Max Frame Range", "budgets.animation.frame_range_max", OverrideValueKind.Integer, "2000", "Maximum frame range.");
                    AddAttr("Max Animation Layers", "budgets.animation.animation_layers_max", OverrideValueKind.Integer, "10", "Maximum animation layer count.");
                    AddAttr("Max Clips", "budgets.animation.clips_max", OverrideValueKind.Integer, "50", "Maximum animation clip count.");
                    break;

                case "lighting":
                    AddAttr("Max Light Count", "budgets.lighting.light_count_max", OverrideValueKind.Integer, "50", "Maximum light count.");
                    AddAttr("Max Shadow Casters", "budgets.lighting.shadow_casters_max", OverrideValueKind.Integer, "20", "Maximum shadow-casting lights.");
                    AddAttr("Max Area Lights", "budgets.lighting.area_lights_max", OverrideValueKind.Integer, "20", "Maximum area lights.");
                    AddAttr("Max Environment Lights", "budgets.lighting.environment_lights_max", OverrideValueKind.Integer, "2", "Maximum environment lights.");
                    AddAttr("Max Light Groups", "budgets.lighting.light_groups_max", OverrideValueKind.Integer, "10", "Maximum light groups.");
                    AddAttr("Max Volumetric Lights", "budgets.lighting.volumetric_lights_max", OverrideValueKind.Integer, "5", "Maximum volumetric lights.");
                    break;

                case "camera":
                    AddAttr("Max Camera Count", "budgets.camera.camera_count_max", OverrideValueKind.Integer, "10", "Maximum camera count.");
                    AddAttr("Max Renderable Cameras", "budgets.camera.renderable_cameras_max", OverrideValueKind.Integer, "1", "Maximum renderable cameras.");
                    AddAttr("Max Overscan", "budgets.camera.overscan_max", OverrideValueKind.Decimal, "1.1", "Maximum overscan value.");
                    AddAttr("Min Focal Length", "budgets.camera.focal_length_min", OverrideValueKind.Decimal, "12", "Minimum focal length.");
                    AddAttr("Max Focal Length", "budgets.camera.focal_length_max", OverrideValueKind.Decimal, "200", "Maximum focal length.");
                    AddAttr("Default Camera Render Allowed", "budgets.camera.default_camera_render_allowed", OverrideValueKind.Boolean, "false", "Allows default cameras to be render cameras.");
                    break;

                case "render":
                    AddAttr("Max AA Samples", "budgets.render.aa_samples_max", OverrideValueKind.Integer, "8", "Maximum anti-aliasing samples.");
                    AddAttr("Max Diffuse Samples", "budgets.render.diffuse_samples_max", OverrideValueKind.Integer, "4", "Maximum diffuse samples.");
                    AddAttr("Max Specular Samples", "budgets.render.specular_samples_max", OverrideValueKind.Integer, "4", "Maximum specular samples.");
                    AddAttr("Max Transmission Samples", "budgets.render.transmission_samples_max", OverrideValueKind.Integer, "4", "Maximum transmission samples.");
                    AddAttr("Max SSS Samples", "budgets.render.sss_samples_max", OverrideValueKind.Integer, "4", "Maximum SSS samples.");
                    AddAttr("Max Volume Samples", "budgets.render.volume_samples_max", OverrideValueKind.Integer, "2", "Maximum volume samples.");
                    AddAttr("Max Adaptive Threshold", "budgets.render.adaptive_threshold_max", OverrideValueKind.Decimal, "0.05", "Maximum adaptive threshold.");
                    AddAttr("Max Noise Threshold", "budgets.render.noise_threshold_max", OverrideValueKind.Decimal, "0.05", "Maximum noise threshold.");
                    AddAttr("Max Tile Size", "budgets.render.tile_size_max", OverrideValueKind.Integer, "512", "Maximum tile size.");
                    AddAttr("Max Total Ray Depth", "budgets.render.ray_depth_total_max", OverrideValueKind.Integer, "8", "Maximum total ray depth.");
                    AddAttr("Max Diffuse Ray Depth", "budgets.render.ray_depth_diffuse_max", OverrideValueKind.Integer, "2", "Maximum diffuse ray depth.");
                    AddAttr("Max Specular Ray Depth", "budgets.render.ray_depth_specular_max", OverrideValueKind.Integer, "2", "Maximum specular ray depth.");
                    AddAttr("Max Transmission Ray Depth", "budgets.render.ray_depth_transmission_max", OverrideValueKind.Integer, "4", "Maximum transmission ray depth.");
                    break;

                case "output":
                    AddAttr("Max Resolution X", "budgets.output.resolution_x_max", OverrideValueKind.Integer, "4096", "Maximum output width.");
                    AddAttr("Max Resolution Y", "budgets.output.resolution_y_max", OverrideValueKind.Integer, "4096", "Maximum output height.");
                    AddAttr("Min Resolution X", "budgets.output.resolution_x_min", OverrideValueKind.Integer, "640", "Minimum output width.");
                    AddAttr("Min Resolution Y", "budgets.output.resolution_y_min", OverrideValueKind.Integer, "360", "Minimum output height.");
                    AddAttr("Max AOV Count", "budgets.output.aov_count_max", OverrideValueKind.Integer, "20", "Maximum AOV count.");
                    AddAttr("Require Multilayer EXR", "budgets.output.required_multilayer_exr", OverrideValueKind.Boolean, "false", "Requires multilayer EXR output.");
                    AddAttr("Output Path Must Be Writable", "budgets.output.output_path_must_be_writable", OverrideValueKind.Boolean, "true", "Requires writable output path.");
                    break;

                case "color_management":
                    AddAttr("ACES Required", "budgets.color_management.aces_required", OverrideValueKind.Boolean, "false", "Requires ACES color management.");
                    AddAttr("Linear Workflow Required", "budgets.color_management.linear_workflow_required", OverrideValueKind.Boolean, "true", "Requires linear workflow.");
                    AddAttr("Min Gamma", "budgets.color_management.gamma_min", OverrideValueKind.Decimal, "0.8", "Minimum gamma value.");
                    AddAttr("Max Gamma", "budgets.color_management.gamma_max", OverrideValueKind.Decimal, "2.2", "Maximum gamma value.");
                    AddAttr("Min Exposure", "budgets.color_management.exposure_min", OverrideValueKind.Decimal, "-5", "Minimum exposure value.");
                    AddAttr("Max Exposure", "budgets.color_management.exposure_max", OverrideValueKind.Decimal, "5", "Maximum exposure value.");
                    break;

                case "scene_hygiene":
                    AddAttr("Max Unknown Nodes", "budgets.scene_hygiene.unknown_nodes_max", OverrideValueKind.Integer, "0", "Maximum unknown nodes.");
                    AddAttr("Max Duplicate Names", "budgets.scene_hygiene.duplicate_names_max", OverrideValueKind.Integer, "0", "Maximum duplicate object names.");
                    AddAttr("Max Namespaces", "budgets.scene_hygiene.namespaces_max", OverrideValueKind.Integer, "5", "Maximum namespace count.");
                    AddAttr("Max Broken References", "budgets.scene_hygiene.broken_references_max", OverrideValueKind.Integer, "0", "Maximum broken references.");
                    AddAttr("Max Missing References", "budgets.scene_hygiene.missing_references_max", OverrideValueKind.Integer, "0", "Maximum missing references.");
                    AddAttr("Max Script Nodes", "budgets.scene_hygiene.script_nodes_max", OverrideValueKind.Integer, "0", "Maximum script nodes.");
                    AddAttr("Max Expressions", "budgets.scene_hygiene.expressions_max", OverrideValueKind.Integer, "0", "Maximum expressions.");
                    break;

                case "export":
                    AddAttr("Max Export File Size MB", "budgets.export.export_file_size_mb_max", OverrideValueKind.Integer, "500", "Maximum export file size in MB.");
                    AddAttr("Max Draw Calls", "budgets.export.draw_calls_max", OverrideValueKind.Integer, "1000", "Maximum draw calls.");
                    AddAttr("Max Submeshes", "budgets.export.submeshes_max", OverrideValueKind.Integer, "20", "Maximum submesh count.");
                    AddAttr("Max LOD Count", "budgets.export.lod_count_max", OverrideValueKind.Integer, "4", "Maximum LOD count.");
                    AddAttr("Max Collision Meshes", "budgets.export.collision_meshes_max", OverrideValueKind.Integer, "10", "Maximum collision mesh count.");
                    break;

                case "performance":
                    AddAttr("Max Validation Runtime Seconds", "budgets.performance.validation_runtime_seconds_max", OverrideValueKind.Integer, "120", "Maximum validation runtime.");
                    AddAttr("Max Scene Open Time Seconds", "budgets.performance.scene_open_time_seconds_max", OverrideValueKind.Integer, "60", "Maximum scene open time.");
                    AddAttr("Max Memory Estimate MB", "budgets.performance.memory_estimate_mb_max", OverrideValueKind.Integer, "8192", "Maximum memory estimate.");
                    AddAttr("Max Render Cost Score", "budgets.performance.render_cost_score_max", OverrideValueKind.Integer, "100", "Maximum render cost score.");
                    AddAttr("Max JSON Report Size KB", "budgets.performance.json_report_size_kb_max", OverrideValueKind.Integer, "2048", "Maximum report size.");
                    break;
            }
        }

        private void AddAttr(string display, string fullPath, OverrideValueKind kind, string defaultRaw, string help) {
            AttributeOptions.Add(new OverridePickerOption {
                DisplayName = display,
                FullPath = fullPath,
                ValueKind = kind,
                DefaultValueRaw = defaultRaw,
                HelpText = help
            });
        }

        private void ApplySelectedAttributeDefaults() {
            ErrorMessage = "";

            if (SelectedAttribute == null) {
                ValueRaw = "";
                BoolValueRaw = "true";
            } else if (SelectedAttribute.ValueKind == OverrideValueKind.Boolean) {
                BoolValueRaw = SelectedAttribute.DefaultValueRaw == "false" ? "false" : "true";
                ValueRaw = "";
            } else {
                ValueRaw = SelectedAttribute.DefaultValueRaw ?? "";
            }

            RaisePropertyChanged(nameof(GeneratedPath));
            RaisePropertyChanged(nameof(ExpectedType));
            RaisePropertyChanged(nameof(HelpText));
            RaisePropertyChanged(nameof(IsBooleanValue));
            RaisePropertyChanged(nameof(FinalValueRaw));
        }

        public bool TryConfirm() {
            ErrorMessage = "";

            if (SelectedAttribute == null) {
                ErrorMessage = "No attribute selected.";
                return false;
            }

            var raw = FinalValueRaw;

            if (string.IsNullOrWhiteSpace(raw)) {
                ErrorMessage = "Value cannot be empty.";
                return false;
            }

            switch (SelectedAttribute.ValueKind) {
                case OverrideValueKind.Boolean:
                    if (raw != "true" && raw != "false") {
                        ErrorMessage = "Boolean value must be true or false.";
                        return false;
                    }
                    break;

                case OverrideValueKind.Integer:
                    if (!int.TryParse(raw, NumberStyles.Integer, CultureInfo.InvariantCulture, out _)) {
                        ErrorMessage = "Value must be a valid integer.";
                        return false;
                    }
                    break;

                case OverrideValueKind.Decimal:
                    if (!double.TryParse(raw, NumberStyles.Float, CultureInfo.InvariantCulture, out _)) {
                        ErrorMessage = "Value must be a valid decimal number.";
                        return false;
                    }
                    break;

                case OverrideValueKind.JsonArray:
                    try {
                        using (var doc = JsonDocument.Parse(raw)) {
                            if (doc.RootElement.ValueKind != JsonValueKind.Array) {
                                ErrorMessage = "Value must be a valid JSON array.";
                                return false;
                            }
                        }
                    } catch {
                        ErrorMessage = "Value must be a valid JSON array.";
                        return false;
                    }
                    break;

                case OverrideValueKind.Regex:
                    try {
                        _ = new Regex(raw);
                    } catch {
                        ErrorMessage = "Value must be a valid regex pattern.";
                        return false;
                    }
                    break;

                case OverrideValueKind.String:
                    break;
            }

            return true;
        }
    }
}