from pathlib import Path
import shutil

root = Path(__file__).resolve().parents[1]
out = root / "_site"

if out.exists():
    shutil.rmtree(out)
out.mkdir()

for name in ["index.html", "bus.glb", "bus_ref.jpg", ".nojekyll"]:
    src = root / name
    if src.exists():
        shutil.copy2(src, out / name)

index = out / "index.html"
text = index.read_text(encoding="utf-8")

old_traverse = """              } else if (parentName.includes('panto_arm1') || objName.includes('panto_arm1')) {
                pantoArm1 = c;
              } else if (parentName.includes('panto_topbar') || objName.includes('panto_topbar')) {
                pantoTopBar = c;
              }"""
new_traverse = """              } else if (parentName.includes('panto_arm1') || objName.includes('panto_arm1')) {
                pantoArm1 = c;
              } else if (parentName.includes('panto_arm2') || objName.includes('panto_arm2')) {
                pantoArm2 = c;
              } else if (parentName.includes('panto_topbar') || objName.includes('panto_topbar')) {
                pantoTopBar = c;
              }"""

old_doors = """        if (frontDoorLeft) {
          frontDoorLeft.position.z += (5.9 + doorOffset - frontDoorLeft.position.z) * 0.1;
          frontDoorRight.position.z += (5.58 - doorOffset - frontDoorRight.position.z) * 0.1;
          midDoorLeft.position.z += (-0.59 + doorOffset - midDoorLeft.position.z) * 0.1;
          midDoorRight.position.z += (-0.91 - doorOffset - midDoorRight.position.z) * 0.1;
        }"""
new_doors = """        if (frontDoorLeft) {
          frontDoorLeft.position.z += (5.9 + doorOffset - frontDoorLeft.position.z) * 0.1;
        }
        if (frontDoorRight) {
          frontDoorRight.position.z += (5.58 - doorOffset - frontDoorRight.position.z) * 0.1;
        }
        if (midDoorLeft) {
          midDoorLeft.position.z += (-0.59 + doorOffset - midDoorLeft.position.z) * 0.1;
        }
        if (midDoorRight) {
          midDoorRight.position.z += (-0.91 - doorOffset - midDoorRight.position.z) * 0.1;
        }"""

old_panto = """        if (pantoArm1) {
          pantoArm1.rotation.x += (pantoRot - pantoArm1.rotation.x) * 0.08;
          pantoArm2.rotation.x += (pantoRot - pantoArm2.rotation.x) * 0.08;
          pantoTopBar.position.y += ((isPantoUp ? 1.15 : 0.4) - pantoTopBar.position.y) * 0.08;
        }"""
new_panto = """        if (pantoArm1) {
          pantoArm1.rotation.x += (pantoRot - pantoArm1.rotation.x) * 0.08;
        }
        if (pantoArm2) {
          pantoArm2.rotation.x += (pantoRot - pantoArm2.rotation.x) * 0.08;
        }
        if (pantoTopBar) {
          pantoTopBar.position.y += ((isPantoUp ? 1.15 : 0.4) - pantoTopBar.position.y) * 0.08;
        }"""

replacements = [
    (old_traverse, new_traverse, "pantograph arm2 traversal"),
    (old_doors, new_doors, "door object guards"),
    (old_panto, new_panto, "pantograph object guards"),
]

for old, new, label in replacements:
    if old not in text:
        raise RuntimeError(f"Expected source block not found: {label}")
    text = text.replace(old, new, 1)

index.write_text(text, encoding="utf-8")
print("Prepared GitHub Pages artifact with safe 3D animation guards.")
