

"""
Validation check identifiers, grouped by execution stage.

Format:
    [STAGE] CHECK_NAME - short explanation
"""

# ============================================================
# NAMING
# ============================================================

CHECK_NAMING = "CHECK_NAMING"  # Generic object naming validation, might be long and verbose
CHECK_RENDER_LAYER_NAME_VALID = "CHECK_RENDER_LAYER_NAME_VALID"  # Render layer name valid
CHECK_AOV_NAME_VALID = "CHECK_AOV_NAME_VALID"  # AOV name valid
CHECK_OUTPUT_NAMING_PATTERN_VALID = "CHECK_OUTPUT_NAMING_PATTERN_VALID"  # Output naming follows pipeline
CHECK_DEFAULT_DCC_NAMING = "CHECK_DEFAULT_DCC_NAMING"
CHECK_DOUBLE_UNDERSCORE = "CHECK_DOUBLE_UNDERSCORE"
CHECK_NAME_PATTERN = "CHECK_NAME_PATTERN"
CHECK_INVALID_CHARACTERS = "CHECK_INVALID_CHARACTERS"
CHECK_VALID_PREFIX = "CHECK_VALID_PREFIX"


# ============================================================
# SCENE
# ============================================================

CHECK_SCENE_HAS_VALID_OUTPUT_PATH = "CHECK_SCENE_HAS_VALID_OUTPUT_PATH"  # Output path exists
CHECK_SCENE_OUTPUT_IS_WRITABLE = "CHECK_SCENE_OUTPUT_IS_WRITABLE"  # Output directory writable
CHECK_DEFAULT_PROJECT_PATH_USED = "CHECK_DEFAULT_PROJECT_PATH_USED"  # Default Maya project used


# ============================================================
# HIERARCHY
# ============================================================

# Reserved for future hierarchy checks


# ============================================================
# TRANSFORM
# ============================================================

CHECK_TRANSFORMS = "CHECK_TRANSFORMS"  # Generic transform validation
CHECK_NEGATIVE_SCALE = "CHECK_NEGATIVE_SCALE"  # Negative scale detected
CHECK_NON_UNIFORM_SCALE = "CHECK_NON_UNIFORM_SCALE"  # Non-uniform scale detected
CHECK_ZERO_SCALE = "CHECK_ZERO_SCALE"  # Zero scale detected
CHECK_EXTREME_SCALE = "CHECK_EXTREME_SCALE"  # Extreme scale detected


# ============================================================
# GEOMETRY
# ============================================================

CHECK_VERTEX_COUNT = "CHECK_VERTEX_COUNT"  # Vertex count exceeds budget
CHECK_TRIANGLE_COUNT = "CHECK_TRIANGLE_COUNT"  # Triangle count exceeds budget
CHECK_NON_MANIFOLD = "CHECK_NON_MANIFOLD"  # Non-manifold geometry detected
CHECK_DEGENERATE_FACES = "CHECK_DEGENERATE_FACES"  # Degenerate faces detected
CHECK_BOUNDING_BOX = "CHECK_BOUNDING_BOX"  # Bounding box invalid
CHECK_HIDDEN_GEOMETRY = "CHECK_HIDDEN_GEOMETRY"  # Hidden geometry detected
CHECK_COLLISION_READINESS = "CHECK_COLLISION_READINESS"  # Collision-readiness invalid
CHECK_ZERO_AREA_FACES = "CHECK_ZERO_AREA_FACES"
CHECK_NGONS = "CHECK_NGONS"
CHECK_ISOLATED_VERTICES = "CHECK_ISOLATED_VERTICES"
CHECK_OVERLAPPING_GEOMETRY = "CHECK_OVERLAPPING_GEOMETRY"
CHECK_NORMALS = "CHECK_NORMALS"
CHECK_BROKEN_NORMALS = "CHECK_BROKEN_NORMALS"
CHECK_HARD_EDGES = "CHECK_HARD_EDGES"
CHECK_LAMINA_FACES = "CHECK_LAMINA_FACES" #Mesh contains lamina faces which are faces that share all vertices with another face.
# ============================================================
# UV
# ============================================================

