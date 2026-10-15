"""Generate the Polymetis middle frame as an STL.

The frame is a flat ring between the top and bottom plates. Its outer shell and the eight M2
holes are taken from the source frame (`frame-source.stl`); the inner cavity is
rebuilt from the main PCB outline (the original cavity was 1.6 mm narrower than the PCB), and
the thickness comes from the KS-33 stack:

    plate-to-PCB gap 1.30 (Gateron KS-33 drawing: 2.50 plate top to PCB top, 1.20 plate)
  + PCB 1.60
  + tallest part under the PCB: flash U4, SOIC-8 208-mil, 2.16 max (Winbond W25Q16JV
    datasheet); the hot-swap sockets are 1.87 (Gateron KS-2P02B01-02 drawing)
  + 0.24 clearance
  = 5.30 mm

The USB-C receptacle hangs 3.26 mm below the PCB (HRO TYPE-C-31-M-12 drawing); it is cleared by
the 16 mm USB opening in the frame and the matching notch in the bottom plate.

Usage: python3 case/make_frame.py <pcb outline json>
The outline JSON holds the main PCB Edge.Cuts outer outline in KiCad millimetres.
Frame coordinates: origin at the key-area centre, x to the right and y to the back in top view,
so frame_x = 142.875 - pcb_x and frame_y = 47.625 - pcb_y.
"""
import json
import sys
from pathlib import Path

import numpy as np
import trimesh
from shapely.geometry import Polygon, box
from shapely.ops import unary_union

HERE = Path(__file__).parent
THICKNESS = 5.30
CLEARANCE = 0.30          # gap between PCB edge and frame wall
USB_X = (116.0, 132.0)    # USB opening, unchanged from the original frame


def original_shell_and_holes():
    m = trimesh.load(HERE / "frame-source.stl")
    top = [Polygon(t[:, :2]).buffer(0) for t in m.triangles if np.allclose(t[:, 2], m.bounds[1][2])]
    u = unary_union([p for p in top if p.area > 0])
    shell = u.convex_hull
    holes = [Polygon(h) for h in u.interiors]
    assert len(holes) == 8, len(holes)
    return shell, holes


def cavity_from_pcb(outline_mm):
    pts = [(142.875 - x, 47.625 - y) for x, y in outline_mm]
    pcb = Polygon(pts).buffer(0)
    return pcb.buffer(CLEARANCE, join_style=2)


def main():
    outline = json.loads(Path(sys.argv[1]).read_text())
    shell, holes = original_shell_and_holes()
    cav = cavity_from_pcb(outline)
    top = shell.bounds[3]
    usb = box(USB_X[0], cav.bounds[3] - 15, USB_X[1], top + 1)
    frame = shell.difference(unary_union([cav, usb] + holes))
    assert frame.geom_type == "Polygon", frame.geom_type

    walls = {
        "left": cav.bounds[0] - shell.bounds[0],
        "right": shell.bounds[2] - cav.bounds[2],
        "front": cav.bounds[1] - shell.bounds[1],
        "back": top - cav.bounds[3],
        "hole to cavity": min(h.distance(cav) for h in holes),
    }
    mesh = trimesh.creation.extrude_polygon(frame, THICKNESS)
    out = HERE / "polymetis-frame.stl"
    mesh.export(out)
    print(f"{out.name}: {mesh.extents.round(2)} mm, watertight={mesh.is_watertight}")
    print("cavity", [round(c, 2) for c in cav.bounds])
    print("walls", {k: round(v, 2) for k, v in walls.items()})


if __name__ == "__main__":
    main()
