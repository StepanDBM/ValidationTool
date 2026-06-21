import maya.cmds as cmds


def createBase(lCTRL, rCTRL):

    rmpC = cmds.createNode("remapColor", name="mx_zip_inv_rmC")

    cmds.setAttr(f"{rmpC}.inputMin", -1)
    for axis in ["red", "green"]:

        cmds.setAttr(rmpC + f".{axis}[0].{axis}_Position", 0)
        cmds.setAttr(rmpC + f".{axis}[0].{axis}_FloatValue", 0)

        cmds.setAttr(rmpC + f".{axis}[1].{axis}_Position", 0.5)
        cmds.setAttr(rmpC + f".{axis}[1].{axis}_FloatValue", 0.15)

        cmds.setAttr(rmpC + f".{axis}[2].{axis}_Position", 1)
        cmds.setAttr(rmpC + f".{axis}[2].{axis}_FloatValue", 1)
    

    xZIPinvMult = cmds.createNode("multiplyDivide", name="mx_zip_inv_mult")
    lZIPinvMult = cmds.createNode("multiplyDivide", name="ml_zip_norm_mult")
    rZIPinvMult = cmds.createNode("multiplyDivide", name="mr_zip_norm_mult")

    cmds.connectAttr(f"{lCTRL}.zipFalloff", f"{rmpC}.colorR")
    cmds.connectAttr(f"{rCTRL}.zipFalloff", f"{rmpC}.colorG")

    cmds.connectAttr(f"{rmpC}.outColorR", f"{xZIPinvMult}.input1X")
    cmds.connectAttr(f"{rmpC}.outColorG", f"{xZIPinvMult}.input1Y")

    cmds.setAttr(f"{xZIPinvMult}.input2X", -1)
    cmds.setAttr(f"{xZIPinvMult}.input2Y", -1)
    cmds.setAttr(f"{xZIPinvMult}.input2Z", -1)

    cmds.setAttr(f"{lZIPinvMult}.input2X", -1)
    cmds.setAttr(f"{lZIPinvMult}.input2Y", -1)
    cmds.setAttr(f"{lZIPinvMult}.input2Z", -1)

    cmds.setAttr(f"{rZIPinvMult}.input2X", -1)
    cmds.setAttr(f"{rZIPinvMult}.input2Y", -1)
    cmds.setAttr(f"{rZIPinvMult}.input2Z", -1)

    cmds.connectAttr(f"{xZIPinvMult}.outputX", f"{lZIPinvMult}.input1X")
    cmds.connectAttr(f"{xZIPinvMult}.outputY", f"{rZIPinvMult}.input1X")

    cmds.connectAttr(f"{rmpC}.outColorR", f"{lZIPinvMult}.input1Y")
    cmds.connectAttr(f"{rmpC}.outColorG", f"{rZIPinvMult}.input1Y")

    return lZIPinvMult, rZIPinvMult

def get_cv_role(i, total):
    if i == 0:
        return "first"
    if i == total - 1:
        return "last"
    if i == 1:
        return "second"
    if i == total - 2:
        return "second_last"
    return "middle"   


