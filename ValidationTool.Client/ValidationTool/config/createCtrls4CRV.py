import maya.cmds as cmds

def multMatrixOfs2CRVctrlPoints(myCRV, main_grp):
    
    # Get shape
    if cmds.nodeType(myCRV) == "transform":
        shapes = cmds.listRelatives(myCRV, shapes=True, fullPath=True) or []
        curve_shape = next((s for s in shapes if cmds.nodeType(s) == "nurbsCurve"), None)
    else:
        curve_shape = myCRV
    
    if not curve_shape:
        raise RuntimeError("No nurbsCurve shape found.")
    
    num_cvs = cmds.getAttr(f"{curve_shape}.controlPoints", size=True)
    
    # parent matrix
    parent = cmds.listRelatives(curve_shape, parent=True, fullPath=True)
    if parent:
        parent_world = cmds.getAttr(f"{parent[0]}.worldMatrix[0]")
    else:
        parent_world = (1,0,0,0,
                        0,1,0,0,
                        0,0,1,0,
                        0,0,0,1)
                        
    
    nodeName = curve_shape.split("|")[-1]
        
    for i in range(num_cvs):
    
        p = cmds.getAttr(f"{curve_shape}.controlPoints[{i}]")[0]
        
        
        mm = cmds.createNode("multMatrix", name=f"{nodeName}_cv_{i:02d}_mM")
    
        # --- CV as matrix ---
        cv_matrix = (
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            p[0], p[1], p[2], 1
        )
        #bake and hardcode the CRVctrlPoint world space into matrixIn[0]
        cmds.setAttr(f"{mm}.matrixIn[0]", *cv_matrix, type="matrix")
        
        # CTRL HIERARCHY
        ofs  = cmds.createNode("transform", name=f"{nodeName}_{i:02d}_ofs")
        sdk  = cmds.createNode("transform", name=f"{nodeName}_{i:02d}_sdk")
        aut  = cmds.createNode("transform", name=f"{nodeName}_{i:02d}_aut")
        ctrl = cmds.spaceLocator(name=f"{nodeName}_{i:02d}_ctrl")[0]
        
        cmds.parent(ctrl, aut)
        cmds.parent(aut, sdk)
        cmds.parent(sdk, ofs)
        cmds.xform(ofs, ws=True, t=p)
        
        cmds.parent(ofs, main_grp)
        
        cmds.connectAttr(
            f"{ctrl}.dagLocalMatrix",
            f"{mm}.matrixIn[1]",
            force=True
        )
        cmds.connectAttr(
            f"{aut}.dagLocalMatrix",
            f"{mm}.matrixIn[2]",
            force=True
        )
        cmds.connectAttr(
            f"{sdk}.dagLocalMatrix",
            f"{mm}.matrixIn[3]",
            force=True
        )
    

        dm = cmds.createNode("decomposeMatrix", name=f"{nodeName}_cv_{i:02d}_dM")
        cmds.connectAttr(f"{mm}.matrixSum", f"{dm}.inputMatrix", force=True)
    
        cmds.connectAttr(
            f"{dm}.outputTranslate",
            f"{curve_shape}.controlPoints[{i}]",
            force=True
        )
    
    print(f"Created {num_cvs} matrix-driven CV nodes (no composeMatrix).")
    


