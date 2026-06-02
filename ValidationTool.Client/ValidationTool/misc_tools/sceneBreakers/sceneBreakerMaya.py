import maya.cmds as cmds


def add_uv_chaos(obj):
    # create extra UV sets
    for i in range(1, 5):
        set_name = f"uvSet{i}"
        if not cmds.polyUVSet(obj, q=True, allUVSets=True):
            continue

        cmds.polyUVSet(obj, create=True, uvSet=set_name)

    # force duplicate UV sets (if possible)
    try:
        cmds.polyUVSet(obj, rename=True, uvSet="map1", newUVSet="uvSet1_dup")
    except:
        pass


def build_test_scene():
    cmds.file(new=True, force=True)

    # ----------------------------------------
    # CLEAN BASE (geometry stress)
    # ----------------------------------------
    for i in range(4):
        obj = cmds.polyCube(name=f"ENV_{i}")[0]
        cmds.polySmooth(obj, dv=i + 4)
        cmds.delete(obj, constructionHistory=True)

        # extreme scale (stress test >1000)
        cmds.setAttr(f"{obj}.scaleX", 1500 * (i + 1))
        cmds.setAttr(f"{obj}.scaleY", 1200 * (i + 1))
        cmds.setAttr(f"{obj}.scaleZ", 800 * (i + 1))

        add_uv_chaos(obj)

    # ----------------------------------------
    # NAMING + NEGATIVE SCALE CHAOS
    # ----------------------------------------
    ch = cmds.polySphere(name="CH_shieh")[0]
    cmds.polySmooth(ch, dv=3)
    cmds.delete(ch, constructionHistory=True)

    cmds.setAttr(f"{ch}.scaleX", -1)  # negative scale

    add_uv_chaos(ch)

    hero = cmds.polySphere(name="HERO__shieh")[0]  # double underscore
    cmds.polySmooth(hero, dv=3)
    cmds.delete(hero, constructionHistory=True)

    cmds.setAttr(f"{hero}.scaleX", 2)
    cmds.setAttr(f"{hero}.scaleY", 5)  # non-uniform scale
    cmds.setAttr(f"{hero}.scaleZ", 0.5)

    add_uv_chaos(hero)
    
    # ----------------------------------------
    # ZERO VERTEX OBJECT (hard fail geometry)
    # ----------------------------------------
    
    empty = cmds.polyCube(name="EMPTY_ZERO")[0]
    
    # delete its shape completely -> leaves transform with no geometry
    shapes = cmds.listRelatives(empty, shapes=True) or []
    if shapes:
        cmds.delete(shapes)
    
    # optional: ensure it still exists but is empty transform
    cmds.setAttr(f"{empty}.visibility", 1)

    # ----------------------------------------
    # HISTORY NOISE + TRANSFORM ISSUES
    # ----------------------------------------
    env1 = cmds.polyTorus(name="ENV_shiehhhh")[0]
    cmds.polySmooth(env1, dv=3)

    cmds.setAttr(f"{env1}.scaleX", 2000)  # extreme scale
    cmds.setAttr(f"{env1}.scaleY", 1)
    cmds.setAttr(f"{env1}.scaleZ", 1)

    cmds.delete(env1, constructionHistory=True)
    add_uv_chaos(env1)

    # ----------------------------------------
    # MATERIAL SLOT / PROP STRESS
    # ----------------------------------------
    prp = cmds.polyTorus(name="PRP_mine")[0]
    cmds.polySmooth(prp, dv=4)
    cmds.delete(prp, constructionHistory=True)

    cmds.setAttr(f"{prp}.scaleX", 1)
    cmds.setAttr(f"{prp}.scaleY", 3)
    cmds.setAttr(f"{prp}.scaleZ", 10)

    add_uv_chaos(prp)

    # ----------------------------------------
    # MODIFIED CHAOS OBJECT
    # ----------------------------------------
    mod = cmds.polyTorus(name="some_MOD")[0]
    cmds.polySmooth(mod, dv=5)
    cmds.delete(mod, constructionHistory=True)

    cmds.setAttr(f"{mod}.scaleX", -3)  # negative scale
    cmds.setAttr(f"{mod}.scaleY", 2000)  # extreme scale
    cmds.setAttr(f"{mod}.scaleZ", 0)  # zero scale (bonus fail)

    add_uv_chaos(mod)

    # ----------------------------------------
    # NAMING FAIL
    # ----------------------------------------
    broken = cmds.polyTorus(name="brokennaming")[0]
    cmds.polySmooth(broken, dv=5)
    cmds.delete(broken, constructionHistory=True)

    cmds.setAttr(f"{broken}.scaleX", 1)
    cmds.setAttr(f"{broken}.scaleY", 1)
    cmds.setAttr(f"{broken}.scaleZ", 1)

    add_uv_chaos(broken)


build_test_scene()