def createZIP_blendHSv(mdA, mdB, dirR, dirL, posUP, posLO, i, total, role, lCTRL, rCTRL):
    """
    example: where there to be 23 PVs.
    Because the tips are NOT moving on ZIP mode, we miss them
    {total - 2} to account for that.
    from the left
        l_MIN (goes down)
        r_MAX (goes up)
    from the right
    l_MAX (goes up)
    l_MIN (goes down)
    LIST OF VALUES of the example
    [ 0.0, 0.047619, 0.095238, 0.142857, 0.190476, 0.238095,
    0.285714, 0.333333, 0.380952, 0.428571, 0.476190,
    0.523810, 0.571429, 0.619048, 0.666667, 0.714286,
    0.761905, 0.809524, 0.857143, 0.904762, 0.952381, 1.0 ]
    """

    zip_count = total - 2
    zip_index = i - 1
    t = zip_index / float(zip_count - 1)

    l_min = t
    l_max = t
    r_min = 1.0 - t
    r_max = 1.0 - t

    # -------------------------------
    # FIXED LAYOUTS
    # -------------------------------
    layouts = {
        "middle": [
            ("l_max", l_max),
            ("l_min", l_min),
            ("r_max", r_max),
            ("r_min", r_min),
        ],

        # first movable CV near LEFT tip:
        # left  = [0, t+falloff]   -> need l_max
        # right = [1-t-falloff, 1] -> need r_min
        "second": [
            ("l_max", l_max),
            ("r_min", r_min),
        ],

        # last movable CV near RIGHT tip:
        # left  = [t-falloff, 1]   -> need l_min
        # right = [0, 1-t+falloff] -> need r_max
        "second_last": [
            ("l_min", l_min),
            ("r_max", r_max),
        ]
    }


        
    fm_nodes = {}

    for name, value in layouts[role]:
        node = cmds.createNode("floatMath", name=f"{name}_zip_{i:02d}_add")
        cmds.setAttr(f"{node}.floatB", value)
        fm_nodes[name] = node

    if "l_max" in fm_nodes:
        cmds.connectAttr(f"{mdA}.outputX", f"{fm_nodes['l_max']}.floatA")

    if "l_min" in fm_nodes:
        cmds.connectAttr(f"{mdA}.outputY", f"{fm_nodes['l_min']}.floatA")

    if "r_max" in fm_nodes:
        cmds.connectAttr(f"{mdB}.outputX", f"{fm_nodes['r_max']}.floatA")

    if "r_min" in fm_nodes:
        cmds.connectAttr(f"{mdB}.outputY", f"{fm_nodes['r_min']}.floatA")

    rvL = cmds.createNode("remapValue", name=f"{dirL}_{posUP}_zip_{i:02d}_rmV")
    rvR = cmds.createNode("remapValue", name=f"{dirR}_{posUP}_zip_{i:02d}_rmV")

    cmds.connectAttr(f"{lCTRL}.zip", f"{rvL}.inputValue")
    cmds.connectAttr(f"{rCTRL}.zip", f"{rvR}.inputValue")

    # IMPORTANT:
    # explicit default ends, so the missing side stays clamped to tip-side boundary
    cmds.setAttr(f"{rvL}.inputMin", 0)
    cmds.setAttr(f"{rvL}.inputMax", 1)
    cmds.setAttr(f"{rvR}.inputMin", 0)
    cmds.setAttr(f"{rvR}.inputMax", 1)

    if role == "middle":

        cmds.connectAttr(f"{fm_nodes['l_max']}.outFloat", f"{rvL}.inputMax")
        cmds.connectAttr(f"{fm_nodes['l_min']}.outFloat", f"{rvL}.inputMin")

        cmds.connectAttr(f"{fm_nodes['r_max']}.outFloat", f"{rvR}.inputMax")
        cmds.connectAttr(f"{fm_nodes['r_min']}.outFloat", f"{rvR}.inputMin")

    elif role == "second":

        # left:  [0, t+falloff]
        cmds.connectAttr(f"{fm_nodes['l_max']}.outFloat", f"{rvL}.inputMax")

        # right: [1-t-falloff, 1]
        cmds.connectAttr(f"{fm_nodes['r_min']}.outFloat", f"{rvR}.inputMin")

    elif role == "second_last":

        # left:  [t-falloff, 1]
        cmds.connectAttr(f"{fm_nodes['l_min']}.outFloat", f"{rvL}.inputMin")

        # right: [0, 1-t+falloff]
        cmds.connectAttr(f"{fm_nodes['r_max']}.outFloat", f"{rvR}.inputMax")

    hsv = cmds.createNode("remapHsv", name=f"{dirL}_{posUP}_zip_{i:02d}_rmH")

    cmds.connectAttr(f"{rvL}.outValue", f"{hsv}.colorR")
    cmds.connectAttr(f"{rvR}.outValue", f"{hsv}.colorG")

    cmds.setAttr(f"{hsv}.color.colorB", 0)

    for attr in ("hue", "saturation"):
        curve = f"{hsv}.{attr}"
        cmds.setAttr(f"{curve}[0].{attr}_Position", 0)
        cmds.setAttr(f"{curve}[0].{attr}_FloatValue", 1)
        cmds.setAttr(f"{curve}[1].{attr}_Position", 1)
        cmds.setAttr(f"{curve}[1].{attr}_FloatValue", 1)

    return hsv