CHECK_UV_SETS = "CHECK_UV_SETS"  # Generic UV sets validation
CHECK_MISSING_UV0 = "CHECK_MISSING_UV0"  # Missing primary UV set
CHECK_MISSING_UV1 = "CHECK_MISSING_UV1"  # Missing secondary UV set
CHECK_TOO_MANY_UV_SETS = "CHECK_TOO_MANY_UV_SETS"  # Too many UV sets
CHECK_EMPTY_UV_SET_NAME = "CHECK_EMPTY_UV_SET_NAME"  # Empty UV set name
CHECK_DUPLICATE_UV_SET_NAMES = "CHECK_DUPLICATE_UV_SET_NAMES"  # Duplicate UV set names


# ============================================================
# MATERIAL
# ============================================================

CHECK_MATERIAL_SLOTS = "CHECK_MATERIAL_SLOTS"  # Material slot count invalid
CHECK_MATERIAL_SLOTS_EXIST = "CHECK_MATERIAL_SLOTS_EXIST"  # Material slot count invalid


# ============================================================
# RIG
# ============================================================

CHECK_SKELETON_COMPAT = "CHECK_SKELETON_COMPAT"  # Skeleton compatibility invalid


# ============================================================
# ANIMATION
# ============================================================

# Reserved for future animation checks


# ============================================================
# CAMERA
# ============================================================

CHECK_HAS_RENDER_CAMERA = "CHECK_HAS_RENDER_CAMERA"  # At least one render camera exists
CHECK_NO_DUPLICATE_RENDER_CAMERAS = "CHECK_NO_DUPLICATE_RENDER_CAMERAS"  # Only one render camera allowed
CHECK_NO_DEFAULT_RENDER_CAMERA_USED = "CHECK_NO_DEFAULT_RENDER_CAMERA_USED"  # Default camera used for render
CHECK_EXPECTED_SHOT_CAMERA_PRESENT = "CHECK_EXPECTED_SHOT_CAMERA_PRESENT"  # Expected shot camera exists


# ============================================================
# LIGHT
# ============================================================

CHECK_ENVIRONMENT_LIGHT_PRESENCE_WARNING = "CHECK_ENVIRONMENT_LIGHT_PRESENCE_WARNING"  # Missing environment light


# ============================================================
# REFERENCE
# ============================================================

# Reserved for future reference checks


# ============================================================
# RENDER
# ============================================================

# --- Renderer / Device ---
CHECK_RENDERER_SUPPORTED = "CHECK_RENDERER_SUPPORTED"  # Renderer allowed by pipeline
CHECK_RENDER_DEVICE_EXPECTED = "CHECK_RENDER_DEVICE_EXPECTED"  # CPU/GPU choice valid
CHECK_RENDER_MODE_VALID = "CHECK_RENDER_MODE_VALID"  # Render mode valid
CHECK_BUCKET_SCANNING_VALID = "CHECK_BUCKET_SCANNING_VALID"  # Bucket scanning valid

# --- Sampling ---
CHECK_AA_SAMPLES_REASONABLE = "CHECK_AA_SAMPLES_REASONABLE"  # AA samples within limits
CHECK_SAMPLING_BALANCE_VALID = "CHECK_SAMPLING_BALANCE_VALID"  # Sampling values balanced
CHECK_ADAPTIVE_SAMPLING_CONFIG_VALID = "CHECK_ADAPTIVE_SAMPLING_CONFIG_VALID"  # Adaptive sampling configured
CHECK_NOISE_THRESHOLD_VALID = "CHECK_NOISE_THRESHOLD_VALID"  # Noise threshold valid
CHECK_SAMPLE_COUNTS_NOT_ZERO = "CHECK_SAMPLE_COUNTS_NOT_ZERO"  # Sample counts not zero
CHECK_TEXTURE_SAMPLING_MODE_VALID = "CHECK_TEXTURE_SAMPLING_MODE_VALID"  # Texture sampling mode set