def jntMatrixesFromCRVpoints(myCRV, main_grp):
    
    curve = myCRV
    
    # Get curve shape
    if cmds.nodeType(curve) == "transform":
        shapes = cmds.listRelatives(curve, shapes=True, fullPath=True) or []
        curve_shape = next((s for s in shapes if cmds.nodeType(s) == "nurbsCurve"), None)
    else:
        curve_shape = curve
    
    if not curve_shape:
        raise RuntimeError("No nurbsCurve shape found.")
    
    # curveInfo
    curve_info = cmds.createNode("curveInfo", name=f"{curve}_crvInfo")
    cmds.connectAttr(f"{curve_shape}.worldSpace[0]", f"{curve_info}.inputCurve", force=True)
    
    # number of CVs
    num_cvs = cmds.getAttr(f"{curve_info}.controlPoints", size=True)
    
    if not cmds.objExists("UPvector_WS"):
        secondaryTargetMatrix = cmds.createNode("transform", name="{nodeName}_UPvector_WS")
    else:
        secondaryTargetMatrix = "offsetUPvector_WS"
    
    for i in range(num_cvs):
    
        # composeMatrix per CV
        cm = cmds.createNode("composeMatrix", name=f"{curve}_cv_{i:02d}_cM")
    
        cmds.connectAttr(
            f"{curve_info}.controlPoints[{i}]",
            f"{cm}.inputTranslate",
            force=True
        )
    
        # aimMatrix
        aim = cmds.createNode("aimMatrix", name=f"{curve}_cv_{i:02d}_aM")
        cmds.setAttr(f"{aim}.secondaryTargetVector", 0, 1, 0, type="double3")
        cmds.setAttr(f"{aim}.secondaryMode", 1)
    
        cmds.connectAttr(
            f"{main_grp}.worldMatrix[0]",
            f"{aim}.inputMatrix",
            force=True
        )
            
        cmds.connectAttr(
            f"{secondaryTargetMatrix}.worldMatrix[0]",
            f"{aim}.secondaryTargetMatrix",
            force=True
        )
            
        cmds.connectAttr(
            f"{cm}.outputMatrix",
            f"{aim}.primaryTargetMatrix",
            force=True
        )
    
        # joint driven by aimMatrix output
        jnt = cmds.createNode("joint", name=f"{curve}_cv_{i:02d}_jnt")
    
        cmds.connectAttr(
            f"{aim}.outputMatrix",
            f"{jnt}.offsetParentMatrix",
            force=True
        )
        
        tip = cmds.createNode("joint", name=jnt.replace("jnt", "tip_jnt"))
        cmds.parent(tip, jnt)
        
        p1 = cmds.xform(jnt, q=True, ws=True, t=True)
        p2 = cmds.getAttr(f"{curve_info}.controlPoints[{i}]")[0]
        
        dist = ((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2 + (p2[2]-p1[2])**2) ** 0.5
        
        cmds.setAttr(f"{tip}.translateX", dist)
        cmds.setAttr(f"{tip}.translateY", 0)
        cmds.setAttr(f"{tip}.translateZ", 0)
        cmds.setAttr(f"{tip}.radius", 0.1)
        cmds.setAttr(f"{jnt}.radius", 0.1)
        cmds.makeIdentity(tip, apply=True, r=True, jo=True)
    
    print(f"Created rig for {num_cvs} CVs.")


def dfrmCRVsetting(curveTransform):
    orig_crv = curveTransform
    
    shapes = cmds.listRelatives(orig_crv, shapes=True, fullPath=True) or []
    orig_shape = next((s for s in shapes if cmds.nodeType(s) == "nurbsCurve"), None)
    
    if not orig_shape:
        raise RuntimeError("Selected object is not a NURBS curve.")
    
    drv_crv = cmds.duplicate(orig_crv, name=f"{orig_crv}_drv")[0]

    cmds.rebuildCurve(
        drv_crv,
        ch=False,
        rpo=True,
        rt=0,
        end=1,
        kr=0,
        kcp=False,
        kep=True,
        kt=False,
        s=4,
        d=3,
        tol=0.01
    )

    cmds.delete(orig_crv, constructionHistory=True)
    cmds.delete(drv_crv, constructionHistory=True)

    cmds.wire(
        orig_crv,
        wire=drv_crv,
        name=f"{orig_crv}_wire"
    )

    return orig_crv, drv_crv


sel = cmds.ls(sl=True, type="transform")

if not sel:
    raise RuntimeError("Select a linear curve transform and a main_ctrl curve transform")
    
orig_crv, drv_crv = dfrmCRVsetting(sel[0])

multMatrixOfs2CRVctrlPoints(drv_crv, sel[1])
#jntMatrixesFromCRVpoints(orig_crv, sel[1])