def createZIP(lCTRL, rCTRL, crvs, pos):
    mdA, mdB = createBase(lCTRL, rCTRL)

    if cmds.nodeType(crvs[0]) == "transform":
        shapes = cmds.listRelatives(crvs[0], shapes=True, fullPath=True) or []
        crvShpae_ZIP = next((s for s in shapes if cmds.nodeType(s) == "nurbsCurve"), None)
    else:
        crvShape_ZIP = crvs[0]

    if cmds.nodeType(crvs[1]) == "transform":
        shapes = cmds.listRelatives(crvs[1], shapes=True, fullPath=True) or []
        crvShape_ORI = next((s for s in shapes if cmds.nodeType(s) == "nurbsCurve"), None)
    else:
        crvShape_ORI = crvs[1]

    crvInfo_ORI = cmds.createNode("curveInfo", name=f"{crvShape_ORI}_crvInfo")
    cmds.connectAttr(f"{crvShape_ORI}.worldSpace[0]", f"{crvInfo_ORI}.inputCurve", force=True)

    crvInfo_ZIP = cmds.createNode("curveInfo", name=f"{crvShape_ZIP}_crvInfo")
    cmds.connectAttr(f"{crvShape_ZIP}.worldSpace[0]", f"{crvInfo_ZIP}.inputCurve", force=True)

    cvs_n_ORI = cmds.getAttr(f"{crvInfo_ORI}.controlPoints", size=True)
    cvs_n_ZIP = cmds.getAttr(f"{crvInfo_ZIP}.controlPoints", size=True)

    if cvs_n_ORI != cvs_n_ZIP:
        print("both crvs should be equal in cv points")
        return

    for i in range(cvs_n_ORI):

        role = get_cv_role(i, cvs_n_ORI)

        side = "l" if i < cvs_n_ORI / 2 else "r"

        if role not in ("first", "last"):
            myHsv = createZIP_blendHSv(mdA, mdB,
                "r", "l", "up", "lo",
                i, cvs_n_ORI,
                role,
                lCTRL, rCTRL)
        else:
            myHsv = None

        bC = cmds.createNode("blendColors",
            name=f"{side}_{pos}_lipzip_cv_{i:02d}_bC")

        cM = cmds.createNode("composeMatrix",
            name=f"{side}_{pos}_lipzip_cv_{i:02d}_cM")

        jnt = cmds.joint(
            name=f"{side}_{pos}_lipzip_{i:02d}_jnt",
            radius=0.1)

        cmds.connectAttr(
            f"{crvInfo_ORI}.controlPoints[{i}]",
            f"{bC}.color1",
            force=True)

        cmds.connectAttr(
            f"{crvInfo_ZIP}.controlPoints[{i}]",
            f"{bC}.color2",
            force=True)

        if myHsv:
            cmds.connectAttr(
                f"{myHsv}.outColorR",
                f"{bC}.blender",
                force=True)
        else:
            cmds.setAttr(f"{bC}.blender", 0)

        cmds.connectAttr(
            f"{bC}.output",
            f"{cM}.inputTranslate",
            force=True)

        cmds.connectAttr(
            f"{cM}.outputMatrix",
            f"{jnt}.offsetParentMatrix",
            force=True)
            
    else:
        print("both crvs should be equal in cv points")


sel = cmds.ls(sl=True)

if len(sel) < 3:
    raise RuntimeError("Select: mdA, mdB, then corner lCTRL and rCTRL.")

lCTRL = sel[0]
rCTRL = sel[1]

crvUP = sel[2]
crvDW = sel[3]

pos = "up"
createZIP(lCTRL, rCTRL, (crvUP, crvDW), pos)