# --- Clamping ---
CHECK_SAMPLE_CLAMPING_ENABLED = "CHECK_SAMPLE_CLAMPING_ENABLED"  # Sample clamp enabled
CHECK_CLAMP_VALUE_REASONABLE = "CHECK_CLAMP_VALUE_REASONABLE"  # Clamp value acceptable
CHECK_CLAMP_USAGE_WARNING = "CHECK_CLAMP_USAGE_WARNING"  # Clamp may hide artifacts

# --- Subdivision / Performance ---
CHECK_SUBDIVISION_ITERATIONS_VALID = "CHECK_SUBDIVISION_ITERATIONS_VALID"  # Subdivision iterations valid
CHECK_HIGH_SUBDIVISION_WARNING = "CHECK_HIGH_SUBDIVISION_WARNING"  # Subdivision too high
CHECK_LOW_RESOLUTION_WARNING = "CHECK_LOW_RESOLUTION_WARNING"  # Resolution too low
CHECK_NO_ADAPTIVE_SAMPLING_WARNING = "CHECK_NO_ADAPTIVE_SAMPLING_WARNING"  # Adaptive sampling disabled
CHECK_CPU_RENDER_WARNING = "CHECK_CPU_RENDER_WARNING"  # CPU rendering may be slow

# --- Denoising / Motion ---
CHECK_DENOISER_CONFIG_VALID = "CHECK_DENOISER_CONFIG_VALID"  # Denoiser configured correctly
CHECK_MOTION_BLUR_EXPECTED = "CHECK_MOTION_BLUR_EXPECTED"  # Motion blur usage valid
CHECK_DEPTH_OF_FIELD_EXPECTED = "CHECK_DEPTH_OF_FIELD_EXPECTED"  # DOF usage valid

# --- Output ---
CHECK_OUTPUT_PREFIX_PRESENT = "CHECK_OUTPUT_PREFIX_PRESENT"  # Output prefix defined
CHECK_IMAGE_FORMAT_ALLOWED = "CHECK_IMAGE_FORMAT_ALLOWED"  # Image format allowed
CHECK_BIT_DEPTH_VALID = "CHECK_BIT_DEPTH_VALID"  # Bit depth valid
CHECK_COMPRESSION_SET = "CHECK_COMPRESSION_SET"  # Compression defined
CHECK_COMPRESSION_VALID_FOR_FORMAT = "CHECK_COMPRESSION_VALID_FOR_FORMAT"  # Compression valid for format
CHECK_MULTILAYER_EXPECTED_FOR_EXR = "CHECK_MULTILAYER_EXPECTED_FOR_EXR"  # EXR should be multilayer
CHECK_ALPHA_ENABLED_WHEN_NEEDED = "CHECK_ALPHA_ENABLED_WHEN_NEEDED"  # Alpha enabled when needed
CHECK_RESOLUTION_VALID = "CHECK_RESOLUTION_VALID"  # Resolution allowed
CHECK_ASPECT_RATIO_VALID = "CHECK_ASPECT_RATIO_VALID"  # Aspect ratio valid
CHECK_RESOLUTION_NOT_TOO_LOW = "CHECK_RESOLUTION_NOT_TOO_LOW"  # Resolution not too low
CHECK_RENDER_SCALE_IS_100 = "CHECK_RENDER_SCALE_IS_100"  # Render scale 100 percent
CHECK_PIXEL_ASPECT_VALID = "CHECK_PIXEL_ASPECT_VALID"  # Pixel aspect valid
CHECK_OVERSCAN_EXPECTED_OR_NOT = "CHECK_OVERSCAN_EXPECTED_OR_NOT"  # Overscan usage valid

