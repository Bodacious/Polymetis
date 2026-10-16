"""Dump geometry from main PCB and both plates to /w/build/verify/geom_*.json"""
import json, pcbnew
T=pcbnew.ToMM
def outline_polys(b):
    ps=pcbnew.SHAPE_POLY_SET()
    b.GetBoardPolygonOutlines(ps)
    out=[]
    for i in range(ps.OutlineCount()):
        o=ps.Outline(i); out.append({"outer":[(T(o.CPoint(k).x),T(o.CPoint(k).y)) for k in range(o.PointCount())],
            "holes":[[(T(h.CPoint(k).x),T(h.CPoint(k).y)) for k in range(h.PointCount())] for h in [ps.Hole(i,j) for j in range(ps.HoleCount(i))]]})
    return out
def npth(b):
    r=[]
    for fp in b.GetFootprints():
        for p in fp.Pads():
            if p.HasHole():
                q=p.GetPosition(); r.append({"ref":fp.GetReference(),"pad":p.GetNumber(),"x":T(q.x),"y":T(q.y),"d":T(p.GetDrillSize().x),"net":p.GetNetname()})
    return r
b=pcbnew.LoadBoard("pcb/polymetis.kicad_pcb")
sw=[]
for fp in b.GetFootprints():
    r=fp.GetReference()
    if r.startswith("K_"):
        pads={p.GetNumber():p.GetNetname() for p in fp.Pads() if p.GetNumber()}
        q=fp.GetPosition()
        sw.append({"ref":r,"x":T(q.x),"y":T(q.y),"rot":fp.GetOrientationDegrees(),"fp":fp.GetFPIDAsString(),"pads":pads})
diodes={}
for fp in b.GetFootprints():
    if fp.GetReference().startswith("D_"):
        diodes[fp.GetReference()]={p.GetNumber():p.GetNetname() for p in fp.Pads()}
u3=[{"pad":p.GetNumber(),"fn":p.GetPinFunction(),"net":p.GetNetname()} for p in b.FindFootprintByReference("U3").Pads()]
usb=b.FindFootprintByReference("USB1"); bb=usb.GetBoundingBox(False)
st=b.FindFootprintByReference("ST1")
json.dump({"switches":sw,"diodes":diodes,"u3":u3,"usb":{"x":T(usb.GetPosition().x),"y":T(usb.GetPosition().y),"bbox":[T(bb.GetLeft()),T(bb.GetTop()),T(bb.GetRight()),T(bb.GetBottom())]},
  "st1":{"x":T(st.GetPosition().x),"y":T(st.GetPosition().y)},"outline":outline_polys(b),"holes":npth(b)},open("/w/build/verify/geom_pcb.json","w"))
for name in ("top-plate","bottom-plate"):
    pb=pcbnew.LoadBoard(f"{name}/{name}.kicad_pcb")
    json.dump({"outline":outline_polys(pb),"holes":npth(pb),"thickness":T(pb.GetDesignSettings().GetBoardThickness())},open(f"/w/build/verify/geom_{name}.json","w"))
print("ok", len(sw), "switches")