# --- Color Management ---
CHECK_COLOR_MANAGEMENT_ENABLED = "CHECK_COLOR_MANAGEMENT_ENABLED"  # Linear workflow enabled
CHECK_ACES_USAGE_EXPECTED = "CHECK_ACES_USAGE_EXPECTED"  # ACES usage valid
CHECK_RENDER_COLOR_SPACE_SET = "CHECK_RENDER_COLOR_SPACE_SET"  # Render color space set
CHECK_OCIO_CONFIG_VALID = "CHECK_OCIO_CONFIG_VALID"  # OCIO config valid
CHECK_VIEW_TRANSFORM_ALLOWED = "CHECK_VIEW_TRANSFORM_ALLOWED"  # View transform allowed

# --- Render Layers ---
CHECK_RENDER_LAYER_EXISTS = "CHECK_RENDER_LAYER_EXISTS"  # Render layer exists
CHECK_ONLY_ONE_ACTIVE_LAYER = "CHECK_ONLY_ONE_ACTIVE_LAYER"  # One active layer only
CHECK_RENDER_LAYER_HAS_MEMBERS = "CHECK_RENDER_LAYER_HAS_MEMBERS"  # Render layer has members
CHECK_RENDER_LAYER_HAS_CAMERA = "CHECK_RENDER_LAYER_HAS_CAMERA"  # Render layer has camera
CHECK_RENDER_LAYER_NOT_DEFAULT_ONLY = "CHECK_RENDER_LAYER_NOT_DEFAULT_ONLY"  # Only default layer used

# --- AOVs ---
CHECK_AOV_PRESENCE_REQUIRED = "CHECK_AOV_PRESENCE_REQUIRED"  # Required AOVs present
CHECK_DUPLICATE_AOV_NAMES = "CHECK_DUPLICATE_AOV_NAMES"  # Duplicate AOV names
CHECK_INVALID_LIGHT_GROUP_SETUP = "CHECK_INVALID_LIGHT_GROUP_SETUP"  # Invalid light groups
CHECK_INVALID_DRIVER_OR_FILTER = "CHECK_INVALID_DRIVER_OR_FILTER"  # Invalid AOV driver or filter


# ============================================================
# HISTORY
# ============================================================

# Reserved for future history checks, BUT...
CHECK_HISTORY = "CHECK_HISTORY"


# ============================================================
# PRE_EXPORT
# ============================================================

CHECK_SCENE_READY_FOR_EXPORT = "CHECK_SCENE_READY_FOR_EXPORT"  # Scene ready for export
CHECK_MISSING_REQUIRED_AOVS = "CHECK_MISSING_REQUIRED_AOVS"  # Required AOVs missing


CHECKS_BY_STAGE = {
    "NAMING": [
        CHECK_NAMING,
        CHECK_RENDER_LAYER_NAME_VALID,
        CHECK_AOV_NAME_VALID,
        CHECK_OUTPUT_NAMING_PATTERN_VALID,
        CHECK_DEFAULT_DCC_NAMING,
        CHECK_DOUBLE_UNDERSCORE,
        CHECK_NAME_PATTERN,
        CHECK_INVALID_CHARACTERS,
        CHECK_VALID_PREFIX
    ],

    "SCENE": [
        CHECK_SCENE_HAS_VALID_OUTPUT_PATH,
        CHECK_SCENE_OUTPUT_IS_WRITABLE,
        CHECK_DEFAULT_PROJECT_PATH_USED,
    ],

    "TRANSFORM": [
        CHECK_TRANSFORMS,
        CHECK_NEGATIVE_SCALE,
        CHECK_NON_UNIFORM_SCALE,
        CHECK_ZERO_SCALE,
        CHECK_EXTREME_SCALE,
    ],

    "GEOMETRY": [
        CHECK_VERTEX_COUNT,
        CHECK_TRIANGLE_COUNT,
        CHECK_NON_MANIFOLD,
        CHECK_DEGENERATE_FACES,
        CHECK_BOUNDING_BOX,
        CHECK_HIDDEN_GEOMETRY,
        CHECK_COLLISION_READINESS,
        CHECK_NORMALS,
        CHECK_BROKEN_NORMALS
    ],

    "UV": [
        CHECK_UV_SETS,
        CHECK_MISSING_UV0,
        CHECK_MISSING_UV1,
        CHECK_TOO_MANY_UV_SETS,
        CHECK_EMPTY_UV_SET_NAME,
        CHECK_DUPLICATE_UV_SET_NAMES,
    ],

    "MATERIAL": [
        CHECK_MATERIAL_SLOTS,
    ],

    "RIG": [
        CHECK_SKELETON_COMPAT,
    ],

    "CAMERA": [
        CHECK_HAS_RENDER_CAMERA,
        CHECK_NO_DUPLICATE_RENDER_CAMERAS,
        CHECK_NO_DEFAULT_RENDER_CAMERA_USED,
        CHECK_EXPECTED_SHOT_CAMERA_PRESENT,
    ],

    "LIGHT": [
        CHECK_ENVIRONMENT_LIGHT_PRESENCE_WARNING,
    ],

    "RENDER": [
        CHECK_RENDERER_SUPPORTED,
        CHECK_RENDER_DEVICE_EXPECTED,
        CHECK_RENDER_MODE_VALID,
        CHECK_BUCKET_SCANNING_VALID,

        CHECK_AA_SAMPLES_REASONABLE,
        CHECK_SAMPLING_BALANCE_VALID,
        CHECK_ADAPTIVE_SAMPLING_CONFIG_VALID,
        CHECK_NOISE_THRESHOLD_VALID,
        CHECK_SAMPLE_COUNTS_NOT_ZERO,
        CHECK_TEXTURE_SAMPLING_MODE_VALID,

        CHECK_SAMPLE_CLAMPING_ENABLED,
        CHECK_CLAMP_VALUE_REASONABLE,
        CHECK_CLAMP_USAGE_WARNING,

        CHECK_SUBDIVISION_ITERATIONS_VALID,
        CHECK_HIGH_SUBDIVISION_WARNING,
        CHECK_LOW_RESOLUTION_WARNING,
        CHECK_NO_ADAPTIVE_SAMPLING_WARNING,
        CHECK_CPU_RENDER_WARNING,

        CHECK_DENOISER_CONFIG_VALID,
        CHECK_MOTION_BLUR_EXPECTED,
        CHECK_DEPTH_OF_FIELD_EXPECTED,

        CHECK_OUTPUT_PREFIX_PRESENT,
        CHECK_IMAGE_FORMAT_ALLOWED,
        CHECK_BIT_DEPTH_VALID,
        CHECK_COMPRESSION_SET,
        CHECK_COMPRESSION_VALID_FOR_FORMAT,
        CHECK_MULTILAYER_EXPECTED_FOR_EXR,
        CHECK_ALPHA_ENABLED_WHEN_NEEDED,
        CHECK_RESOLUTION_VALID,
        CHECK_ASPECT_RATIO_VALID,
        CHECK_RESOLUTION_NOT_TOO_LOW,
        CHECK_RENDER_SCALE_IS_100,
        CHECK_PIXEL_ASPECT_VALID,
        CHECK_OVERSCAN_EXPECTED_OR_NOT,

        CHECK_COLOR_MANAGEMENT_ENABLED,
        CHECK_ACES_USAGE_EXPECTED,
        CHECK_RENDER_COLOR_SPACE_SET,
        CHECK_OCIO_CONFIG_VALID,
        CHECK_VIEW_TRANSFORM_ALLOWED,

        CHECK_RENDER_LAYER_EXISTS,
        CHECK_ONLY_ONE_ACTIVE_LAYER,
        CHECK_RENDER_LAYER_HAS_MEMBERS,
        CHECK_RENDER_LAYER_HAS_CAMERA,
        CHECK_RENDER_LAYER_NOT_DEFAULT_ONLY,

        CHECK_AOV_PRESENCE_REQUIRED,
        CHECK_DUPLICATE_AOV_NAMES,
        CHECK_INVALID_LIGHT_GROUP_SETUP,
        CHECK_INVALID_DRIVER_OR_FILTER,
    ],

    "PRE_EXPORT": [
        CHECK_SCENE_READY_FOR_EXPORT,
        CHECK_MISSING_REQUIRED_AOVS,
    ],
}